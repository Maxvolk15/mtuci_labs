#!/usr/bin/env python3
"""Часть 4. Выполнить scripts/cost.sql для одного Parquet-файла и напечатать результаты.
Запуск: python scripts/cost.py data/txn_zstd.parquet   (или make cost FILE=...)"""
import pathlib
import sys

import duckdb

f = sys.argv[1] if len(sys.argv) > 1 else "data/txn_zstd.parquet"
sql_file = pathlib.Path(__file__).resolve().parent / "cost.sql"
con = duckdb.connect()
con.execute("set variable f = ?", [f])
for stmt in con.extract_statements(sql_file.read_text(encoding="utf-8")):
    print(con.sql(stmt.query))
