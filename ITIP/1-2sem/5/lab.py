# Лабораторная работа №5: Работа с классами

# Задание 1: Базовый класс и методы

class Book:
    """Класс для представления книги."""

    def __init__(self, title, author, year):
        """
        Конструктор для инициализации атрибутов книги.
        """
        self.title = title
        self.author = author
        self.year = year

    def get_info(self):
        """
        Возвращает информацию о книге в формате строки.
        """
        return f"Название книги: {self.title}, Автор: {self.author}, Год издания: {self.year}"


# Задание 2: Работа с конструктором

class Circle:
    """Класс для представления круга."""

    def __init__(self, radius):
        """
        Конструктор для инициализации радиуса круга.
        """
        self.radius = radius

    def get_radius(self):
        """
        Возвращает значение радиуса.
        """
        return self.radius

    def set_radius(self, new_radius):
        """
        Устанавливает новое значение радиуса.
        """
        self.radius = new_radius


# --- Тест ---

print("Задание 1:")
# Создаем объект класса Book
book1 = Book("Мастер и Маргарита", "Михаил Булгаков", 1967)
print(book1.get_info())  # Выводим информацию о книге

print("\nЗадание 2:")
# Создаем объект класса Circle
circle1 = Circle(5)
print(f"Исходный радиус круга: {circle1.get_radius()}")

# Изменяем радиус
circle1.set_radius(10)
print(f"Новый радиус круга: {circle1.get_radius()}")