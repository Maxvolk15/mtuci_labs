#!/usr/bin/env python3
"""Уборка: удалить из своего префикса всё, кроме txn_*.parquet (нужны в лабе 4).
Запуск: make clean-s3"""
from common import BUCKET, login, s3

c, me = s3(), login()
pages = c.get_paginator("list_objects_v2").paginate(Bucket=BUCKET, Prefix=f"{me}/")
doomed = [o["Key"] for p in pages for o in p.get("Contents", [])
          if not o["Key"].removeprefix(f"{me}/").startswith("txn_")]
for i in range(0, len(doomed), 1000):
    c.delete_objects(Bucket=BUCKET, Delete={"Objects": [{"Key": k} for k in doomed[i:i + 1000]]})
print(f"удалено объектов: {len(doomed)}")
left = c.list_objects_v2(Bucket=BUCKET, Prefix=f"{me}/").get("Contents", [])
print("осталось:", ", ".join(o["Key"].split("/")[-1] for o in left) or "ничего")
