#!/usr/bin/env bash
# Часть 5 (HDFS). Читатель: сколько файлов версии видно прямо сейчас.
# Запуск во втором терминале на node1: ./reader_hdfs.sh v2   (остановить: Ctrl+C)
# Опрашивает NameNode по WebHDFS (как в задании 1.3), а не клиентом hdfs:
# каждый запуск клиента — это JVM на пару секунд, а node1 у всего потока один.
V=${1:?укажите версию, например v2}
MART=/user/$USER/lab3/mart
NN=$(hdfs haadmin -getAllServiceState 2>/dev/null | awk '$2=="active"{split($1,a,":"); print a[1]}')
[ -n "$NN" ] || { echo "активный NameNode не найден"; exit 1; }
echo "опрашиваю $NN раз в секунду"
while true; do
  n=$(curl -s "http://$NN:50070/webhdfs/v1$MART/$V?op=GETCONTENTSUMMARY&user.name=$USER" \
      | grep -o '"fileCount":[0-9]*' | cut -d: -f2)
  if [ -n "$n" ]; then
    echo "$(date +%T) версия $V: файлов $n"
  else
    echo "$(date +%T) версия $V: каталога нет"
  fi
  sleep 1
done
