#!/usr/bin/env python3
"""Часть 5. Читатель: раз в секунду смотрит на витрину и печатает, что видит.

  python scripts/reader.py naive v2   — листинг mart/v2/ и сумма по файлам
  python scripts/reader.py atomic     — TODO: сначала узнать текущую версию

Остановить: Ctrl+C. Контрольная сумма полной версии из 20 файлов — 20190.
"""
import sys
import time

from botocore.exceptions import ClientError

from common import BUCKET, login, s3

c, me = s3(), login()
MART = f"{me}/mart"


def read_version(version: str):
    keys = [o["Key"] for o in c.list_objects_v2(
        Bucket=BUCKET, Prefix=f"{MART}/{version}/").get("Contents", [])]
    total = 0
    for k in keys:
        line = c.get_object(Bucket=BUCKET, Key=k)["Body"].read().decode()
        total += int(line.strip().split(",")[2])
    return len(keys), total


def read_current():
    """TODO. Вернуть имя текущей версии из объекта-указателя
    (или None, если указателя ещё нет)."""
    raise NotImplementedError("TODO: read_current")


if __name__ == "__main__":
    mode = sys.argv[1]
    while True:
        version = sys.argv[2] if mode == "naive" else read_current()
        if version is None:
            print(time.strftime("%H:%M:%S"), "витрина ещё не опубликована")
        else:
            n, total = read_version(version)
            verdict = "полная" if (n, total) == (20, 20190) else "ПОЛУГОТОВАЯ"
            print(time.strftime("%H:%M:%S"), f"версия {version}: файлов {n:2d}, сумма {total:6d} — {verdict}")
        time.sleep(1)
