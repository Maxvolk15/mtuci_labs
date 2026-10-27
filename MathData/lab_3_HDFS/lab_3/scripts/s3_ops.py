#!/usr/bin/env python3
"""Часть 2. Чего нет в договоре S3: каталоги, дозапись, переименование.

Готовые шаги выполните и прочитайте; три функции с TODO допишите.
Запуск: make ops            (все шаги по порядку)
        make ops STEP=rename (один шаг: dirs, append, rename, multipart, presign, neighbour)
"""
import pathlib
import sys
import time

from boto3.s3.transfer import TransferConfig
from botocore.exceptions import ClientError

from common import BUCKET, ROOT, login, s3

c, me = s3(), login()
P = f"{me}/ops"                                   # рабочий префикс этой части


def ls(prefix):
    """Все ключи с префиксом. LIST отдаёт страницами по 1000 — отсюда пагинатор."""
    pages = c.get_paginator("list_objects_v2").paginate(Bucket=BUCKET, Prefix=prefix)
    return [o["Key"] for page in pages for o in page.get("Contents", [])]


def step_dirs():
    print("— «каталог» в S3")
    print("  до записи:        ", ls(f"{P}/reports/"))
    c.put_object(Bucket=BUCKET, Key=f"{P}/reports/2026/q3.txt", Body=b"draft\n")
    print("  после PUT:        ", ls(f"{P}/reports/"))
    c.delete_object(Bucket=BUCKET, Key=f"{P}/reports/2026/q3.txt")
    print("  после DELETE:     ", ls(f"{P}/reports/"))
    # Вопрос 2.1: куда делся «каталог» reports/2026/ и существовал ли он вообще?


def append_line(key: str, line: bytes) -> int:
    """TODO 1. «Дописать» строку в конец объекта и вернуть, сколько байт
    пришлось передать по сети (туда и обратно). Операции append в S3 нет —
    реализуйте единственным возможным способом."""
    try:
        response = c.get_object(Bucket=BUCKET, Key=key)

        old_data = response['Body'].read()
        print(f"Получили {len(old_data)} байт из сети")
        
        new_data = old_data + line

        c.put_object(Bucket=BUCKET, Key=key, Body=new_data)
        print(f"Отправили {len(new_data)} байт в сеть")
    except Exception as e:
        print(e)

    return len(new_data) + len(old_data)

    # raise NotImplementedError("TODO 1")


def step_append():
    print("— дозапись")
    key = f"{P}/events.log"
    c.put_object(Bucket=BUCKET, Key=key, Body=b"event\n" * 100_000)   # ~600 КБ
    moved = append_line(key, b"one more event\n")
    size = c.head_object(Bucket=BUCKET, Key=key)["ContentLength"]
    print(f"  объект {size} байт; ради 15 байт передано {moved} байт")


def rename_prefix(src: str, dst: str) -> int:
    """TODO 2. «Переименовать каталог»: перенести все объекты с префиксом src
    под префикс dst. Вернуть число запросов к хранилищу, которые понадобились.
    Подсказка: copy_object + delete_object на каждый ключ; ls() тоже запрос."""
    keys = ls(src)
    requests = 1
    for old_key in keys:
        new_key = dst + old_key[len(src):]
        
        c.copy_object(
            Bucket=BUCKET,
            Key=new_key,
            CopySource={"Bucket": BUCKET, "Key": old_key}
        )
        requests += 1
        c.delete_object(Bucket=BUCKET, Key=old_key)
        requests += 1
    return requests
    # raise NotImplementedError("TODO 2")


def step_rename():
    print("— переименование префикса из 100 объектов")
    for i in range(100):
        c.put_object(Bucket=BUCKET, Key=f"{P}/mart_tmp/part-{i:03d}.txt", Body=b"x" * 1024)
    t = time.perf_counter()
    n = rename_prefix(f"{P}/mart_tmp/", f"{P}/mart/")
    print(f"  {n} запросов, {time.perf_counter() - t:.2f} с; "
          f"под новым префиксом {len(ls(f'{P}/mart/'))} объектов")
    # Сравните с `time hdfs dfs -mv` из части 1 и заполните таблицу 2.4.


def step_multipart():
    print("— составная загрузка")
    src = ROOT.parent / "lab_3" / "data" / "txn_july.parquet"         # ~11 МБ
    if not src.exists():
        sys.exit(f"  нет {src}: соберите лабу 2 (make avro) или укажите свой файл 10–20 МБ")
    cfg = TransferConfig(multipart_threshold=5 * 2**20, multipart_chunksize=5 * 2**20)
    c.upload_file(str(src), BUCKET, f"{P}/txn_july.parquet", Config=cfg)
    h = c.head_object(Bucket=BUCKET, Key=f"{P}/txn_july.parquet")
    print(f"  размер {h['ContentLength']} байт, ETag {h['ETag']}")
    # Вопрос 2.5: что означает суффикс после дефиса и почему ETag — не md5 файла?


def step_presign():
    print("— presigned URL")
    url = c.generate_presigned_url(
        "get_object", Params={"Bucket": BUCKET, "Key": f"{P}/events.log"}, ExpiresIn=300)
    print("  " + url)
    # Вопрос 2.6: откройте ссылку в браузере без ключей. Разберите параметры
    # X-Amz-*. Измените в ссылке один символ ключа объекта и объясните ответ.


def step_neighbour():
    """TODO 3. Попробуйте прочитать листинг чужого префикса и объект из него
    (логин соседа — аргументом). Поймайте ClientError и напечатайте код ошибки
    (e.response['Error']['Code']) для LIST и для GET."""
    raise NotImplementedError("TODO 3")


STEPS = {"dirs": step_dirs, "append": step_append, "rename": step_rename,
         "multipart": step_multipart, "presign": step_presign, "neighbour": step_neighbour}

if __name__ == "__main__":
    chosen = sys.argv[1:] or list(STEPS)
    for name in chosen:
        try:
            STEPS[name]()
        except NotImplementedError as e:
            print(f"  пропущено: {e} не заполнен")
