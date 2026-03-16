# Лабораторная работа №4: Модули и пакеты

# Задание 1: Импорт стандартных модулей

import math
import datetime

print("Задание 1:")
# Вычисление квадратного корня
num = 25
sqrt_num = math.sqrt(num)
print(f"Квадратный корень из {num}: {sqrt_num}")

# Отображение текущей даты и времени
now = datetime.datetime.now()
print(f"Текущая дата и время: {now}")

# ------------------------------------
# Задание 2: Создание и использование собственного модуля

import my_module

print("\nЗадание 2:")
# Вызываем функцию из своего модуля
result = my_module.add(5, 3)
print(f"Сумма 5 и 3: {result}")


# ------------------------------------
# Задание 3

from my_package import numbers, strings

print("\nЗадание 3:")
# Используем функции из модулей внутри пакета

# Модуль numbers
print(f"Сумма 10 и 20: {numbers.sum(10,20)}")
print(f"Произведение 5 и 7: {numbers.multiply(5,7)}")

# Модуль strings
print(f"Строка 'Hello' в верхнем регистре: {strings.upper('Hello')}")
print(f"Строка 'World' в нижнем регистре: {strings.lower('World')}")