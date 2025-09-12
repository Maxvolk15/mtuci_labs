# Лабораторная работа №2: Функции в Python и базовые алгоритмы

# Задание 1: Написание простых функций

def greet(name):
    """Выводит приветствие с указанным именем."""
    print(f"Привет, {name}!")


def square(number):
    """Возвращает квадрат числа."""
    return number * number


def max_of_two(x, y):
    """Возвращает большее из двух чисел."""
    if x > y:
        return x
    else:
        return y


# Задание 2: Работа с аргументами функций

def describe_person(name, age=30):
    """Выводит описание человека с именем и возрастом (возраст опционален)."""
    print(f"Имя: {name}, Возраст: {age}")


# Задание 3: Использование функций для решения алгоритмических задач

def is_prime(number):
    """Проверяет, является ли число простым, и возвращает True или False."""
    if number <= 1:
        return False
    for i in range(2, int(number**0.5) + 1):
        if number % i == 0:
            return False
    return True


# --- Тесты ---

# Задание 1
greet("Max")
print(f"Квадрат числа 5: {square(5)}")
print(f"Большее из 10 и 5: {max_of_two(10, 5)}")
print("---------------------------------------------------\n")

# Задание 2
describe_person("Misha")
describe_person("Vovchik", 25)
print("---------------------------------------------------\n")

# Задание 3
print(f"Число 7 простое? {is_prime(7)}")
print(f"Число 10 простое? {is_prime(10)}")