#!/usr/bin/env python3
"""Часть 3.5. Один запрос Q1 к txn_zstd.parquet: байты, запросы, секунды.
Запускается дважды — на ноутбуке (через VPN) и на node1 (в одной сети с хранилищем)."""
import time

from common import duck, http_stats, my

con = duck()
t = time.perf_counter()
plan = con.execute(
    "explain analyze select federal_district, sum(amount_rub) "
    f"from read_parquet('{my('txn_zstd.parquet')}') where status = 'approved' group by 1"
).fetchall()[0][1]
s = http_stats(plan)
print(f"получено {s['in']}, запросов GET {s['GET']}, {time.perf_counter() - t:.2f} с")
