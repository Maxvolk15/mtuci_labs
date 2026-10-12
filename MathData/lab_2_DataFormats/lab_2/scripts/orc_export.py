#!/usr/bin/env python3
"""
Часть 2 (продолжение). ORC рядом с Parquet — на одном движке (pyarrow).

DuckDB ORC не читает, поэтому честное сравнение форматов делаем через
pyarrow: он умеет и Parquet, и ORC. Сравнивать Parquet-в-DuckDB с ORC-в-pyarrow
нельзя — это сравнение движков, а не форматов.

Запуск: python scripts/orc_export.py
"""
import os
import pathlib
import time

import duckdb
import pyarrow.orc as orc
import pyarrow.parquet as pq

os.environ["TZDIR"] = "C:/Users/maxym/VSCode/mtuci_labs/MathData/lab_2_DataFormats/lab_2/venv/Lib/site-packages/tzdata/zoneinfo"
ROOT = pathlib.Path(__file__).resolve().parent.parent
DATA = ROOT / "data"

con = duckdb.connect(str(ROOT / "formats.duckdb"), read_only=True)
table = con.sql("select * from txn_wide").to_arrow_table()   # DuckDB → Arrow Table
print(f"txn_wide → Arrow: {table.num_rows:,} строк, {table.nbytes / 1e6:.0f} МБ в памяти")

t0 = time.perf_counter()
orc.write_table(table, DATA / "txn.orc", compression="ZSTD")
print(f"ORC (zstd) записан за {time.perf_counter() - t0:.1f} с")

for name in ("txn.orc", "txn_zstd.parquet"):
    print(f"  {name:20s} {os.path.getsize(DATA / name) / 1e6:6.1f} МБ")

# Один и тот же запрос — три колонки из 28 — через один движок
COLS = ["status", "federal_district", "amount_rub"]


def bench(fn, runs=3):
    best = float("inf")
    for _ in range(runs):
        t = time.perf_counter()
        fn()
        best = min(best, time.perf_counter() - t)
    return best


print(f"чтение 3 колонок из 28 (pyarrow, лучшее из 3):")
print(f"  Parquet: {bench(lambda: pq.read_table(DATA / 'txn_zstd.parquet', columns=COLS)):.3f} с")
print(f"  ORC:     {bench(lambda: orc.read_table(DATA / 'txn.orc', columns=COLS)):.3f} с")
print(f"чтение всех 28 колонок:")
print(f"  Parquet: {bench(lambda: pq.read_table(DATA / 'txn_zstd.parquet')):.3f} с")
print(f"  ORC:     {bench(lambda: orc.read_table(DATA / 'txn.orc')):.3f} с")

# Устройство ORC: stripes вместо row groups, индексы внутри
f = orc.ORCFile(DATA / "txn.orc")
print(f"ORC: stripes = {f.nstripes}, строк = {f.nrows:,}, сжатие = {f.compression}")
