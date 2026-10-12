VENV    := .venv
PYTHON  := $(VENV)/bin/python
DATA_DIR ?= ../lab_1/data
FILE    ?= data/txn_zstd.parquet

.PHONY: install data build export bench cost avro orc arrow check clean ui

install:
	python3 -m venv $(VENV)
	$(PYTHON) -m pip install -q -r requirements.txt

# данные лабы 1 (если их ещё нет): генератор детерминирован, ~10 сек
data:
	$(PYTHON) ../lab_1/generator/generate.py --out $(DATA_DIR)

# собрать широкую таблицу txn_wide в formats.duckdb
build:
	$(PYTHON) scripts/run_sql.py scripts/build_wide.sql $(DATA_DIR)

# часть 1: выгрузить txn_wide во все форматы (заполните TODO в шаблоне)
export:
	@mkdir -p data
	$(PYTHON) scripts/run_sql.py scripts/export_template.sql $(DATA_DIR)

# часть 3: один набор запросов ко всем файлам data/
bench:
	$(PYTHON) scripts/bench.py

# часть 4: цена запроса из метаданных; make cost FILE=data/txn_shuffled.parquet
cost:
	$(PYTHON) scripts/cost.py $(FILE)

avro:
	$(PYTHON) scripts/avro_evolution.py $(DATA_DIR)

orc:
	$(PYTHON) scripts/orc_export.py

arrow:
	$(PYTHON) scripts/arrow_demo.py

check:
	$(PYTHON) scripts/check.py

# DuckDB UI над formats.duckdb (как make ui в лабе 1); закрыть перед другими make-командами
ui:
	@$(PYTHON) -c "import duckdb,time,signal,sys; signal.signal(signal.SIGINT, lambda *a: (print('\nUI остановлен'), sys.exit(0))); con=duckdb.connect('formats.duckdb'); con.sql('call start_ui()'); print('UI запущен: http://localhost:4213 (остановить: Ctrl+C)'); time.sleep(10**9)"

clean:
	rm -rf data formats.duckdb
