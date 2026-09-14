-- ============================================================================
-- Слой витрины: ШАБЛОН. Выполняется после scripts/staging_template.sql.
-- Места, помеченные -- TODO, заполняете вы. Всё остальное — готовый код
-- и образцы: dim_date и dim_client сделаны за вас, остальное — по их образцу.
-- ============================================================================

create schema if not exists marts;

-- ────────────────────────────────────────────────────────────────────────────
-- dim_date — календарь. ГОТОВО, менять не нужно.
create or replace table marts.dim_date as
select cast(d as date)                                as date_actual,
       year(d) * 10000 + month(d) * 100 + day(d)      as date_sk,
       month(d)                                       as month,
       date_trunc('week', cast(d as date))            as week_start,
       isodow(d) in (6, 7)                            as is_weekend
from generate_series(date '2026-06-01', date '2026-08-31', interval 1 day) t(d);

-- ────────────────────────────────────────────────────────────────────────────
-- dim_client — ГОТОВО, это ваш ОБРАЗЕЦ. Разберите три приёма:
--   1) суррогатный ключ: row_number() нумерует строки — это и есть client_sk;
--   2) join со справочником по lower(city): чинит «МОСКВА»/«москва»,
--      канон図написание берём из справочника (coalesce);
--   3) последняя строка union all — «неизвестный клиент» с ключом -1:
--      на него потом сошлются операции, у которых карта не нашлась в АБС.
create or replace table marts.dim_client as
select row_number() over (order by c.client_id)       as client_sk,
       c.client_id, c.fio, c.gender, c.birth_date,
       coalesce(r.city, c.city)                       as city,
       coalesce(r.region, 'Не определён')             as region,
       coalesce(r.federal_district, 'Не определён')   as federal_district,
       c.segment
from staging.clients c
left join staging.regions r on lower(r.city) = lower(c.city)
union all
select -1, 'UNKNOWN', 'Неизвестный клиент', null, null, null,
       'Не определён', 'Не определён', 'unknown';

-- ────────────────────────────────────────────────────────────────────────────
-- dim_product — измерение «счёт/продукт». Сделайте по образцу dim_client:
-- суррогатный ключ product_sk + колонки account_id, client_id,
-- product_code, product_name + строка «неизвестный продукт» с ключом -1.
create or replace table marts.dim_product as
select row_number() over (order by account_id) as product_sk,
    account_id, 
    client_id,
    product_code, 
    product_name
    -- TODO: суррогатный ключ product_sk (row_number по account_id)
    -- TODO: account_id, client_id, product_code, product_name
from staging.accounts
union all
select -1, 'UNKNOWN', 'UNKNOWN', 'XX', 'Неизвестный продукт';

-- ────────────────────────────────────────────────────────────────────────────
-- dim_merchant — мерчанты + категория трат из справочника MCC.
-- Три служебные строки уже написаны: -1 для неизвестных мерчантов,
-- -2 и -3 — для операций БЕЗ мерчанта (снятие в банкомате и перевод):
-- так ни одна операция не потеряется и не получит NULL-ключ.
create or replace table marts.dim_merchant as
select
    row_number() over (order by m.merchant_id)        as merchant_sk,
    m.merchant_id, m.merchant_name,
    coalesce(mc.category, 'Неизвестно')               as category,
    -- TODO: категория трат из staging.mcc (join по mcc);
    --       если MCC в справочнике нет — 'Неизвестно' (coalesce)
    m.channel
from staging.merchants m
left join staging.mcc on mc.mcc = m.mcc
-- TODO: left join staging.mcc ...
union all select -1, 'UNKNOWN', 'Неизвестный мерчант', 'Неизвестно', null
union all select -2, 'ATM',     'Снятие наличных',     'Наличные',  'atm'
union all select -3, 'P2P',     'Перевод СБП',         'Переводы',  'p2p';

-- ────────────────────────────────────────────────────────────────────────────
-- fct_transactions — таблица фактов.
-- Каркас готов; ваши TODO — три решения, которые вы приняли в части 3
-- задания. Конвертация валют через ASOF JOIN уже написана: разберите её —
-- это ответ на вопрос про субботний курс.
create or replace table marts.fct_transactions as
select
    t.txn_id,
    d.date_sk,
    t.txn_ts,
    coalesce(dc.client_sk, -1)                          as client_sk,
    coalesce(dp.product_sk, -1)                         as product_sk,
    -- TODO: client_sk — из dc, но если join не нашёл клиента,
    --       операция должна попасть на «неизвестного» (ключ -1, coalesce)
    -- TODO: product_sk — так же
    case t.channel when 'atm' then -2
                   when 'p2p' then -3
                   else coalesce(dm.merchant_sk, -1) end as merchant_sk,
    t.channel,
    t.status,
    t.amount                                          as amount_orig,
    t.currency,
    -- курс: ПОСЛЕДНИЙ опубликованный не позже даты операции.
    -- asof join сам находит ближайшую прошлую дату — суббота получает
    -- пятничный курс. Для рублей курса нет (r.rate is null) → умножаем на 1
    round(t.amount * coalesce(r.rate, 1.0), 2)        as amount_rub
from staging.transactions t
join marts.dim_date d           on d.date_actual = t.txn_ts::date
left join staging.cards k       using (card_id)
left join staging.accounts a    using (account_id)
left join marts.dim_client dc   on dc.client_id  = a.client_id
left join marts.dim_product dp  on dp.account_id = k.account_id
left join marts.dim_merchant dm on dm.merchant_id = t.merchant_id
asof left join staging.rates r
     on r.ccy = t.currency and r.rate_date <= t.txn_ts::date;

-- ────────────────────────────────────────────────────────────────────────────
-- САМОПРОВЕРКА. Обе цифры должны сойтись у всех — данные одинаковые:
--   select count(*) from marts.fct_transactions;          -- 2 312 606
--   select count(*) from marts.fct_transactions
--    where client_sk = -1;                                -- 11 557
-- Первая не сошлась — дедупликация; вторая — потеряли сирот (нужен
-- left join + coalesce, а не inner).
