#!/usr/bin/env python3
"""
Часть 5. Arrow: формат данных В ПАМЯТИ и передача между движками без копий.

Parquet — как таблица лежит на диске. Arrow — как она лежит в оперативной
памяти, одинаково для DuckDB, Polars, pandas 2, Spark, DataFusion. Пока
такого стандарта не было, «передать таблицу из движка в Python» означало
сериализовать и разобрать её заново.

Запуск: python scripts/arrow_demo.py
"""
import pathlib
import time

import duckdb
import polars as pl

ROOT = pathlib.Path(__file__).resolve().parent.parent
con = duckdb.connect(str(ROOT / "formats.duckdb"), read_only=True)


def timed(label, fn):
    t = time.perf_counter()
    res = fn()
    print(f"  {label:55s} {time.perf_counter() - t:7.3f} с")
    return res


print("Путь 1 — через Arrow:")
tbl = timed("DuckDB → Arrow Table (.to_arrow_table())", lambda: con.sql("select * from txn_wide").to_arrow_table())
df = timed("Arrow → Polars (pl.from_arrow)", lambda: pl.from_arrow(tbl))
res = timed("Polars: group_by федеральный округ",
            lambda: df.group_by("federal_district").agg(pl.col("amount_rub").sum()))
back = timed("Polars DataFrame → снова запрос DuckDB (через Arrow)",
             lambda: con.sql("select count(*) from df where status = 'approved'").fetchall())

print("Путь 2 — через файл (так делали до Arrow):")
tmp_csv = ROOT / "data" / "_arrow_demo.csv"
timed("DuckDB → CSV на диск", lambda: con.execute(f"copy txn_wide to '{tmp_csv}' (header)"))
timed("CSV → Polars (read_csv)", lambda: pl.read_csv(tmp_csv))
try:
    tmp_csv.unlink()
except PermissionError:
    pass

# TODO 1. Добавьте путь 3: DuckDB → pandas (.df()) → Polars (pl.from_pandas).
#         pandas без pyarrow-типов хранит строки объектами Python — это копия
#         и конвертация. Сравните время с путём 1 и объясните.
print("Путь 3 — через pandas (с копированием):")
pdf = timed("DuckDB → pandas (.df())", lambda: con.sql("select * from txn_wide").df())
timed("pandas → Polars (pl.from_pandas)", lambda: pl.from_pandas(pdf))

# TODO 2. Посмотрите на tbl.schema. Найдите, как Arrow хранит txn_ts и fio
#         (тип, единицы времени). Сравните с parquet_schema() того же набора:
#         где Arrow и Parquet совпадают, а где различаются, и почему это
#         два разных формата, а не один.
print("Схема Arrow для выборочных колонок:")
print("txn_ts:", tbl.schema.field("txn_ts").type)
print("fio:", tbl.schema.field("fio").type)