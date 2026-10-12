-- ============================================================================
-- Лаба 2. Сборка «широкой» таблицы операций txn_wide — подопытного для всех
-- замеров. ГОТОВЫЙ КОД: выполните целиком, менять ничего не нужно.
--
-- Это денормализованная витрина (One Big Table) по данным лабы 1: операция
-- процессинга + атрибуты клиента, продукта, мерчанта, региона, даты, сумма
-- в рублях. Очистка — та же, что в staging лабы 1 (дедуп, типизация,
-- нормализация значений). Итог: 2 312 606 строк × 28 колонок.
--
-- Путь к данным лабы 1 подставляется через параметр data_dir (см. Makefile).
-- ============================================================================

create or replace view src_clients as
with raw as (
    select * from read_csv(getvariable('data_dir') || '/abs/clients.csv',
                           delim=';', all_varchar=true)
)
select client_id,
       trim(regexp_replace(fio, ' +', ' '))                        as fio,
       case when lower(gender) in ('м', 'муж') or gender = 'M'
            then 'М' else 'Ж' end                                  as gender,
       case when birth_date like '%.%'
            then strptime(birth_date, '%d.%m.%Y')::date
            else birth_date::date end                              as birth_date,
       trim(replace(city, 'г. ', ''))                              as city,
       lower(segment)                                              as segment,
       registered_at::timestamp                                    as registered_at
from raw
qualify row_number() over (partition by client_id order by updated_at desc) = 1;

create or replace view src_accounts as
select account_id, client_id, product_code, product_name
from read_csv(getvariable('data_dir') || '/abs/accounts.csv', delim=';', all_varchar=true);

create or replace view src_cards as
select card_id, account_id, payment_system
from read_csv(getvariable('data_dir') || '/abs/cards.csv', delim=';', all_varchar=true);

create or replace view src_merchants as
select m.merchant_id, m.merchant_name, m.mcc as merchant_mcc,
       coalesce(c.category, 'Неизвестно') as category, m.home_city
from read_csv(getvariable('data_dir') || '/processing/merchants.csv', all_varchar=true) m
left join read_csv(getvariable('data_dir') || '/refs/mcc_codes.csv', all_varchar=true) c using (mcc);

create or replace view src_regions as
select * from read_csv(getvariable('data_dir') || '/refs/regions.csv');

create or replace view src_rates as
select date::date as rate_date, 'USD' as ccy, valutes.USD.value as rate
from read_json(getvariable('data_dir') || '/rates/cbr_rates.json')
union all
select date::date, 'EUR', valutes.EUR.value from read_json(getvariable('data_dir') || '/rates/cbr_rates.json')
union all
select date::date, 'CNY', valutes.CNY.value from read_json(getvariable('data_dir') || '/rates/cbr_rates.json');

create or replace view src_txn as
select * from read_parquet(getvariable('data_dir') || '/processing/transactions_*.parquet')
qualify row_number() over (partition by txn_id order by txn_ts) = 1;

create or replace table txn_wide as
select
    -- операция
    t.txn_id,
    t.txn_ts,
    t.txn_ts::date                                   as txn_date,
    t.channel,
    t.status,
    t.decline_reason,
    t.mcc,
    t.amount                                         as amount_orig,
    t.currency,
    round(t.amount * coalesce(r.rate, 1.0), 2)       as amount_rub,
    t.orig_txn_id,
    -- карта и продукт
    t.card_id,
    k.payment_system,
    a.account_id,
    a.product_code,
    a.product_name,
    -- клиент
    coalesce(c.client_id, 'UNKNOWN')                 as client_id,
    c.fio,
    c.gender,
    c.birth_date,
    c.segment,
    coalesce(rg.city, c.city)                        as city,
    coalesce(rg.region, 'Не определён')              as region,
    coalesce(rg.federal_district, 'Не определён')    as federal_district,
    -- мерчант
    case t.channel when 'atm' then 'ATM' when 'p2p' then 'P2P'
         else coalesce(m.merchant_id, 'UNKNOWN') end as merchant_id,
    case t.channel when 'atm' then 'Снятие наличных' when 'p2p' then 'Перевод СБП'
         else coalesce(m.merchant_name, 'Неизвестный мерчант') end as merchant_name,
    case t.channel when 'atm' then 'Наличные' when 'p2p' then 'Переводы'
         else coalesce(m.category, 'Неизвестно') end as category,
    -- служебное
    t.merchant_name_raw
from src_txn t
left join src_cards k      using (card_id)
left join src_accounts a   using (account_id)
left join src_clients c    on c.client_id = a.client_id
left join src_regions rg   on lower(rg.city) = lower(c.city)
left join src_merchants m  on m.merchant_id = t.merchant_id
asof left join src_rates r on r.ccy = t.currency and r.rate_date <= t.txn_ts::date
order by t.txn_ts, t.txn_id;
