#!/usr/bin/env python3
"""Самопроверка лабы 3: окружение, ключи, доступ к бакетам, файлы в своём префиксе.
Запуск: make check"""
import duckdb
from botocore.exceptions import ClientError

from common import BUCKET, DATASETS, ENDPOINT, SINITSA, login, s3

failures = []


def check(name, ok, detail=""):
    print(f"  {'ok ' if ok else 'FAIL'}  {name} {detail}")
    if not ok:
        failures.append(name)


print("Окружение:")
check("duckdb == 1.5.5", duckdb.__version__ == "1.5.5", duckdb.__version__)
me = login()
print(f"Хранилище {ENDPOINT}, логин {me}:")
c = s3()
try:
    n = c.list_objects_v2(Bucket=DATASETS, Prefix=f"{SINITSA}/").get("KeyCount", 0)
    check(f"чтение {DATASETS}/{SINITSA}/", n > 0, f"объектов: {n}")
except ClientError as e:
    check(f"чтение {DATASETS}/{SINITSA}/", False, e.response["Error"]["Code"]
          + " — ключи истекли? make login")
try:
    c.put_object(Bucket=BUCKET, Key=f"{me}/.check", Body=b"ok")
    c.delete_object(Bucket=BUCKET, Key=f"{me}/.check")
    check(f"запись в {BUCKET}/{me}/", True)
except ClientError as e:
    check(f"запись в {BUCKET}/{me}/", False, e.response["Error"]["Code"])
try:
    c.put_object(Bucket=DATASETS, Key="should-fail", Body=b"x")
    c.delete_object(Bucket=DATASETS, Key="should-fail")
    check(f"запись в {DATASETS} запрещена", False, "записалось — сообщите преподавателю")
except ClientError:
    check(f"запись в {DATASETS} запрещена", True)

staged = {o["Key"].split("/")[-1]: o["Size"] for o in c.list_objects_v2(
    Bucket=BUCKET, Prefix=f"{me}/txn_").get("Contents", [])}
EXPECTED = {"txn_zstd.parquet": 89717699, "txn_shuffled.parquet": 101211676,
            "txn_by_merchant.parquet": 61475586, "txn_rg10k.parquet": 111804268,
            "txn_rg1m.parquet": 83693418}
print("Файлы в своём префиксе (после make stage):")
for name, size in EXPECTED.items():
    check(name, staged.get(name) == size, str(staged.get(name, "нет")))

print("\nВсе проверки пройдены" if not failures else f"\nНе пройдено: {len(failures)}")
