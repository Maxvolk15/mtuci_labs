#!/usr/bin/env python3
"""Часть 5. Публикация версии витрины из 20 файлов — с паузами, как у долгой задачи.

  python scripts/publish.py naive  v2   — писать файлы прямо в mart/v2/
  python scripts/publish.py atomic v3   — TODO: так, чтобы читатель не видел полуготового

Во втором терминале в это время работает scripts/reader.py.
"""
import sys
import time

from common import BUCKET, login, s3

c, me = s3(), login()
MART = f"{me}/mart"
N, PAUSE = 20, 1.0


def part(version: str, i: int) -> bytes:
    return f"{version},part-{i:02d},{1000 + i}\n".encode()


def publish_naive(version: str):
    for i in range(N):
        c.put_object(Bucket=BUCKET, Key=f"{MART}/{version}/part-{i:02d}.csv", Body=part(version, i))
        print(f"  записан part-{i:02d}")
        time.sleep(PAUSE)


def publish_atomic(version: str):
    """TODO. Опубликовать версию так, чтобы читатель в любой момент видел
    либо прежнюю версию целиком, либо новую целиком. Переименования нет.
    Что в S3 происходит «разом»? Запись одного объекта. Значит, читателю
    нужен один маленький объект, который говорит, какая версия текущая, —
    например {MART}/_current. Парная функция — read_current() в reader.py."""
    raise NotImplementedError("TODO: publish_atomic")


if __name__ == "__main__":
    mode, version = sys.argv[1], sys.argv[2]
    {"naive": publish_naive, "atomic": publish_atomic}[mode](version)
    print("публикация завершена")
