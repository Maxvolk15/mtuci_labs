-- ============================================================================
-- Часть 4. Цена запроса из метаданных Parquet. ШАБЛОН.
--
-- Идея: движок читает не файл, а нужные колонки нужных row group.
-- Значит стоимость запроса в байтах можно посчитать, не выполняя его:
--   1) по min/max колонки фильтра отобрать row group, которые могут
--      содержать искомые строки;
--   2) сложить total_compressed_size колонок запроса в этих row group.
-- Именно за эти байты выставляет счёт облачное хранилище (лекция 3).
--
-- Запуск: make cost FILE=data/txn_zstd.parquet
-- Переменная f подставляется Makefile'ом.
-- ============================================================================

-- Образец: Q2 — select count(*), sum(amount_rub) ... where txn_date = '2026-07-15'
with needed_rg as (
    select row_group_id
    from parquet_metadata(getvariable('f'))
    where path_in_schema = 'txn_date'
      and stats_min::date <= date '2026-07-15'
      and stats_max::date >= date '2026-07-15'
),
file_total as (
    select sum(total_compressed_size) as bytes,
           count(distinct row_group_id) as row_groups
    from parquet_metadata(getvariable('f'))
)
select 'Q2 фильтр по дате'                              as query,
       (select count(*) from needed_rg)                  as row_groups_needed,
       (select row_groups from file_total)               as row_groups_total,
       round(sum(m.total_compressed_size) / 1e6, 2)      as mb_needed,
       round((select bytes from file_total) / 1e6, 1)    as mb_file,
       round(100.0 * sum(m.total_compressed_size)
             / (select bytes from file_total), 2)        as pct
from parquet_metadata(getvariable('f')) m
join needed_rg using (row_group_id)
where path_in_schema in ('txn_date', 'amount_rub');

-- TODO 1. Q1 — select federal_district, sum(amount_rub) ... where status='approved'
--         group by 1. Фильтр по status не отсекает ни одной row group
--         (почему? посмотрите stats_min/stats_max колонки status), значит
--         row group нужны все, а колонок — три. Посчитайте mb_needed и pct.
with needed_rg as (
    select distinct row_group_id
    from parquet_metadata(getvariable('f'))
),
file_total as (
    select sum(total_compressed_size) as bytes,
           count(distinct row_group_id) as row_groups
    from parquet_metadata(getvariable('f'))
)
select 'Q1 агрегат по статусу'                      as query,
       (select count(*) from needed_rg)               as row_groups_needed,
       (select row_groups from file_total)            as row_groups_total,
       round(sum(m.total_compressed_size) / 1e6, 2)     as mb_needed,
       round((select bytes from file_total) / 1e6, 1)   as mb_file,
       round(100.0 * sum(m.total_compressed_size)
             / (select bytes from file_total), 2)       as pct
from parquet_metadata(getvariable('f')) m
join needed_rg using (row_group_id)
where path_in_schema in ('status', 'federal_district', 'amount_rub');

-- TODO 2. Q3 — ... where merchant_id = 'M3300'. Здесь min/max бесполезны
--         (проверьте), зато есть bloom-фильтр:
--           select * from parquet_bloom_probe(getvariable('f'), 'merchant_id', 'M3300');
--         Оставьте row group, где bloom_filter_excludes = false, и посчитайте
--         байты колонок merchant_id и amount_rub.
with needed_rg as (
    select row_group_id
    from parquet_bloom_probe(getvariable('f'), 'merchant_id', 'M3300')
    where bloom_filter_excludes = false  -- оставляем те блоки, где значение РЕАЛЬНО может быть
),
file_total as (
    select sum(total_compressed_size) as bytes,
           count(distinct row_group_id) as row_groups
    from parquet_metadata(getvariable('f'))
)
select 'Q3 редкий мерчант (bloom)'                   as query,
       (select count(*) from needed_rg)               as row_groups_needed,
       (select row_groups from file_total)            as row_groups_total,
       round(sum(m.total_compressed_size) / 1e6, 2)     as mb_needed,
       round((select bytes from file_total) / 1e6, 1)   as mb_file,
       round(100.0 * sum(m.total_compressed_size)
             / (select bytes from file_total), 2)       as pct
from parquet_metadata(getvariable('f')) m
join needed_rg using (row_group_id)
where path_in_schema in ('merchant_id', 'amount_rub');
