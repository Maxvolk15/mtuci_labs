package lab3;

public class TaskOne {
    public static void main(String[] args) {
        HashTable<Integer, String> studtable = new HashTable<>(10);
        
        System.out.println("Таблица пуста: " + studtable.isEmpty());
        System.out.println("Размер таблицы: " + studtable.size());
        System.out.println();
        
        studtable.put(101, "Иван Петров");
        studtable.put(102, "Мария Сидорова");
        studtable.put(103, "Алексей Козлов");
        studtable.put(104, "Елена Новикова");
        studtable.put(105, "Дмитрий Волков");
        
        System.out.println("После добавления 5 студентов:");
        System.out.println("Таблица пуста: " + studtable.isEmpty());
        System.out.println("Размер таблицы: " + studtable.size());
        System.out.println();
        
        System.out.println("Поиск студентов по ID:");
        System.out.println("ID 101: " + studtable.get(101));
        System.out.println("ID 103: " + studtable.get(103));
        System.out.println("ID 106: " + studtable.get(106));
        System.out.println();
        
        System.out.println("Обновление данных студента с ID 102:");
        studtable.put(102, "Мария Иванова");
        System.out.println("ID 102 после обновления: " + studtable.get(102));
        System.out.println("Размер таблицы после обновления: " + studtable.size());
        System.out.println();
        
        HashTable<String, String> subtable = new HashTable<>();
        
        subtable.put("MATH101", "Математический анализ");
        subtable.put("PHYS202", "Общая физика");
        subtable.put("CS303", "Программирование на Java");
        subtable.put("ENG404", "Английский язык");
        
        System.out.println("Таблица предметов:");
        System.out.println("MATH101: " + subtable.get("MATH101"));
        System.out.println("CS303: " + subtable.get("CS303"));
        System.out.println("Размер таблицы предметов: " + subtable.size());
        System.out.println();

        System.out.println("Пример удаления:");
        System.out.println("Размер таблицы студентов до удаления: " + studtable.size());
        System.out.println();
        studtable.remove(103);
        System.out.println("После удаления ID 103:");
        System.out.println("ID 103: " + studtable.get(103));
        System.out.println("Размер таблицы студентов после удаления: " + studtable.size());
        System.out.println();
        
        studtable.remove(101);
        studtable.remove(105);
        
        System.out.println("После удаления ID 101 и 105:");
        System.out.println("Размер таблицы студентов: " + studtable.size());
        System.out.println("ID 101: " + studtable.get(101));
        System.out.println("ID 102: " + studtable.get(102));
        System.out.println("ID 104: " + studtable.get(104));
        System.out.println();
        
        System.out.println("Таблица студентов пуста: " + studtable.isEmpty());
        
        studtable.remove(102);
        studtable.remove(104);
        
        System.out.println("После удаления всех студентов:");
        System.out.println("Размер таблицы студентов: " + studtable.size());
        System.out.println("Таблица студентов пуста: " + studtable.isEmpty());
    }
}

