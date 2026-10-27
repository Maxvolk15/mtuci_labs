# Лаба 3 «Переезд» — материалы преподавателя

Третья лабораторная сквозного проекта «Синица» (лекция 3 «Где лежат
данные»). Задание — `ЛАБА.md`, доступ к стенду — `ДОСТУП.md` (часть 0
из `ansible-cluster/docs/labs/lab1-hdfs.md`), эталонные тела TODO —
`../преподавателю/лаба_3_решения.py` (студентам не выдаётся, как и этот файл).

## Статус проверки

| Что | Состояние |
|---|---|
| `stage`, `check`, `s3_ops`, `bench_s3`, `http_log`, `small_files`, `publish`/`reader`, `q1`, решения TODO | прогнаны на локальном эмуляторе S3 (moto) с файлами лабы 2, DuckDB 1.5.5 |
| Байты и число GET в лекции и в ответах | сняты там же; от сервера не зависят — только от файла и версии DuckDB |
| `s3_login.py` (STS `AssumeRoleWithLDAPIdentity`) | **на стенде не проверен** — эмулятор этого вызова не знает; вызов взят из `ansible-cluster/docs/minio.md` |
| Политика с `${ldap:username}` | **на стенде не проверена** — эмулятор политик не применяет |
| `node1/*.sh`, часть 1 | **на стенде не проверены** (локально Hadoop нет); только `bash -n` |
| Секунды | на стенде будут другими: VPN идёт по TCP |

Первым делом на стенде: `make login && make check` под студенческой
учёткой. Если политика с переменной в этой сборке MinIO не работает —
запасной путь ниже.

## Что должно быть готово до выдачи

1. **Данные.** Девять файлов лабы 2 (`lab_2/data/txn*.parquet`, `txn.csv`)
   в HDFS `/datasets/sinitsa/` и пять Parquet-файлов из `scripts/stage.py`
   в бакете `datasets` под префиксом `sinitsa/`. Размеры сверяет `make check`.
   Проверить, что политика Ranger «чтение `/datasets` для студентов»
   пропускает `hdfs fsck` по `/datasets/sinitsa/txn.csv`.
2. **MinIO**: бакеты `students` (общая квота, предлагаю 300 ГиБ)
   и `datasets`; политика `student-rw`, привязанная к группе студентов
   FreeIPA. Роль `minio` сейчас умеет привязывать только встроенные
   политики — нужен шаг `mc admin policy create`. Текст политики:

   ```json
   { "Version": "2012-10-17", "Statement": [
     { "Effect": "Allow", "Action": ["s3:GetBucketLocation"],
       "Resource": ["arn:aws:s3:::students", "arn:aws:s3:::datasets"] },
     { "Effect": "Allow", "Action": ["s3:ListBucket"],
       "Resource": ["arn:aws:s3:::students"],
       "Condition": {"StringLike": {"s3:prefix": ["${ldap:username}/*"]}} },
     { "Effect": "Allow",
       "Action": ["s3:GetObject", "s3:PutObject", "s3:DeleteObject",
                  "s3:AbortMultipartUpload", "s3:ListMultipartUploadParts"],
       "Resource": ["arn:aws:s3:::students/${ldap:username}/*"] },
     { "Effect": "Allow", "Action": ["s3:GetObject", "s3:ListBucket"],
       "Resource": ["arn:aws:s3:::datasets", "arn:aws:s3:::datasets/*"] } ] }
   ```

   Запасной путь, если `${ldap:username}` не подставляется: политика
   на пользователя, которую создаёт `portal/provision_student.py`
   (`mc admin policy create` + `mc idp ldap policy attach --user`).
3. **Адрес хранилища.** По умолчанию `compute1.mtuci.cloud.ru:9000`
   (`S3_ENDPOINT` в `scripts/common.py`). Лучше — имя `s3.mtuci.cloud.ru`
   с четырьмя A-записями в DNS FreeIPA; тогда поменять одну строку.
4. **`/opt/lab3/venv` на `node1`** с `duckdb==1.5.5` и `boto3` — только
   для задания 3.5. Системный Python на узле — 3.9, под него `duckdb==1.5.5`
   нет; в репозитории SberLinux есть `python3.12`. Если поставить не
   получится, задание снимается, а цифру «с `node1`» показать на лекции.
5. Студенческий VPN и портал — как для практики по HDFS.
6. **Все три DataNode живы** (`hdfs haadmin`/Ambari, или JMX NameNode:
   `NumDeadDataNodes = 0`). При двух живых узлах из трёх `appendToFile`
   в задании 1.5 падает с «no more good datanodes», а `setrep -w 3`
   висит бесконечно — проверено на стенде 27.09.

Лаба не требует ни Prometheus, ни консоли MinIO, ни `mc` у студента.

## Нагрузка на стенд

- `node1`: только клиент `hdfs` и один лёгкий запрос DuckDB (3.5).
  Часть 5.1 — 10 запусков JVM на студента; при 30 студентах одновременно
  это заметно, но коротко.
- HDFS: на студента 235 МБ × 3 реплики + мелочь; квота дома 5 ГБ.
- MinIO: на студента ≈ 450 МБ (серверное копирование) + ≈ 25 МБ.
  На 100 студентов — 50 ГиБ из ~1000.
- VPN: загрузка ≈ 25 МБ, скачивание ≈ 150 МБ за всю работу.
  `txn_rg10k` в `make bench` — 1 700 мелких запросов; через TCP-VPN
  это минуты. Это и есть урок, но предупредите.

## Детерминизм

Байты и число GET в частях 3–4 зависят от файла и версии DuckDB
и у всех совпадают (эталон — в `../лекция_3_преподавателю.md`).
**`duckdb` не поднимать** — та же причина, что в лабе 2.

## Связь с соседними лабами

- **Лаба 2** → файлы, запросы Q0–Q4 и прогноз из `cost.sql`.
- **Лаба 4 (Spark)** → читает `txn_*.parquet` из префикса студента через
  `s3a://`; временные ключи STS подходят (`TemporaryAWSCredentialsProvider`).
- **Лаба 6 (Iceberg)** → часть 5: студент уже собрал файл-указатель
  и ответил, кто чистит старые версии и что делают два писателя.
