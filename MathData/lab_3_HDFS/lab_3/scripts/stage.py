#!/usr/bin/env python3
"""Часть 2. Скопировать файлы «Синицы» из общего бакета в свой префикс.

Копирование серверное (CopyObject): данные идут внутри хранилища,
через ваш VPN проходит только запрос и ответ. Сравните время с тем,
сколько вы качали бы эти 450 МБ по сети.
Запуск: make stage
"""
import time

from common import BUCKET, DATASETS, SINITSA, login, s3

FILES = ["txn_zstd.parquet", "txn_shuffled.parquet", "txn_by_merchant.parquet",
         "txn_rg10k.parquet", "txn_rg1m.parquet"]

c, me = s3(), login()
for name in FILES:
    t = time.perf_counter()
    c.copy_object(Bucket=BUCKET, Key=f"{me}/{name}",
                  CopySource={"Bucket": DATASETS, "Key": f"{SINITSA}/{name}"})
    size = c.head_object(Bucket=BUCKET, Key=f"{me}/{name}")["ContentLength"]
    print(f"{name:28s} {size / 1e6:7.1f} МБ  {time.perf_counter() - t:5.2f} с")
