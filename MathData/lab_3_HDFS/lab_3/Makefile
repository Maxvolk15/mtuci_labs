VENV    := .venv
PYTHON  := $(VENV)/bin/python
FILE    ?= txn_zstd.parquet
Q       ?= select count(*) from {src}
STEP    ?=

.PHONY: install login check stage ops bench httplog small publish reader clean-s3

install:
	python3 -m venv $(VENV)
	$(PYTHON) -m pip install -q -r requirements.txt

# часть 0: временные ключи S3 по доменному паролю (12 часов)
login:
	$(PYTHON) scripts/s3_login.py

check:
	$(PYTHON) scripts/check.py

# часть 2: серверное копирование файлов «Синицы» в свой префикс
stage:
	$(PYTHON) scripts/stage.py

# часть 2: make ops  или  make ops STEP=rename
ops:
	$(PYTHON) scripts/s3_ops.py $(STEP)

# часть 3: байты, запросы и секунды для Q0–Q4
bench:
	$(PYTHON) scripts/bench_s3.py

# часть 3: make httplog FILE=txn_zstd.parquet Q="select count(*) from {src}"
httplog:
	$(PYTHON) scripts/http_log.py $(FILE) "$(Q)"

# часть 4: один файл против сотен мелких
small:
	$(PYTHON) scripts/small_files.py

# уборка в хранилище; txn_*.parquet остаются для лабы 4
clean-s3:
	$(PYTHON) scripts/clean.py
