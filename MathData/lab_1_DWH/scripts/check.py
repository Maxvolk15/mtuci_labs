#!/usr/bin/env python3
"""
Проверка сгенерированного датасета: все ли дефекты на месте и в ожидаемых долях.
Запускать после `make data`. Каждая строка — свойство данных, на которое
опирается задание; если проверка упала, лабу выдавать нельзя.
"""
import pathlib
import sys

import duckdb

D = pathlib.Path(__file__).resolve().parent.parent / "data"
con = duckdb.connect()
failures = []


def check(name, sql, lo, hi):
    val = con.execute(sql).fetchone()[0]
    ok = lo <= val <= hi
    print(f"  {'ok ' if ok else 'FAIL'}  {name}: {val}  (ожидание {lo}..{hi})")
    if not ok:
        failures.append(name)


clients = f"read_csv('{D}/abs/clients.csv', delim=';', all_varchar=true)"
accounts = f"read_csv('{D}/abs/accounts.csv', delim=';')"
cards = f"read_csv('{D}/abs/cards.csv', delim=';')"
txn = f"read_parquet('{D}/processing/transactions_*.parquet')"
events = f"read_json('{D}/applog/app_events_*.jsonl')"

print("АБС:")
check("клиентов в выгрузке", f"select count(*) from {clients}", 12_000, 12_500)
check("полных дублей client_id",
      f"select count(*) - count(distinct client_id) from {clients}", 100, 140)
check("дат рождения в формате ДД.ММ.ГГГГ, %",
      f"select round(100.0*sum(case when birth_date like '%.%' then 1 else 0 end)/count(*)) from {clients}", 30, 50)
check("грязных значений сегмента (не lower-case)",
      f"select count(distinct segment) from {clients}", 6, 6)
check("счетов-сирот (client_id не из выгрузки)",
      f"""select count(*) from {accounts} a left join {clients} c using (client_id)
          where c.client_id is null""", 30, 90)

print("Процессинг:")
check("транзакций всего", f"select count(*) from {txn}", 2_000_000, 2_500_000)
check("полных дублей строк (повторная доставка)",
      f"select count(*) - count(distinct txn_id) from {txn}", 7_000, 12_000)
check("reversals", f"select count(*) from {txn} where status='reversed'", 8_000, 16_000)
check("операций по картам не из АБС",
      f"""select count(*) from {txn} t left join {cards} c using (card_id)
          where c.card_id is null""", 4_000, 10_000)
check("MCC=0000", f"select count(*) from {txn} where mcc='0000'", 6_000, 11_000)
check("валютных операций, %",
      f"select round(100.0*sum(case when currency<>'RUB' then 1 else 0 end)/count(*), 1) from {txn}", 1.0, 3.0)
check("доля топ-25 мерчантов, %",
      f"""select round(100.0*sum(case when merchant_id <= 'M3024' then 1 else 0 end)
          / count(merchant_id), 1) from {txn}""", 22.0, 32.0)

print("Курсы и логи:")
check("дней с курсом (только будни)",
      f"select count(*) from read_json('{D}/rates/cbr_rates.json')", 60, 70)
check("суббот и воскресений среди дат курса",
      f"""select count(*) from read_json('{D}/rates/cbr_rates.json')
          where dayofweek(date::date) in (0, 6)""", 0, 0)
check("событий приложения", f"select count(*) from {events}", 400_000, 700_000)
check("событий без client_id, %",
      f"select round(100.0*sum(case when client_id is null then 1 else 0 end)/count(*), 1) from {events}", 1.0, 3.0)

print("Сквозная сборка:")
check("txn→card→account→client→region собирается, округов",
      f"""select count(distinct r.federal_district)
          from {txn} t
          join {cards} c using (card_id)
          join {accounts} a using (account_id)
          join (select distinct client_id, city from {clients}) cl using (client_id)
          join read_csv('{D}/refs/regions.csv') r using (city)
          where t.status = 'approved'""", 8, 8)

if failures:
    print(f"\nПровалено: {len(failures)} — {failures}")
    sys.exit(1)
print("\nВсе проверки пройдены — датасет можно выдавать.")
