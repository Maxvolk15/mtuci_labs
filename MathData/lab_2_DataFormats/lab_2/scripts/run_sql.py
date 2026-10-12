#!/usr/bin/env python3
"""Выполнить SQL-файл в базе formats.duckdb (переменная data_dir — путь к данным лабы 1).
Запуск: python scripts/run_sql.py scripts/build_wide.sql [../lab_1/data]"""
import pathlib
import sys
import time

import duckdb

sql_file = pathlib.Path(sys.argv[1])
data_dir = sys.argv[2] if len(sys.argv) > 2 else "../lab_1/data"
con = duckdb.connect("formats.duckdb")
con.execute("set variable data_dir = ?", [data_dir])
for stmt in con.extract_statements(sql_file.read_text(encoding="utf-8")):
    t0 = time.perf_counter()
    con.execute(stmt.query)
    head = next(l.strip() for l in stmt.query.splitlines() if l.strip() and not l.strip().startswith("--"))
    print(f"  {time.perf_counter() - t0:6.1f} с  {head[:80]}")
print(f"{sql_file}: выполнено")
