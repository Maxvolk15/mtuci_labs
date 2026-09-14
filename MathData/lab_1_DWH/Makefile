VENV    := .venv
PYTHON  := $(VENV)/bin/python

.PHONY: install data db ui check clean

install:
	python3 -m venv $(VENV)
	$(PYTHON) -m pip install -q -r requirements.txt

data:
	$(PYTHON) generator/generate.py

db:
	$(PYTHON) -c "import duckdb,pathlib; con=duckdb.connect('bank.duckdb'); con.execute(pathlib.Path('scripts/raw_views.sql').read_text()); print('bank.duckdb готова: схема raw, 9 представлений-источников')"

ui:
	@$(PYTHON) -c "import duckdb,time,signal,sys; signal.signal(signal.SIGINT, lambda *a: (print('\nUI остановлен'), sys.exit(0))); con=duckdb.connect('bank.duckdb'); con.sql('call start_ui()'); print('UI запущен: http://localhost:4213 (остановить: Ctrl+C)'); time.sleep(10**9)"

check:
	$(PYTHON) scripts/check.py

clean:
	rm -rf data bank.duckdb
