package lab3;

public class TaskTwo {
    public static class Student {
        String firstName;
        String lastName;
        int age;
        double averageGrade;

        public Student(String firstName, String lastName, int age, double averageGrade) {
            this.firstName = firstName;
            this.lastName = lastName;
            this.age = age;
            this.averageGrade = averageGrade;
        }

        @Override
        public String toString() {
            return "Student: " + firstName + " " + lastName + ", age: " + age + ", averageGrade: " + averageGrade;
        }
    }

    public static void main(String[] args) {
        HashTable<Integer, Student> st = new HashTable<>();

        System.out.println("Создание студентов:");
        st.put(202501, new Student("Misha", "Golikov", 17, 4.8));
        st.put(202502, new Student("Stepan", "Aniskov", 18, 3.6));
        st.put(202503, new Student("Artem", "Vladimirovich", 23, 4.6));
        st.put(202504, new Student("Tanya", "Zorkina", 17, 3.2));
        st.put(202505, new Student("Vadim", "Aniskov", 19, 2.6));
        System.out.println();

        System.out.println("Количество студентов до изменений: " + st.size());
        System.out.println();

        System.out.println("Изменяем студента с номером зачётки: 202502: ");
        System.out.println("Старый студент: " + st.get(202502));
        st.put(202502, new Student("Anna", "Socolova", 23, 4.7));
        System.out.println("Новый студент: " + st.get(202502));
        System.out.println();

        System.out.println("Поиск студентов:");
        System.out.println("Студент по зачётке 202503: " + st.get(202503));
        System.out.println("Студент по зачётке 202501: " + st.get(202501));
        System.out.println("Студент по зачётке 202505: " + st.get(202505));
        System.out.println("Студент по зачётке 202506: " + st.get(202506));    
        System.out.println();

        System.out.println("Удаление студентов:");
        System.out.println("Удаляем студентов с зачёткой 202502 и 202501:");
        System.out.println("Студенты до удаления:");
        System.out.println(st.get(202502));
        System.out.println(st.get(202501));
        st.remove(202502);
        st.remove(202501);
        System.out.println();
        System.out.println("После удаления:");
        System.out.println("Студент зачётка 202502: " + st.get(202502));
        System.out.println("Студент зачётка 202501: " + st.get(202501));
    }
}

