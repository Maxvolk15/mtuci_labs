-- ============================================================================
-- Слой staging: приводим источники в порядок. ШАБЛОН.
--
-- Две таблицы разобраны полностью как образец: clients (самый грязный
-- источник, все приёмы очистки) и rates (разбор JSON). Их нужно выполнить
-- и ПРОЧИТАТЬ: каждая конструкция чинит конкретный дефект из вашего
-- чек-листа (часть 2 задания).
--
-- Остальные таблицы — TODO: в комментарии над каждой написано, какая
-- в ней неувязка; чините по образцам из clients. Пока TODO не заполнены,
-- самопроверка в части 4 не сойдётся.
--
-- Правило слоя: только типизация, нормализация значений и дедупликация.
-- Бизнес-решений (что считать оборотом, куда девать отказы) здесь НЕТ.
-- ============================================================================

create schema if not exists staging;

-- Справочники читаем как есть — они чистые.
create or replace view staging.regions as
select * from read_csv('data/refs/regions.csv');

create or replace view staging.mcc as
select * from read_csv('data/refs/mcc_codes.csv', all_varchar=true);

create or replace view staging.merchants as
select * from read_csv('data/processing/merchants.csv', all_varchar=true);

-- ----------------------------------------------------------------------------
-- ОБРАЗЕЦ 1. Клиенты: самый грязный источник — здесь собраны все приёмы.
-- Неувязки: пробелы в ФИО; 8 написаний пола (2.1); два формата дат (2.2);
-- приставка «г. » в городе; регистр сегмента (2.1); полные дубли (2.3).
-- ----------------------------------------------------------------------------
create or replace view staging.clients as
with raw as (
    -- all_varchar: не даём DuckDB угадывать типы — колонку дат с двумя
    -- форматами он всё равно прочитал бы как текст, но молча
    select * from read_csv('data/abs/clients.csv', delim=';', all_varchar=true)
),
typed as (
    select
        client_id,
        trim(regexp_replace(fio, ' +', ' '))                    as fio,
        -- пол: 8 вариантов написания приводим к двум
        case when lower(gender) in ('м', 'муж') or gender = 'M'
             then 'М' else 'Ж' end                              as gender,
        -- дата рождения: в колонке два формата, разбираем оба явно
        case when birth_date like '%.%'
             then strptime(birth_date, '%d.%m.%Y')::date
             else birth_date::date end                          as birth_date,
        -- город: срезаем приставку «г. »; регистр починим в витрине
        -- по справочнику регионов
        trim(replace(city, 'г. ', ''))                          as city,
        lower(segment)                                          as segment,
        registered_at::timestamp                                as registered_at,
        updated_at::timestamp                                   as updated_at
    from raw
)
select * from typed
-- полные дубли схлопываем по ключу: из одинаковых строк остаётся одна.
-- «Почти дубли» (другой client_id) НЕ трогаем — см. вопрос В-Д в задании
qualify row_number() over (partition by client_id order by updated_at desc) = 1;

-- ----------------------------------------------------------------------------
-- TODO 1. Счета: источник чистый, но CSV с разделителем ';' читается
-- текстом — единственная неувязка в том, что opened_at остаётся строкой.
-- Приведите её к date (образец — registered_at в clients).
-- ----------------------------------------------------------------------------
create or replace view staging.accounts as
select account_id, client_id, product_code, product_name,
       opened_at::date as opened_at,   -- TODO: тип date
       status
from read_csv('data/abs/accounts.csv', delim=';', all_varchar=true);

-- ----------------------------------------------------------------------------
-- TODO 2. Карты: та же неувязка, что в accounts, — issued_at строкой.
-- ----------------------------------------------------------------------------
create or replace view staging.cards as
select card_id, account_id, payment_system,
       issued_at::date as issued_at,   -- TODO: тип date
       status
from read_csv('data/abs/cards.csv', delim=';', all_varchar=true);

-- ----------------------------------------------------------------------------
-- TODO 3. Транзакции: повторная доставка из процессинга дала полные
-- дубли строк с тем же txn_id — это ваш пункт 2.4, и чинится он здесь.
-- Оставьте одну строку на txn_id — приём qualify row_number() из
-- образца clients (в order by подойдёт txn_ts).
-- ----------------------------------------------------------------------------
create or replace view staging.transactions as
select * from read_parquet('data/processing/transactions_*.parquet')
qualify row_number() over (partition by txn_id order by txn_ts desc) = 1;
-- TODO: дедупликация по txn_id
;

-- ----------------------------------------------------------------------------
-- ОБРАЗЕЦ 2. Курсы ЦБ: json → «длинная» таблица (дата, валюта, курс).
-- Обратите внимание: дат-выходных здесь НЕТ (пункт 2.6) — и это чинит
-- не staging, а витрина протяжкой курса (asof join, см. шаблон marts).
-- ----------------------------------------------------------------------------
create or replace view staging.rates as
select date::date as rate_date, 'USD' as ccy, valutes.USD.value as rate
from read_json('data/rates/cbr_rates.json')
union all
select date::date, 'EUR', valutes.EUR.value from read_json('data/rates/cbr_rates.json')
union all
select date::date, 'CNY', valutes.CNY.value from read_json('data/rates/cbr_rates.json');
