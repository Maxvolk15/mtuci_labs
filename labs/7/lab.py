# Лабораторная работа №7: Работа с классами ч.3

# Задание: Система управления сотрудниками

class Employee:
    """Базовый класс для представления сотрудника."""
    def __init__(self, name, id, **kwargs):
        """
        Конструктор для инициализации атрибутов сотрудника.
        """
        self.name = name
        self.id = id
        super().__init__(**kwargs)

    def get_info(self):
        """
        Возвращает базовую информацию о сотруднике.
        """
        return f"Имя: {self.name}, ID: {self.id}"

class Manager(Employee):
    """Класс для представления менеджера."""
    def __init__(self, name, id, department, **kwargs):
        """
        Конструктор для инициализации атрибутов менеджера.
        """
        super().__init__(name=name, id=id, **kwargs)
        self.department = department

    def get_info(self):
        """
         Возвращает информацию о менеджере с указанием отдела.
        """
        return f"{super().get_info()}, Отдел: {self.department}"

    def manage_project(self):
        """
         Символизирует управление проектами.
        """
        print(f"Менеджер {self.name} управляет проектом.")

class Technician(Employee):
    """Класс для представления технического специалиста."""
    def __init__(self, name, id, specialization, **kwargs):
        """
        Конструктор для инициализации атрибутов технического специалиста.
        """
        super().__init__(name=name, id=id, **kwargs)
        self.specialization = specialization

    def get_info(self):
      """
       Возвращает информацию о техническом специалисте с указанием специализации.
      """
      return f"{super().get_info()}, Специализация: {self.specialization}"

    def perform_maintenance(self):
        """
         Символизирует выполнение технического обслуживания.
        """
        print(f"Техник {self.name} выполняет техническое обслуживание.")

class TechManager(Manager, Technician):
    """Класс для представления технического менеджера, наследующий от Manager и Technician."""
    def __init__(self, name, id, department, specialization, **kwargs):
        """
        Конструктор для инициализации атрибутов технического менеджера.
        """
        super().__init__(name=name, id=id, department=department, specialization=specialization, **kwargs)
        self.subordinates = [] # Список для хранения подчинённых сотрудников

    def add_employee(self, employee):
        """
        Добавляет сотрудника в список подчинённых.
        """
        self.subordinates.append(employee)

    def get_team_info(self):
        """
        Выводит информацию о всех подчинённых сотрудниках.
        """
        print(f"\nКоманда под руководством {self.name}:")
        for employee in self.subordinates:
            print(employee.get_info())

# --- Тест ---
print("Тестирование системы управления сотрудниками:")
# Создаем объекты каждого класса
employee1 = Employee("Иван Иванов", 101)
manager1 = Manager("Петр Петров", 201, "Разработка")
technician1 = Technician("Сидор Сидоров", 301, "Сетевые технологии")
tech_manager1 = TechManager("Анна Андреева", 401, "ИТ", "Программирование")

# Демонстрируем функциональность
print(employee1.get_info())
print(manager1.get_info())
manager1.manage_project()
print(technician1.get_info())
technician1.perform_maintenance()
print(tech_manager1.get_info())
tech_manager1.manage_project()
tech_manager1.perform_maintenance()


# Добавляем подчинённых для тех. менеджера
tech_manager1.add_employee(employee1)
tech_manager1.add_employee(technician1)

# Выводим информацию о команде
tech_manager1.get_team_info()