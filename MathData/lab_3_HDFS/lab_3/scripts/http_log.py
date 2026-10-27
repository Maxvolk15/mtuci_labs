#!/usr/bin/env python3
"""Часть 3. Журнал HTTP-запросов DuckDB для одного запроса.
Запуск: make httplog FILE=txn_zstd.parquet Q="select count(*) from {src}"
В тексте запроса {src} заменяется на чтение файла из вашего префикса."""
import sys

from common import duck, my

f, sql = sys.argv[1], sys.argv[2]
con = duck()
con.execute("call enable_logging('HTTP')")
con.execute(sql.format(src=f"read_parquet('{my(f)}')")).fetchall()
rows = con.execute("""
    select request.type, coalesce(request.headers['Range'], ''), response.status,
           request.headers['Authorization']
    from duckdb_logs_parsed('HTTP') order by timestamp""").fetchall()
for method, rng, status, _ in rows:
    print(f"{method:5s} {rng:34s} {status}")
print(f"\nвсего запросов: {len(rows)}")
print("\nЗаголовок Authorization первого запроса (подпись сокращена):")
print("  " + rows[0][3][:150] + "…")
