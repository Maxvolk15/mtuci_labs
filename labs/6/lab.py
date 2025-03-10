# Лабораторная работа №6: Работа с классами ч.2

# Задание 1: Защита данных пользователя

class UserAccount:
    """Класс для представления аккаунта пользователя."""

    def __init__(self, username, email, password):
        """
        Конструктор для инициализации атрибутов пользователя.
        """
        self.username = username
        self.email = email
        self.__password = password  # Приватный атрибут

    def set_password(self, new_password):
        """
        Изменяет пароль аккаунта.
        """
        if len(new_password) < 6:
          print("Пароль должен состоять минимум из 6 символов.")
          return
        self.__password = new_password
        print("Пароль успешно изменен.")


    def check_password(self, password):
        """
        Проверяет соответствие введенного пароля текущему паролю.
        """
        return self.__password == password


# Задание 2: Полиморфизм и наследование

class Vehicle:
    """Базовый класс для представления транспортного средства."""

    def __init__(self, make, model):
        """
        Конструктор для инициализации атрибутов транспортного средства.
        """
        self.make = make
        self.model = model

    def get_info(self):
        """
        Возвращает информацию о транспортном средстве.
        """
        return f"Марка: {self.make}, Модель: {self.model}"


class Car(Vehicle):
    """Класс для представления автомобиля, наследующий от Vehicle."""

    def __init__(self, make, model, fuel_type):
        """
        Конструктор для инициализации атрибутов автомобиля.
        """
        super().__init__(make, model)  # Вызов конструктора родительского класса
        self.fuel_type = fuel_type

    def get_info(self):
        """
        Переопределяет метод get_info, добавляя информацию о типе топлива.
        """
        return f"{super().get_info()}, Тип топлива: {self.fuel_type}"  # Вызов метода родительского класса


# --- Тест ---

print("Задание 1:")
# Создаем объект класса UserAccount
user1 = UserAccount("Miha", "miha@mtuci.ru", "52")

# Проверяем пароль
print(f"Проверка пароля: {user1.check_password('52')}")
print(f"Проверка пароля: {user1.check_password('56')}")


# Изменяем пароль
user1.set_password("535254")
print(f"Проверка пароля: {user1.check_password('535254')}")

user1.set_password("54525")
print(f"Проверка пароля: {user1.check_password('54525')}")


print("\nЗадание 2:")
# Создаем объекты классов Vehicle и Car
vehicle1 = Vehicle("Toyota", "Camry")
car1 = Car("Tesla", "Model S", "Electric")

print(vehicle1.get_info())  # Выводим информацию о Vehicle
print(car1.get_info())  # Выводим информацию о Car