#!/usr/bin/env python3
"""
Лаба 2. Бенчмарк: один и тот же набор запросов ко всем файлам в data/,
на одном движке (DuckDB), с тёплым кешем. Печатает markdown-таблицы
для отчёта: размер файла и время каждого запроса (лучшее из 3 прогонов).

Запуск: python scripts/bench.py            # все файлы из data/
        python scripts/bench.py txn.csv txn_zstd.parquet   # только эти

Сравнивать можно только цифры, снятые на одной машине в одном прогоне:
абсолютные секунды у всех разные, отношения — примерно одинаковые.
"""
import os
import pathlib
import sys
import time

import duckdb

DATA = pathlib.Path(__file__).resolve().parent.parent / "data"
RUNS = 3

# (метка, шаблон запроса; {src} заменяется на функцию чтения файла)
QUERIES = [
    ("Q0 count(*)",
     "select count(*) from {src}"),
    ("Q1 агрегат 2 из 28 колонок",
     "select federal_district, sum(amount_rub) from {src} "
     "where status = 'approved' group by 1"),
    ("Q2 фильтр по дате",
     "select count(*), sum(amount_rub) from {src} "
     "where txn_date = date '2026-07-15'"),
    ("Q3 редкий мерчант",
     "select count(*), sum(amount_rub) from {src} where merchant_id = 'M3300'"),
    ("Q4 точечный поиск по txn_id",
     "select fio, amount_rub from {src} where txn_id = '2026-07-00123456'"),
    ("Q5 все 28 колонок",
     "select max(length(concat_ws('|', columns(*)))) from {src}"),
]


def reader(path: pathlib.Path) -> str:
    name = path.name
    if name.endswith((".parquet",)):
        return f"read_parquet('{path}')"
    if name.endswith((".csv", ".csv.gz")):
        # типы задаём явно там, где авто-вывод врёт (см. часть 1 задания)
        return (f"read_csv('{path}', types={{'mcc': 'VARCHAR', 'txn_date': 'DATE'}})")
    if name.endswith((".jsonl", ".json")):
        return f"read_json('{path}')"
    return None


def bench(con, sql: str) -> float:
    best = float("inf")
    for _ in range(RUNS):
        t0 = time.perf_counter()
        con.execute(sql).fetchall()
        best = min(best, time.perf_counter() - t0)
    return best


def main():
    names = sys.argv[1:] or sorted(p.name for p in DATA.iterdir()
                                   if p.is_file() and reader(p))
    con = duckdb.connect()
    header = "| файл | МБ | " + " | ".join(q for q, _ in QUERIES) + " |"
    print(header)
    print("|" + "---|" * (2 + len(QUERIES)))
    for name in names:
        path = DATA / name
        src = reader(path)
        if not src:
            continue
        cells = [name, f"{os.path.getsize(path) / 1e6:.1f}"]
        for _, tmpl in QUERIES:
            try:
                cells.append(f"{bench(con, tmpl.format(src=src)):.3f}")
            except Exception as e:  # noqa: BLE001
                cells.append("ошибка: " + str(e).splitlines()[0][:40])
        print("| " + " | ".join(cells) + " |")
        sys.stdout.flush()


if __name__ == "__main__":
    main()
