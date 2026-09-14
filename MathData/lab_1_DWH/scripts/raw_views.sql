-- Представления поверх сырых файлов. Создаются командой `make db`
-- в базе bank.duckdb, чтобы все источники были видны в UI как таблицы.
-- Это НЕ очистка данных: view отдаёт файлы как есть.

create schema if not exists raw;

create or replace view raw.clients as
select * from read_csv('data/abs/clients.csv', delim=';', all_varchar=true);

create or replace view raw.accounts as
select * from read_csv('data/abs/accounts.csv', delim=';');

create or replace view raw.cards as
select * from read_csv('data/abs/cards.csv', delim=';');

create or replace view raw.transactions as
select * from read_parquet('data/processing/transactions_*.parquet');

create or replace view raw.merchants as
select * from read_csv('data/processing/merchants.csv');

create or replace view raw.mcc_codes as
select * from read_csv('data/refs/mcc_codes.csv', all_varchar=true);

create or replace view raw.regions as
select * from read_csv('data/refs/regions.csv');

create or replace view raw.rates as
select * from read_json('data/rates/cbr_rates.json');

create or replace view raw.app_events as
select * from read_json('data/applog/app_events_*.jsonl');
