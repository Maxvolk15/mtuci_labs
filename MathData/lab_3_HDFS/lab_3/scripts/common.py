"""Общее для скриптов лабы 3: адрес хранилища, логин, клиенты boto3 и DuckDB.

Ключи берутся из профиля [stand] файла ~/.aws/credentials — его пишет
make login. В коде и в отчёте ключей быть не должно.
"""
import configparser
import os
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
ENDPOINT = os.environ.get("S3_ENDPOINT", "compute1.mtuci.cloud.ru:9000")
PROFILE = "stand"
BUCKET = "students"            # общий бакет, у каждого свой префикс <логин>/
DATASETS = "datasets"          # общие данные, только чтение
SINITSA = "sinitsa"            # префикс файлов лабы 2 в бакете datasets
# Хранилище стенда доступно только напрямую через VPN. Системный или
# корпоративный прокси (HTTP_PROXY) до него не дотянется — исключаем адрес.
_host = ENDPOINT.split(":")[0]
for _var in ("NO_PROXY", "no_proxy"):
    os.environ[_var] = ",".join(filter(None, [os.environ.get(_var), _host, ".mtuci.cloud.ru"]))

CREDENTIALS = pathlib.Path(os.environ.get(
    "AWS_SHARED_CREDENTIALS_FILE", pathlib.Path.home() / ".aws" / "credentials"))


def login() -> str:
    f = ROOT / ".stand_login"
    name = os.environ.get("STAND_LOGIN") or (f.read_text().strip() if f.exists() else "")
    if not name:
        sys.exit("Логин неизвестен: выполните make login")
    return name


def keys() -> dict:
    cfg = configparser.ConfigParser()
    cfg.read(CREDENTIALS)
    if PROFILE not in cfg:
        sys.exit(f"В {CREDENTIALS} нет профиля [{PROFILE}]: выполните make login")
    return dict(cfg[PROFILE])


def s3():
    import boto3
    from botocore.config import Config
    k = keys()
    return boto3.client(
        "s3", endpoint_url=f"http://{ENDPOINT}", region_name="us-east-1",
        aws_access_key_id=k["aws_access_key_id"],
        aws_secret_access_key=k["aws_secret_access_key"],
        aws_session_token=k.get("aws_session_token"),
        config=Config(signature_version="s3v4", s3={"addressing_style": "path"},
                      request_checksum_calculation="when_required",
                      response_checksum_validation="when_required"))


def duck():
    """Новое соединение DuckDB с секретом S3. Кеш файлов выключен, чтобы
    каждый запрос честно ходил в хранилище и замеры не зависели от порядка."""
    import duckdb
    k = keys()
    con = duckdb.connect()
    con.execute("install httpfs; load httpfs")
    token = k.get("aws_session_token")
    con.execute(
        "create secret stand (type s3, key_id ?, secret ?, "
        + ("session_token ?, " if token else "")
        + "endpoint ?, url_style 'path', use_ssl false, region 'us-east-1')",
        [k["aws_access_key_id"], k["aws_secret_access_key"]]
        + ([token] if token else []) + [ENDPOINT])
    con.execute("set http_proxy = ''")                 # см. NO_PROXY выше
    con.execute("set enable_external_file_cache = false")
    con.execute("set threads = 4")
    return con


def http_stats(plan: str) -> dict:
    """Вытащить блок HTTPFS HTTP Stats из текста explain analyze."""
    import re
    out = {"in": "0 bytes", "HEAD": 0, "GET": 0, "PUT": 0}
    m = re.search(r"in: ([^│]+?)\s*│", plan)
    if m:
        out["in"] = m.group(1)
    for verb in ("HEAD", "GET", "PUT"):
        m = re.search(rf"#{verb}: (\d+)", plan)
        if m:
            out[verb] = int(m.group(1))
    return out


def my(path: str = "") -> str:
    return f"s3://{BUCKET}/{login()}/{path}"
