# Лабораторная работа №1: Работа со структурами данных, циклами и условными операторами в Python

# 1. Работа со структурами данных

my_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

print("Первый элемент:", my_list[0])
print("Третий элемент:", my_list[2])
print("Последний элемент:", my_list[-1])

my_list[1] = 100
print("Список после замены второго элемента:", my_list)

# 2. Работа с циклами

print("\nЦикл for:")
for i in range(1, 11):
    print(i)

print("\nЦикл while:")
i = 10
while i >= 1:
    print(i)
    i -= 1

# 3. Работа с условными операторами

print("\nПроверка четности:")
num = int(input("Введите число: "))
if num % 2 == 0:
    print("Число четное")
else:
    print("Число нечетное")

print("\nПроверка знака числа:")
num = int(input("Введите число: "))
if num > 0:
    print("Число положительное")
elif num < 0:
    print("Число отрицательное")
else:
    print("Число равно нулю")