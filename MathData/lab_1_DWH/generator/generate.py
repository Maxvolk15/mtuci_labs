#!/usr/bin/env python3
"""
Детерминированный генератор данных необанка «Синица» — сквозной домен курса.

Легенда: студент — дата-инженер необанка. Данные лежат в пяти системах,
которые друг о друге не знают:

  data/abs/          выгрузка из АБС: клиенты, счета, карты (CSV через «;»)
  data/processing/   транзакции процессинга (Parquet, помесячно)
                     + справочник мерчантов эквайринга (CSV)
  data/refs/         справочники: MCC-коды, регионы (CSV)
  data/rates/        курсы валют ЦБ (JSON; в выходные курса нет — протягивать)
  data/applog/       события мобильного приложения (JSONL, помесячно)

Данные синтетические, но дефекты — как в жизни:
  клиенты      полные дубли (~1%), «почти дубли» (~0.7%: ё/е, формат телефона),
               два формата дат в одной колонке, N/A и пустые значения,
               грязные справочные значения (сегмент, пол, город)
  счета        сироты — client_id, которого нет в выгрузке (~0.3%)
  транзакции   повторная доставка — полные дубли строк (~0.4%),
               reversals отрицательной суммой (~0.7% покупок),
               карты не из выгрузки АБС (~0.3%), MCC=0000 (~0.4%),
               перекос по мерчантам (топ-25 ≈ 27% операций) и по картам
  курсы        нет значений за выходные — forward fill обязателен
  события      client_id пуст у ~2% событий, дубли событий (~0.5%)

Детерминированность: random.Random(SEED) + duckdb setseed + threads=1.
Повторный запуск даёт те же данные: у всех студентов одинаковые цифры,
работы сравнимы между собой, проверка воспроизводима.

Запуск:  python generator/generate.py [--per-day 25000] [--events-per-day 6000]
                                      [--out data] [--seed 0.42]
Для лаб про Spark масштаб поднимается ключом --per-day без правки кода.
"""
import argparse
import csv
import json
import pathlib
import random

import duckdb

# ── период ───────────────────────────────────────────────────────────────────
# (метка, первый день, дней в месяце); «сегодня» по легенде — 1 сентября 2026
MONTHS = [
    ("2026-06", "2026-06-01", 30),
    ("2026-07", "2026-07-01", 31),
    ("2026-08", "2026-08-01", 31),
]
PERIOD_START, PERIOD_END = "2026-06-01", "2026-08-31"

N_CLIENTS = 12_000

# ── справочные данные ────────────────────────────────────────────────────────
# (город, вес, регион, федеральный округ, транслит). Иннополис и Сириус
# намеренно отсутствуют в refs/regions.csv — «города, которых нет в справочнике».
CITIES = [
    ("Москва", 0.30, "Москва", "ЦФО", "MOSKVA"),
    ("Санкт-Петербург", 0.12, "Санкт-Петербург", "СЗФО", "SANKT-PETERBURG"),
    ("Новосибирск", 0.05, "Новосибирская область", "СФО", "NOVOSIBIRSK"),
    ("Екатеринбург", 0.05, "Свердловская область", "УФО", "EKATERINBURG"),
    ("Казань", 0.05, "Республика Татарстан", "ПФО", "KAZAN"),
    ("Нижний Новгород", 0.04, "Нижегородская область", "ПФО", "N.NOVGOROD"),
    ("Краснодар", 0.04, "Краснодарский край", "ЮФО", "KRASNODAR"),
    ("Самара", 0.03, "Самарская область", "ПФО", "SAMARA"),
    ("Уфа", 0.03, "Республика Башкортостан", "ПФО", "UFA"),
    ("Ростов-на-Дону", 0.03, "Ростовская область", "ЮФО", "ROSTOV-NA-DONU"),
    ("Красноярск", 0.025, "Красноярский край", "СФО", "KRASNOYARSK"),
    ("Пермь", 0.025, "Пермский край", "ПФО", "PERM"),
    ("Воронеж", 0.025, "Воронежская область", "ЦФО", "VORONEZH"),
    ("Волгоград", 0.02, "Волгоградская область", "ЮФО", "VOLGOGRAD"),
    ("Тюмень", 0.02, "Тюменская область", "УФО", "TYUMEN"),
    ("Саратов", 0.015, "Саратовская область", "ПФО", "SARATOV"),
    ("Ижевск", 0.01, "Удмуртская Республика", "ПФО", "IZHEVSK"),
    ("Барнаул", 0.01, "Алтайский край", "СФО", "BARNAUL"),
    ("Иркутск", 0.01, "Иркутская область", "СФО", "IRKUTSK"),
    ("Хабаровск", 0.01, "Хабаровский край", "ДФО", "KHABAROVSK"),
    ("Владивосток", 0.01, "Приморский край", "ДФО", "VLADIVOSTOK"),
    ("Калининград", 0.01, "Калининградская область", "СЗФО", "KALININGRAD"),
    ("Сочи", 0.01, "Краснодарский край", "ЮФО", "SOCHI"),
    ("Ставрополь", 0.01, "Ставропольский край", "СКФО", "STAVROPOL"),
    ("Иннополис", 0.005, None, None, "INNOPOLIS"),
    ("Сириус", 0.005, None, None, "SIRIUS"),
]

MALE_NAMES = ["Александр", "Дмитрий", "Максим", "Сергей", "Андрей", "Алексей",
              "Артём", "Илья", "Кирилл", "Михаил", "Никита", "Матвей", "Роман",
              "Егор", "Иван", "Денис", "Евгений", "Даниил", "Тимофей", "Владислав",
              "Игорь", "Владимир", "Павел", "Руслан"]
FEMALE_NAMES = ["Анастасия", "Мария", "Дарья", "Анна", "Елизавета", "Полина",
                "Виктория", "Екатерина", "Софья", "Александра", "Валерия",
                "Вероника", "Арина", "Алиса", "Ксения", "Милана", "Диана",
                "Алина", "Маргарита", "Ольга", "Татьяна", "Наталья", "Ирина", "Юлия"]
SURNAMES = ["Иванов", "Смирнов", "Кузнецов", "Попов", "Васильев", "Петров",
            "Соколов", "Михайлов", "Новиков", "Фёдоров", "Морозов", "Волков",
            "Алексеев", "Лебедев", "Семёнов", "Егоров", "Павлов", "Козлов",
            "Степанов", "Николаев", "Орлов", "Андреев", "Макаров", "Никитин",
            "Захаров", "Зайцев", "Соловьёв", "Борисов", "Яковлев", "Григорьев",
            "Романов", "Воробьёв", "Сергеев", "Фролов", "Александров", "Дмитриев",
            "Королёв", "Гусев", "Киселёв", "Ильин", "Максимов", "Поляков",
            "Сорокин", "Виноградов", "Ковалёв", "Белов", "Медведев", "Антонов",
            "Тарасов", "Жуков", "Баранов", "Филиппов", "Комаров", "Давыдов",
            "Белкин", "Ткаченко", "Мельник", "Шевченко", "Бондаренко", "Кравченко"]
PATRONYMICS_M = ["Александрович", "Дмитриевич", "Сергеевич", "Андреевич",
                 "Алексеевич", "Иванович", "Михайлович", "Николаевич",
                 "Павлович", "Владимирович", "Олегович", "Петрович",
                 "Романович", "Юрьевич", "Игоревич", "Викторович",
                 "Анатольевич", "Борисович", "Григорьевич", "Степанович"]

TRANSLIT = dict(zip("абвгдежзийклмнопрстуфхцчшщъыьэюяё",
                    ["a", "b", "v", "g", "d", "e", "zh", "z", "i", "y", "k", "l",
                     "m", "n", "o", "p", "r", "s", "t", "u", "f", "kh", "ts",
                     "ch", "sh", "sch", "", "y", "", "e", "yu", "ya", "e"]))

PRODUCTS = [("DC", "Дебетовая карта «Синица»", 0.52),
            ("CC", "Кредитная карта «Синица»", 0.22),
            ("SV", "Накопительный счёт «Копилка»", 0.18),
            ("DEP", "Вклад «Гнездо»", 0.08)]

# MCC-справочник: (код, описание, категория)
MCC_CODES = [
    ("4112", "Железнодорожные перевозки", "Путешествия"),
    ("4121", "Такси", "Транспорт"),
    ("4511", "Авиаперевозки", "Путешествия"),
    ("4722", "Турагентства", "Путешествия"),
    ("4814", "Связь и телеком", "Связь"),
    ("4829", "Денежные переводы", "Переводы"),
    ("4900", "Коммунальные услуги", "ЖКХ"),
    ("5309", "Магазины duty free", "Путешествия"),
    ("5311", "Универмаги", "Покупки"),
    ("5399", "Маркетплейсы и универсальные магазины", "Покупки"),
    ("5411", "Супермаркеты", "Продукты"),
    ("5541", "АЗС", "Топливо"),
    ("5651", "Одежда", "Покупки"),
    ("5732", "Электроника", "Покупки"),
    ("5812", "Рестораны и кафе", "Рестораны"),
    ("5814", "Фастфуд", "Рестораны"),
    ("5816", "Цифровые товары и игры", "Цифровые сервисы"),
    ("5912", "Аптеки", "Здоровье"),
    ("5921", "Алкогольные магазины", "Продукты"),
    ("5941", "Спорттовары", "Покупки"),
    ("5942", "Книжные магазины", "Покупки"),
    ("5977", "Косметика и парфюмерия", "Покупки"),
    ("5999", "Специализированная розница", "Покупки"),
    ("6011", "Снятие наличных", "Наличные"),
    ("7011", "Отели", "Путешествия"),
]

# Параметры логнормального распределения сумм по категориям (в рублях)
AMOUNT_PARAMS = {
    "Продукты": (6.45, 0.70), "Рестораны": (6.85, 0.60), "Топливо": (7.60, 0.40),
    "Покупки": (7.55, 1.00), "Путешествия": (8.75, 0.75), "Связь": (6.40, 0.30),
    "ЖКХ": (7.80, 0.50), "Переводы": (8.00, 1.10), "Наличные": (8.60, 0.80),
    "Цифровые сервисы": (6.30, 0.80), "Транспорт": (6.00, 0.50),
    "Здоровье": (6.60, 0.60),
}

# Топ-мерчанты: (название, транслит для сырой строки, MCC, канал).
# Порядок = ранг популярности: индекс выбирается как floor(r² · N),
# поэтому голова списка забирает непропорционально много операций.
TOP_MERCHANTS = [
    ("Пятёрочка", "PYATEROCHKA", "5411", "pos"),
    ("Магнит", "MAGNIT", "5411", "pos"),
    ("Яндекс Такси", "YANDEX.TAXI", "4121", "ecom"),
    ("Wildberries", "WILDBERRIES", "5651", "ecom"),
    ("Ozon", "OZON.RU", "5399", "ecom"),
    ("Перекрёсток", "PEREKRESTOK", "5411", "pos"),
    ("Лукойл", "LUKOIL AZS", "5541", "pos"),
    ("Красное&Белое", "KRASNOE-BELOE", "5921", "pos"),
    ("Яндекс Еда", "YANDEX.EDA", "5812", "ecom"),
    ("Вкусно — и точка", "VKUSNO I TOCHKA", "5814", "pos"),
    ("Лента", "LENTA", "5411", "pos"),
    ("МТС", "MTS.RU", "4814", "ecom"),
    ("ВкусВилл", "VKUSVILL", "5411", "pos"),
    ("Газпромнефть", "GAZPROMNEFT AZS", "5541", "pos"),
    ("Мегафон", "MEGAFON", "4814", "ecom"),
    ("Додо Пицца", "DODO PIZZA", "5814", "ecom"),
    ("РЖД", "RZD PASS", "4112", "ecom"),
    ("Аэрофлот", "AEROFLOT", "4511", "ecom"),
    ("Аптека Ригла", "APTEKA RIGLA", "5912", "pos"),
    ("DNS", "DNS RETAIL", "5732", "pos"),
    ("М.Видео", "MVIDEO", "5732", "pos"),
    ("Спортмастер", "SPORTMASTER", "5941", "pos"),
    ("Летуаль", "LETOILE", "5977", "pos"),
    ("Читай-город", "CHITAI-GOROD", "5942", "pos"),
    ("Самокат", "SAMOKAT", "5411", "ecom"),
]
# Зарубежные мерчанты — операции в валюте; стоят сразу за топом,
# чтобы дать ~1.5–2% валютных операций
FOREIGN_MERCHANTS = [
    ("AliExpress", "ALIEXPRESS", "5399", "ecom", "CNY", "HANGZHOU CN"),
    ("Trip.com", "TRIP.COM", "4722", "ecom", "USD", "SINGAPORE SG"),
    ("Steam", "STEAM GAMES", "5816", "ecom", "USD", "HAMBURG DE"),
    ("Duty Free Istanbul", "DUTY FREE IST", "5309", "pos", "EUR", "ISTANBUL TR"),
]
N_TAIL_MERCHANTS = 320

MCC_CATEGORY = {code: cat for code, _, cat in MCC_CODES}

EMAIL_DOMAINS = ["mail.ru", "yandex.ru", "gmail.com", "bk.ru", "inbox.ru", "rambler.ru"]

# доли событий приложения по часам суток (пики утром и вечером), сумма = 1
EVENT_HOUR_WEIGHTS = [
    0.010, 0.006, 0.004, 0.003, 0.003, 0.006,   # 00-05
    0.020, 0.045, 0.060, 0.055, 0.048, 0.052,   # 06-11
    0.062, 0.055, 0.050, 0.048, 0.050, 0.058,   # 12-17
    0.072, 0.080, 0.078, 0.065, 0.045, 0.025,   # 18-23
]
# доли покупок по часам: ночной провал, обеденный и вечерний пики
TXN_HOUR_WEIGHTS = [
    0.008, 0.005, 0.004, 0.003, 0.003, 0.006,
    0.015, 0.035, 0.050, 0.048, 0.050, 0.062,
    0.075, 0.062, 0.052, 0.050, 0.055, 0.068,
    0.082, 0.080, 0.070, 0.058, 0.040, 0.019,
]


def translit(s: str) -> str:
    return "".join(TRANSLIT.get(ch, ch) for ch in s.lower())


def female_surname(s: str) -> str:
    if s.endswith(("ов", "ев", "ёв", "ин", "ын")):
        return s + "а"
    if s.endswith("ий"):
        return s[:-2] + "ая"
    return s  # Ткаченко, Мельник и т.п. не склоняются


def hour_case(column: str, weights) -> str:
    """Разворачивает веса часов в CASE по накопленной вероятности."""
    parts, acc = [], 0.0
    for hour, weight in enumerate(weights[:-1]):
        acc += weight
        parts.append(f"when {column} < {acc:.6f} then {hour}")
    parts.append(f"else {len(weights) - 1}")
    return "case " + " ".join(parts) + " end"


# ── АБС: клиенты, счета, карты ───────────────────────────────────────────────

def rand_date(rnd, y1, y2):
    return f"{rnd.randint(y1, y2)}-{rnd.randint(1, 12):02d}-{rnd.randint(1, 28):02d}"


def make_clients(rnd):
    clients = []
    for i in range(N_CLIENTS):
        is_female = rnd.random() < 0.52
        surname = SURNAMES[rnd.randrange(len(SURNAMES))]
        if is_female:
            surname = female_surname(surname)
            name = FEMALE_NAMES[rnd.randrange(len(FEMALE_NAMES))]
            pat = PATRONYMICS_M[rnd.randrange(len(PATRONYMICS_M))][:-2] + "на"
            gender = rnd.choices(["Ж", "ж", "жен", "F"], [0.8, 0.07, 0.08, 0.05])[0]
        else:
            name = MALE_NAMES[rnd.randrange(len(MALE_NAMES))]
            pat = PATRONYMICS_M[rnd.randrange(len(PATRONYMICS_M))]
            gender = rnd.choices(["М", "м", "муж", "M"], [0.8, 0.07, 0.08, 0.05])[0]
        fio = f"{surname} {name} {pat}"

        birth = rand_date(rnd, 1962, 2008)
        if rnd.random() < 0.40:  # второй формат даты в той же колонке
            y, m, d = birth.split("-")
            birth = f"{d}.{m}.{y}"

        city, _, _, _, _ = rnd.choices(CITIES, [c[1] for c in CITIES])[0]
        if rnd.random() < 0.03:
            city = rnd.choice([city.upper(), city.lower(), f"г. {city}"])

        digits = f"9{rnd.randint(10**8, 10**9 - 1)}"
        phone = rnd.choice([
            f"+7{digits}", f"8{digits}",
            f"+7 ({digits[:3]}) {digits[3:6]}-{digits[6:8]}-{digits[8:]}",
            f"8 {digits[:3]} {digits[3:6]} {digits[6:8]} {digits[8:]}",
        ])
        if rnd.random() < 0.01:
            phone = ""

        email = f"{translit(name)}.{translit(surname)}{rnd.randint(1, 99)}@{rnd.choice(EMAIL_DOMAINS)}"
        if rnd.random() < 0.02:
            email = rnd.choice(["N/A", "-", ""])

        segment = rnd.choices(["mass", "Mass", "MASS", "premium", "Premium", "private"],
                              [0.62, 0.09, 0.07, 0.14, 0.04, 0.04])[0]
        registered = rand_date(rnd, 2021, 2025) + f" {rnd.randint(8, 21):02d}:{rnd.randint(0, 59):02d}:00"
        updated = registered if rnd.random() < 0.7 else \
            rand_date(rnd, 2026, 2026)[:8] + f"{rnd.randint(1, 28):02d} {rnd.randint(8, 21):02d}:00:00"

        clients.append([f"C{100000 + i}", fio, gender, birth, city, phone,
                        email, segment, registered, updated])

    # полные дубли (~1%): та же строка ещё раз
    for row in rnd.sample(clients, int(N_CLIENTS * 0.010)):
        clients.append(list(row))

    # «почти дубли» (~0.7%): другой client_id, вариация ФИО и формата телефона —
    # классическая задача MDM: тот же человек, вторая учётная запись
    for row in rnd.sample(clients[:N_CLIENTS], int(N_CLIENTS * 0.007)):
        twin = list(row)
        twin[0] = f"C{700000 + int(row[0][1:])}"
        twin[1] = row[1].replace("ё", "е") if "ё" in row[1] else row[1].replace(" ", "  ", 1)
        digits = "".join(ch for ch in row[5] if ch.isdigit())[-10:]
        twin[5] = f"+7{digits}" if digits else ""
        clients.append(twin)

    rnd.shuffle(clients)
    return clients


def make_accounts(rnd, clients):
    accounts = []
    seq = 0
    for row in clients[: N_CLIENTS]:            # дубли клиентов счетов не плодят
        client_id, registered = row[0], row[8]
        n = rnd.choices([1, 2, 3], [0.55, 0.33, 0.12])[0]
        codes = ["DC"] + rnd.choices([p[0] for p in PRODUCTS],
                                     [p[2] for p in PRODUCTS], k=n - 1)
        for code in codes:
            seq += 1
            pname = next(p[1] for p in PRODUCTS if p[0] == code)
            opened = max(registered[:10], rand_date(rnd, 2021, 2026))
            status, closed = ("active", "")
            if rnd.random() < 0.08:
                status, closed = "closed", rand_date(rnd, 2025, 2026)
            accounts.append([f"A{1000000 + seq}", client_id, code, pname,
                             opened, closed, status])
    # счета-сироты (~0.3%): client_id, которого нет в выгрузке клиентов
    for _ in range(int(len(accounts) * 0.003)):
        seq += 1
        code, pname, _ = rnd.choice(PRODUCTS)
        accounts.append([f"A{1000000 + seq}", f"C{900000 + rnd.randint(0, 9999)}",
                         code, pname, rand_date(rnd, 2022, 2026), "", "active"])
    return accounts


def make_cards(rnd, accounts):
    cards, seq = [], 0
    for acc in accounts:
        if acc[2] not in ("DC", "CC") or acc[6] == "closed":
            continue
        n = rnd.choices([1, 2, 0], [0.85, 0.10, 0.05])[0]
        for _ in range(n):
            seq += 1
            system = rnd.choices(["МИР", "Visa", "Mastercard"], [0.72, 0.14, 0.14])[0]
            bin_ = rnd.choice(["2200", "2202", "2204"]) if system == "МИР" else \
                rnd.choice(["4276", "5469"])
            pan = f"{bin_} {rnd.randint(10,99)}** **** {rnd.randint(1000, 9999)}"
            issued = max(acc[4], rand_date(rnd, 2022, 2026))
            expires = f"{int(issued[:4]) + 4}-{issued[5:7]}-01"
            status = "blocked" if rnd.random() < 0.02 else "active"
            cards.append([f"K{2000000 + seq}", acc[0], pan, system,
                          issued, expires, status])
    return cards


def make_merchants(rnd):
    """Единый список: топ → зарубежные → хвост. Порядок = ранг популярности."""
    merchants = []  # (merchant_id, name, translit, mcc, channel, currency, city)
    for name, tr, mcc, channel in TOP_MERCHANTS:
        merchants.append((name, tr, mcc, channel, "RUB", "федеральная сеть"))
    for name, tr, mcc, channel, ccy, city in FOREIGN_MERCHANTS:
        merchants.append((name, tr, mcc, channel, ccy, city))
    tail_mcc = ["5411", "5812", "5814", "5912", "5541", "5651", "5732", "5999",
                "4900", "5921", "5942"]
    ooo_words = ["Ромашка", "Вектор", "Заря", "Меркурий", "Атлант", "Гранат",
                 "Прогресс", "Родник", "Фрегат", "Юпитер", "Кристалл", "Титан",
                 "Сапфир", "Орион", "Квант", "Эверест", "Дельта", "Омега",
                 "Альянс", "Форум", "Салют", "Импульс", "Мираж", "Рубин",
                 "Топаз", "Агат", "Пилот", "Каскад", "Зенит", "Азимут"]
    cafe_words = ["Уют", "Минутка", "Причал", "Ковчег", "Луч", "Тайга",
                  "Восход", "Абрикос", "Вишня", "Маяк", "Бриз", "Шафран",
                  "Полянка", "Самовар", "Гнездо", "Лаванда", "Мельница",
                  "Барбарис", "Черника", "Облепиха", "Крендель", "Веранда"]
    for i in range(N_TAIL_MERCHANTS):
        kind = rnd.random()
        city = rnd.choices(CITIES, [c[1] for c in CITIES])[0]
        if kind < 0.30:
            s = SURNAMES[rnd.randrange(len(SURNAMES))]
            ini = f"{rnd.choice('АЕИКМНОПРС')}.{rnd.choice('АВЕИН')}."
            name, tr = f"ИП {s} {ini}", f"IP {translit(s).upper()}"
            mcc = rnd.choice(tail_mcc)
        elif kind < 0.55:
            word = ooo_words[rnd.randrange(len(ooo_words))]
            name, tr = f"ООО «{word}»", f"OOO {translit(word).upper()}"
            mcc = rnd.choice(tail_mcc)
        elif kind < 0.75:
            word = cafe_words[rnd.randrange(len(cafe_words))]
            name, tr = f"Кафе «{word}»", f"CAFE {translit(word).upper()}"
            mcc = rnd.choice(["5812", "5814"])
        elif kind < 0.88:
            n = rnd.randint(100, 999)
            name, tr, mcc = f"Аптека №{n}", f"APTEKA {n}", "5912"
        else:
            n = rnd.randint(10, 99)
            name, tr, mcc = f"АЗС «Регион-{n}»", f"AZS REGION-{n}", "5541"
        channel = "ecom" if rnd.random() < 0.15 else "pos"
        merchants.append((name, tr, mcc, channel, "RUB", city[0]))
    return [(f"M{3000 + i}", *m) for i, m in enumerate(merchants)]


def make_rates(rnd):
    """Курсы ЦБ: случайное блуждание, по выходным курс не публикуется."""
    import datetime
    rates, cur = [], {"USD": 81.20, "EUR": 94.55, "CNY": 11.34}
    day = datetime.date(2026, 6, 1)
    end = datetime.date(2026, 8, 31)
    while day <= end:
        if day.weekday() < 5:  # ЦБ не публикует курс на выходные
            for code in cur:
                cur[code] = round(cur[code] * (1 + rnd.gauss(0, 0.004)), 4)
            rates.append({
                "date": day.isoformat(),
                "valutes": {code: {"nominal": 1, "value": cur[code]} for code in cur},
            })
        day += datetime.timedelta(days=1)
    return rates


# ── процессинг: транзакции (DuckDB SQL, объёмная часть) ─────────────────────

TXN_SQL = """
create or replace table txn as
with base as (
    select i,
        (hash(i, 11) % 1000000) / 1000000.0 as r_card,
        (hash(i, 12) % 1000000) / 1000000.0 as r_merch,
        (hash(i, 13) % 1000000) / 1000000.0 as r_type,
        (hash(i, 14) % 1000000) / 1000000.0 as r_day,
        (hash(i, 15) % 1000000) / 1000000.0 as r_hour,
        (hash(i, 16) % 1000000) / 1000000.0 as r_min,
        (hash(i, 17) % 1000000) / 1000000.0 as r_sec,
        (hash(i, 18) % 1000000) / 1000000.0 as r_amt1,
        (hash(i, 19) % 1000000) / 1000000.0 as r_amt2,
        (hash(i, 20) % 1000000) / 1000000.0 as r_status,
        (hash(i, 21) % 1000000) / 1000000.0 as r_reason,
        (hash(i, 22) % 1000000) / 1000000.0 as r_branch,
        (hash(i, 23) % 1000000) / 1000000.0 as r_city,
        (hash(i, 24) % 1000000) / 1000000.0 as r_defect
    from range(0, {rows}) t(i)
),
typed as (
    select *,
        case when r_type < 0.10 then 'p2p'
             when r_type < 0.16 then 'atm'
             else 'purchase' end as op,
        -- перекос: квадрат равномерной величины прижимает выбор к голове списка
        cast(floor(pow(r_card, 2) * {n_cards}) as int)  as card_idx,
        cast(floor(pow(r_merch, 2) * {n_merch}) as int) as m_idx,
        timestamp '{month_start} 00:00:00'
            + to_days(cast(floor(r_day * {days}) as int))
            + to_hours({hour_expr})
            + to_minutes(cast(floor(r_min * 60) as int))
            + to_seconds(cast(floor(r_sec * 60) as int)) as txn_ts
    from base
),
joined as (
    select t.*, c.card_id as real_card_id,
        m.merchant_id as m_merchant_id, m.tr as m_tr, m.mcc as m_mcc,
        m.channel as m_channel, m.currency as m_currency,
        ct.tr as city_tr,
        case t.op when 'p2p' then 'Переводы'
                  when 'atm' then 'Наличные'
                  else m.category end as category
    from typed t
    join cards_t  c  on c.idx  = t.card_idx
    join merch_t  m  on m.idx  = t.m_idx
    join cities_t ct on ct.idx = cast(floor(t.r_city * {n_cities}) as int)
),
priced as (
    select *,
        -- логнормальная сумма через Бокса—Мюллера
        round(exp(p.mu + p.sigma *
              sqrt(-2 * ln(greatest(r_amt1, 1e-12))) * cos(2 * pi() * r_amt2)), 2)
            as amount_rub
    from joined
    join params_t p using (category)
)
select
    '{label}-' || lpad(i::varchar, 8, '0')                          as txn_id,
    txn_ts,
    -- ~0.3% операций пришло по картам, которых нет в выгрузке АБС
    case when r_defect < 0.003
         then 'K9' || lpad(cast(floor(r_branch * 90000) as int)::varchar, 5, '0')
         else real_card_id end                                       as card_id,
    case when op = 'purchase' then m_merchant_id end                 as merchant_id,
    case op
        when 'atm' then 'ATM ' || (220000 + cast(floor(r_branch * 9999) as int))::varchar
                        || ' ' || city_tr || ' RUS'
        when 'p2p' then 'SBP P2P PEREVOD'
        else m_tr || ' ' || (1 + cast(floor(r_branch * 8000) as int))::varchar
                  || ' ' || city_tr || ' RUS'
    end                                                              as merchant_name_raw,
    case when op = 'atm' then '6011'
         when op = 'p2p' then '4829'
         when r_defect >= 0.003 and r_defect < 0.007 then '0000'
         else m_mcc end                                              as mcc,
    case when op = 'purchase' then m_channel else op end             as channel,
    case
        when op = 'atm' then greatest(100, round(amount_rub / 100) * 100)
        when coalesce(m_currency, 'RUB') <> 'RUB' and op = 'purchase' then
            round(amount_rub / case m_currency when 'USD' then 81.0
                                               when 'EUR' then 94.0
                                               else 11.3 end, 2)
        else greatest(10.0, amount_rub)
    end                                                              as amount,
    case when op = 'purchase' then coalesce(m_currency, 'RUB')
         else 'RUB' end                                              as currency,
    case when r_status < 0.935 then 'approved' else 'declined' end   as status,
    case when r_status >= 0.935 then
        case when r_reason < 0.55 then 'insufficient_funds'
             when r_reason < 0.80 then 'limit_exceeded'
             when r_reason < 0.95 then 'suspected_fraud'
             else 'card_expired' end
    end                                                              as decline_reason,
    cast(null as varchar)                                            as orig_txn_id
from priced;

-- reversals: возврат отдельной записью с отрицательной суммой
create or replace table rev as
select
    'R-' || txn_id                                     as txn_id,
    least(txn_ts + to_hours(cast(1 + hash(txn_id, 31) % 72 as int)),
          timestamp '{month_last} 23:59:59')           as txn_ts,
    card_id, merchant_id, merchant_name_raw, mcc, channel,
    -amount                                            as amount,
    currency,
    'reversed'                                         as status,
    cast(null as varchar)                              as decline_reason,
    txn_id                                             as orig_txn_id
from txn
where status = 'approved' and channel in ('pos', 'ecom') and hash(txn_id, 32) % 10000 < 70;

-- повторная доставка из процессинга: полные дубли строк (тот же txn_id!)
create or replace table dup as
select * from txn where hash(txn_id, 33) % 10000 < 40;

create or replace table out as
select * from txn union all select * from rev union all select * from dup;
"""

EVENTS_SQL = """
create or replace table ev as
with base as (
    select i,
        (hash(i, 41) % 1000000) / 1000000.0 as r_client,
        (hash(i, 42) % 1000000) / 1000000.0 as r_day,
        (hash(i, 43) % 1000000) / 1000000.0 as r_hour,
        (hash(i, 44) % 1000000) / 1000000.0 as r_min,
        (hash(i, 45) % 1000000) / 1000000.0 as r_type,
        (hash(i, 46) % 1000000) / 1000000.0 as r_platform,
        (hash(i, 47) % 1000000) / 1000000.0 as r_null
    from range(0, {rows}) t(i)
),
shaped as (
    select *,
        cast(floor(pow(r_client, 1.7) * {n_clients}) as int) as client_idx,
        timestamp '{month_start} 00:00:00'
            + to_days(cast(floor(r_day * {days}) as int))
            + to_hours({hour_expr})
            + to_minutes(cast(floor(r_min * 60) as int)) as event_ts,
        case when r_type < 0.24 then 'login'
             when r_type < 0.44 then 'view_main'
             when r_type < 0.56 then 'view_history'
             when r_type < 0.66 then 'transfer_init'
             when r_type < 0.73 then 'transfer_success'
             when r_type < 0.80 then 'push_open'
             when r_type < 0.86 then 'card_details'
             when r_type < 0.92 then 'marketplace_view'
             when r_type < 0.96 then 'support_chat'
             else 'logout' end as event_type,
        case when r_platform < 0.40 then 'ios'
             when r_platform < 0.98 then 'android'
             else 'web' end as platform
    from base
)
select
    '{label}-E' || lpad(i::varchar, 8, '0')            as event_id,
    event_ts,
    case when r_null < 0.02 then null
         else c.client_id end                          as client_id,
    event_type, platform,
    case platform when 'ios'     then '4.{minor}.0'
                  when 'android' then '4.{minor}.2'
                  else 'web' end                       as app_version
from shaped s
join clients_t c on c.idx = s.client_idx;

create or replace table ev_dup as select * from ev where hash(event_id, 51) % 1000 < 5;
create or replace table ev_out as select * from ev union all select * from ev_dup;
"""


# ── запись файлов ────────────────────────────────────────────────────────────

def write_csv(path, header, rows, delimiter=";"):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, delimiter=delimiter)
        w.writerow(header)
        w.writerows(rows)
    print(f"  {path}  ({len(rows):,} строк)")


def main():
    ap = argparse.ArgumentParser(description="Генератор данных необанка «Синица»")
    ap.add_argument("--per-day", type=int, default=25_000,
                    help="транзакций в день (по умолчанию 25000)")
    ap.add_argument("--events-per-day", type=int, default=6_000,
                    help="событий приложения в день (по умолчанию 6000)")
    ap.add_argument("--out", default="data", help="каталог результата")
    ap.add_argument("--seed", type=float, default=0.42)
    args = ap.parse_args()

    out = pathlib.Path(args.out)
    rnd = random.Random(int(args.seed * 1000))

    print("АБС и справочники:")
    clients = make_clients(rnd)
    accounts = make_accounts(rnd, clients)
    cards = make_cards(rnd, accounts)
    merchants = make_merchants(rnd)
    rates = make_rates(rnd)

    write_csv(out / "abs" / "clients.csv",
              ["client_id", "fio", "gender", "birth_date", "city", "phone",
               "email", "segment", "registered_at", "updated_at"], clients)
    write_csv(out / "abs" / "accounts.csv",
              ["account_id", "client_id", "product_code", "product_name",
               "opened_at", "closed_at", "status"], accounts)
    write_csv(out / "abs" / "cards.csv",
              ["card_id", "account_id", "pan_masked", "payment_system",
               "issued_at", "expires_at", "status"], cards)
    write_csv(out / "processing" / "merchants.csv",
              ["merchant_id", "merchant_name", "merchant_name_latin", "mcc",
               "channel", "currency", "home_city"], merchants, delimiter=",")
    write_csv(out / "refs" / "mcc_codes.csv",
              ["mcc", "description", "category"], MCC_CODES, delimiter=",")
    write_csv(out / "refs" / "regions.csv",
              ["city", "region", "federal_district"],
              [(c[0], c[2], c[3]) for c in CITIES if c[2]], delimiter=",")

    rates_path = out / "rates" / "cbr_rates.json"
    rates_path.parent.mkdir(parents=True, exist_ok=True)
    rates_path.write_text(json.dumps(rates, ensure_ascii=False, indent=1),
                          encoding="utf-8")
    print(f"  {rates_path}  ({len(rates)} дней, выходных нет)")

    # объёмная часть — в DuckDB; threads=1 ради детерминированности random()
    con = duckdb.connect()
    con.execute("set threads to 1")

    con.execute("create table cards_t(idx int, card_id varchar)")
    active_cards = [c[0] for c in cards]
    rnd.shuffle(active_cards)  # ранг популярности карты не связан с порядком выпуска
    con.executemany("insert into cards_t values (?, ?)",
                    list(enumerate(active_cards)))

    con.execute("""create table merch_t(idx int, merchant_id varchar, tr varchar,
                   mcc varchar, channel varchar, currency varchar, category varchar)""")
    con.executemany("insert into merch_t values (?, ?, ?, ?, ?, ?, ?)",
                    [(i, m[0], m[2], m[3], m[4], m[5], MCC_CATEGORY.get(m[3], "Покупки"))
                     for i, m in enumerate(merchants)])

    con.execute("create table cities_t(idx int, tr varchar)")
    big_cities = [c for c in CITIES if c[1] >= 0.01]
    con.executemany("insert into cities_t values (?, ?)",
                    [(i, c[4]) for i, c in enumerate(big_cities)])

    con.execute("create table params_t(category varchar, mu double, sigma double)")
    con.executemany("insert into params_t values (?, ?, ?)",
                    [(k, *v) for k, v in AMOUNT_PARAMS.items()])

    con.execute("create table clients_t(idx int, client_id varchar)")
    client_ids = [c[0] for c in clients[:N_CLIENTS]]
    rnd.shuffle(client_ids)
    con.executemany("insert into clients_t values (?, ?)",
                    list(enumerate(client_ids)))

    print("Процессинг и логи приложения:")
    for mi, (label, month_start, days) in enumerate(MONTHS):
        month_last = f"{month_start[:8]}{days:02d}"
        con.execute(TXN_SQL.format(
            rows=args.per_day * days, n_cards=len(active_cards),
            n_merch=len(merchants), n_cities=len(big_cities),
            month_start=month_start, month_last=month_last, days=days,
            label=label, hour_expr=hour_case("r_hour", TXN_HOUR_WEIGHTS)))
        txn_path = out / "processing" / f"transactions_{label}.parquet"
        con.execute(f"""copy (select * from out order by txn_ts, txn_id)
                        to '{txn_path}' (format parquet, compression zstd)""")
        n = con.execute("select count(*) from out").fetchone()[0]
        print(f"  {txn_path}  ({n:,} строк)")

        con.execute(EVENTS_SQL.format(
            rows=args.events_per_day * days, n_clients=len(client_ids),
            month_start=month_start, days=days, label=label, minor=6 + mi,
            hour_expr=hour_case("r_hour", EVENT_HOUR_WEIGHTS)))
        ev_path = out / "applog" / f"app_events_{label}.jsonl"
        ev_path.parent.mkdir(parents=True, exist_ok=True)
        con.execute(f"""copy (select * from ev_out order by event_ts, event_id)
                        to '{ev_path}' (format json)""")
        n = con.execute("select count(*) from ev_out").fetchone()[0]
        print(f"  {ev_path}  ({n:,} строк)")

    con.close()
    total = sum(f.stat().st_size for f in out.rglob("*") if f.is_file())
    print(f"Готово: {total / 1e6:.0f} МБ в {out}/")


if __name__ == "__main__":
    main()
