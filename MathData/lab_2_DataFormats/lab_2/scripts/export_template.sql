-- ============================================================================
-- Часть 1. Один и тот же набор данных — в разных форматах. ШАБЛОН.
--
-- Источник — таблица txn_wide (2 312 606 строк × 28 колонок) в formats.duckdb.
-- Первые четыре COPY даны как образец, остальные — TODO по образцу.
-- Все файлы пишутся в data/. Выполнить: make export
-- ============================================================================

-- Образец 1. CSV с заголовком — «формат по умолчанию» половины интеграций.
copy txn_wide to 'data/txn.csv' (format csv, header);

-- Образец 2. Parquet без сжатия: чистый эффект колоночной раскладки и кодировок.
copy txn_wide to 'data/txn_none.parquet' (format parquet, compression uncompressed);

-- Образец 3. Parquet + zstd — то, что стоит писать по умолчанию в 2026.
copy txn_wide to 'data/txn_zstd.parquet' (format parquet, compression zstd);

-- Образец 4. Тот же Parquet, но строки перемешаны: min/max по дате в каждой
-- row group растянется на всё лето. Нужен для части 4 (pushdown).
copy (select * from txn_wide order by hash(txn_id))
  to 'data/txn_shuffled.parquet' (format parquet, compression zstd);

-- TODO 1. Parquet + snappy (компромисс «быстро сжать» из эпохи Hadoop).
--         Имя файла: data/txn_snappy.parquet
copy txn_wide to 'data/txn_snappy.parquet' (format parquet, compression snappy);

-- TODO 2. CSV, сжатый gzip: data/txn.csv.gz  (опция compression gzip).
--         Обратите внимание на время записи — и запомните его до части 3.
copy txn_wide to 'data/txn.csv.gz' (format csv, header, compression gzip);

-- TODO 3. Parquet + zstd, отсортированный по merchant_id, txn_ts:
--         data/txn_by_merchant.parquet. Нужен для части 4 (bloom-фильтр).
copy (select * from txn_wide order by merchant_id, txn_ts)
  to 'data/txn_by_merchant.parquet' (format parquet, compression zstd);

-- TODO 4. Parquet + zstd с маленькими row group (row_group_size 10000):
--         data/txn_rg10k.parquet — и с большими (1000000): data/txn_rg1m.parquet.
copy txn_wide to 'data/txn_rg10k.parquet' (format parquet, compression zstd, row_group_size 10000);
copy txn_wide to 'data/txn_rg1m.parquet' (format parquet, compression zstd, row_group_size 1000000);

-- ⭐ Бонус (если есть 2 ГБ на диске): JSON Lines — формат логов приложения.
-- copy txn_wide to 'data/txn.jsonl' (format json);
copy txn_wide to 'data/txn.jsonl' (format json);