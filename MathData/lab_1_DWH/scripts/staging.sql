-- ============================================================================
-- Слой staging: приводим источники в порядок. ГОТОВЫЙ КОД — выполните его
-- целиком и ПРОЧИТАЙТЕ: каждая конструкция здесь чинит конкретный дефект
-- из вашего чек-листа (часть 2 задания). Менять ничего не нужно.
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

-- Клиенты: самый грязный источник.
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

create or replace view staging.accounts as
select account_id, client_id, product_code, product_name,
       opened_at::date  as opened_at, status
from read_csv('data/abs/accounts.csv', delim=';', all_varchar=true);

create or replace view staging.cards as
select card_id, account_id, payment_system,
       issued_at::date as issued_at, status
from read_csv('data/abs/cards.csv', delim=';', all_varchar=true);

-- Транзакции: повторная доставка из процессинга даёт полные дубли строк
-- с тем же txn_id — дедуплицируем по бизнес-ключу прямо на входе.
create or replace view staging.transactions as
select * from read_parquet('data/processing/transactions_*.parquet')
qualify row_number() over (partition by txn_id order by txn_ts) = 1;

-- Курсы ЦБ: json → «длинная» таблица (дата, валюта, курс).
-- Обратите внимание: дат-выходных здесь НЕТ — протяжку курса
-- делает витрина (asof join, см. шаблон marts).
create or replace view staging.rates as
select date::date as rate_date, 'USD' as ccy, valutes.USD.value as rate
from read_json('data/rates/cbr_rates.json')
union all
select date::date, 'EUR', valutes.EUR.value from read_json('data/rates/cbr_rates.json')
union all
select date::date, 'CNY', valutes.CNY.value from read_json('data/rates/cbr_rates.json');
