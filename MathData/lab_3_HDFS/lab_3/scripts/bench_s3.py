#!/usr/bin/env python3
"""Часть 3. Запросы лабы 2 к файлам в объектном хранилище.

На каждый запрос — новое соединение и выключенный кеш: иначе футер и колонки,
прочитанные предыдущим запросом, исказят счёт. Печатает markdown-таблицу:
получено байт / запросов GET / секунды.
Запуск: make bench
"""
import time

from common import duck, http_stats, my

FILES = ["txn_zstd.parquet", "txn_shuffled.parquet", "txn_by_merchant.parquet",
         "txn_rg10k.parquet", "txn_rg1m.parquet"]
QUERIES = [   # те же тексты, что в lab_2/scripts/bench.py
    ("Q0", "select count(*) from {src}"),
    ("Q1", "select federal_district, sum(amount_rub) from {src} "
           "where status = 'approved' group by 1"),
    ("Q2", "select count(*), sum(amount_rub) from {src} where txn_date = date '2026-07-15'"),
    ("Q3", "select count(*), sum(amount_rub) from {src} where merchant_id = 'M3300'"),
    ("Q4", "select fio, amount_rub from {src} where txn_id = '2026-07-00123456'"),
]

print("| Файл | " + " | ".join(q for q, _ in QUERIES) + " |")
print("|---|" + "---|" * len(QUERIES))
for f in FILES:
    cells = []
    for _, sql in QUERIES:
        con = duck()
        t = time.perf_counter()
        plan = con.execute("explain analyze " + sql.format(
            src=f"read_parquet('{my(f)}')")).fetchall()[0][1]
        s = http_stats(plan)
        cells.append(f"{s['in']} / {s['GET']} GET / {time.perf_counter() - t:.2f} с")
    print(f"| {f} | " + " | ".join(cells) + " |")
