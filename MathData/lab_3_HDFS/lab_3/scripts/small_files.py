#!/usr/bin/env python3
"""Часть 4. Одни и те же данные одним файлом и сотнями мелких.

Берём июль, пять колонок. Пишем дважды: big/july.parquet и small/ —
по файлу на каждый час каждого дня (ключи вида txn_date=…/hr=…/data_0.parquet).
Затем два запроса к обоим вариантам: байты, число запросов, секунды.
Запуск: make small
"""
import time

from common import BUCKET, DATASETS, SINITSA, duck, http_stats, login, my, s3

SRC = f"s3://{DATASETS}/{SINITSA}/txn_zstd.parquet"
JULY = (f"select txn_ts, txn_date, hour(txn_ts) as hr, status, federal_district, amount_rub "
        f"from read_parquet('{SRC}') "
        f"where txn_date between date '2026-07-01' and date '2026-07-31'")

con = duck()
t = time.perf_counter()
con.execute(f"copy ({JULY}) to '{my('big/july.parquet')}' (format parquet, compression zstd)")
print(f"big/   записан за {time.perf_counter() - t:.1f} с")
t = time.perf_counter()
con.execute(f"copy ({JULY}) to '{my('small')}' "
            f"(format parquet, compression zstd, partition_by (txn_date, hr), overwrite_or_ignore)")
print(f"small/ записан за {time.perf_counter() - t:.1f} с")

c, me = s3(), login()
for prefix in ("big/", "small/"):
    pages = c.get_paginator("list_objects_v2").paginate(Bucket=BUCKET, Prefix=f"{me}/{prefix}")
    objs = [o for p in pages for o in p.get("Contents", [])]
    print(f"{prefix:7s} объектов {len(objs):4d}, всего {sum(o['Size'] for o in objs) / 1e6:.1f} МБ")

QUERIES = [
    ("весь июль", "select federal_district, sum(amount_rub) from {src} "
                  "where status = 'approved' group by 1"),
    ("один день", "select count(*), sum(amount_rub) from {src} "
                  "where txn_date = date '2026-07-15'"),
]
SOURCES = [("big", f"read_parquet('{my('big/july.parquet')}')"),
           ("small", f"read_parquet('{my('small/*/*/*.parquet')}', hive_partitioning = true)")]

print("\n| Запрос | Вариант | Получено | HEAD | GET | Секунды |")
print("|---|---|---|---|---|---|")
for qname, sql in QUERIES:
    for sname, src in SOURCES:
        con = duck()
        t = time.perf_counter()
        plan = con.execute("explain analyze " + sql.format(src=src)).fetchall()[0][1]
        s = http_stats(plan)
        print(f"| {qname} | {sname} | {s['in']} | {s['HEAD']} | {s['GET']} | "
              f"{time.perf_counter() - t:.2f} |")
print("\nЛистинг (LIST) в статистику DuckDB входит как GET.")
