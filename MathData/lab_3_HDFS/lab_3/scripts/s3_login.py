#!/usr/bin/env python3
"""Часть 0. Получить временные ключи S3 по доменному паролю (служба STS).

Пароль спрашивается без эха и никуда не сохраняется. Ключи действуют
12 часов и пишутся в профиль [stand] файла ~/.aws/credentials (права 600).
Только стандартная библиотека — работает и на ноутбуке, и на node1.
Запуск: make login
"""
import configparser
import getpass
import os
import pathlib
import sys
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from common import CREDENTIALS, ENDPOINT, PROFILE, ROOT  # noqa: E402

user = input("Логин на стенде: ").strip().lower()
password = getpass.getpass("Пароль (не отображается): ")

form = urllib.parse.urlencode({
    "Action": "AssumeRoleWithLDAPIdentity", "Version": "2011-06-15",
    "LDAPUsername": user, "LDAPPassword": password,
    "DurationSeconds": 12 * 3600}).encode()
try:
    with urllib.request.urlopen(f"http://{ENDPOINT}", data=form, timeout=15) as r:
        body = r.read()
except urllib.error.HTTPError as e:
    sys.exit(f"Отказ STS ({e.code}): неверный пароль или нет политики для группы.\n"
             + e.read().decode(errors="replace")[:300])
except OSError as e:
    sys.exit(f"Хранилище {ENDPOINT} недоступно — VPN поднят? ({e})")

# ответ — XML с пространством имён; ищем элементы по локальному имени
found = {el.tag.split("}")[-1]: el.text for el in ET.fromstring(body).iter()}
cfg = configparser.ConfigParser()
cfg.read(CREDENTIALS)
cfg[PROFILE] = {
    "aws_access_key_id": found["AccessKeyId"],
    "aws_secret_access_key": found["SecretAccessKey"],
    "aws_session_token": found["SessionToken"]}
CREDENTIALS.parent.mkdir(mode=0o700, exist_ok=True)
with open(os.open(CREDENTIALS, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600), "w") as f:
    cfg.write(f)
(ROOT / ".stand_login").write_text(user)
print(f"Ключи записаны в {CREDENTIALS}, профиль [{PROFILE}]; действуют до {found.get('Expiration')}")
