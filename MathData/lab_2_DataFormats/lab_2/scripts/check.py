#!/usr/bin/env python3
"""
Самопроверка лабы 2: окружение, таблица txn_wide и обязательные файлы в data/.
Запуск: make check. Контрольные числа детерминированы (данные лабы 1 +
duckdb==1.5.5), у всех студентов обязаны совпасть.
"""
import os
import pathlib
import sys

import duckdb

ROOT = pathlib.Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
failures = []


def check(name, ok, detail=""):
    print(f"  {'ok ' if ok else 'FAIL'}  {name} {detail}")
    if not ok:
        failures.append(name)


print("Окружение:")
check("duckdb == 1.5.5", duckdb.__version__ == "1.5.5", duckdb.__version__)
for mod in ("pyarrow", "fastavro", "polars", "pandas"):
    try:
        __import__(mod)
        check(f"{mod} установлен", True)
    except ImportError:
        check(f"{mod} установлен (нужен для частей 2 и 5)", False)

print("Таблица txn_wide:")
if not (ROOT / "formats.duckdb").exists():
    check("formats.duckdb существует (make build)", False)
else:
    con = duckdb.connect(str(ROOT / "formats.duckdb"), read_only=True)
    n, cols = con.execute(
        "select count(*), (select count(*) from information_schema.columns "
        "where table_name = 'txn_wide') from txn_wide").fetchone()
    check("строк", n == 2_312_606, f"{n:,} (ожидание 2 312 606)")
    check("колонок", cols == 28, f"{cols} (ожидание 28)")
    con.close()

print("Файлы части 1:")
expected_mb = {  # имя: (мин, макс) МБ — коридор на случай другой версии zstd
    "txn.csv": (840, 870),
    "txn_none.parquet": (225, 245),
    "txn_zstd.parquet": (85, 95),
    "txn_snappy.parquet": (120, 132),
    "txn_shuffled.parquet": (96, 106),
    "txn_by_merchant.parquet": (58, 66),
    "txn_rg10k.parquet": (105, 118),
    "txn_rg1m.parquet": (79, 88),
    "txn.csv.gz": (140, 152),
}
for name, (lo, hi) in expected_mb.items():
    p = DATA / name
    if not p.exists():
        check(name, False, "— файла нет")
        continue
    mb = os.path.getsize(p) / 1e6
    check(name, lo <= mb <= hi, f"{mb:.1f} МБ (ожидание {lo}..{hi})")

if (DATA / "txn_zstd.parquet").exists():
    con = duckdb.connect()
    rg = con.execute("select num_row_groups from parquet_file_metadata(?)",
                     [str(DATA / "txn_zstd.parquet")]).fetchone()[0]
    check("row groups в txn_zstd.parquet", rg == 19, f"{rg} (ожидание 19)")

if failures:
    print(f"\nПровалено: {len(failures)} — {failures}")
    sys.exit(1)
print("\nВсе проверки пройдены.")
