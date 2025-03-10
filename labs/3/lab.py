# Лабораторная работа №3: Работа с файлами в Python

# Задание 1: Открытие и чтение файла

def read_file(filename, read_type='all'):
    """
    Открывает файл и выводит его содержимое на экран.
    """
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            if read_type == 'all':
                content = file.read()
                print("Содержимое файла:")
                print(content)
            elif read_type == 'line':
                print("Содержимое файла (построчно):")
                for line in file:
                    print(line, end='') # end='' чтобы избежать двойных переносов строк

            else:
                print("Неверный тип чтения. Используйте 'all' или 'line'.")

    except FileNotFoundError:
        print(f"Ошибка: Файл '{filename}' не найден.")
    except Exception as e:
        print(f"Произошла ошибка: {e}") # Обработка других возможных ошибок

# Задание 2: Запись в файл
def write_to_file(filename, text, append=False):
    """
    Записывает текст в файл.
    """
    try:
        mode = 'a' if append else 'w'  # 'a' для добавления, 'w' для перезаписи
        with open(filename, mode, encoding='utf-8') as file:
            file.write(text)
        print(f"Текст успешно {'добавлен' if append else 'записан'} в файл '{filename}'.")
    except Exception as e:
       print(f"Произошла ошибка записи в файл: {e}")

# --- Тест ---

# Задание 1:
print("Задание 1:")
read_file('example.txt')          # Чтение всего файла
read_file('example.txt', 'line')  # Построчное чтение
read_file('hehehe.txt')      # Проверка обработки исключений
read_file('example.txt', 'wrong')  # Проверка неверного типа

# Задание 2:
print("\nЗадание 2:")
user_text = input("Введите текст для записи в файл: ")
write_to_file('user_input.txt', user_text)
add_text = input("Введите текст для добавления в файл: ")
write_to_file('user_input.txt', "\n" + add_text, append=True)  # Добавление