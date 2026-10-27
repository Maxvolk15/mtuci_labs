#!/usr/bin/env bash
# Часть 5 (HDFS). Публикация версии витрины: 10 файлов во временный каталог,
# затем ОДНО переименование. Запуск на node1: ./publish_hdfs.sh v2
# Каждая команда hdfs поднимает JVM (~2 с) — пауз добавлять не нужно.
set -euo pipefail
V=${1:?укажите версию, например v2}
MART=/user/$USER/lab3/mart
hdfs dfs -mkdir -p "$MART/_tmp_$V"
for i in $(seq -w 0 9); do
  echo "$V,part-$i" | hdfs dfs -put - "$MART/_tmp_$V/part-$i.csv"
  echo "записан part-$i"
done
hdfs dfs -mv "$MART/_tmp_$V" "$MART/$V"
echo "опубликовано: $MART/$V"
