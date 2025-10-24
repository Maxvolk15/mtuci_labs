package lab4;

public class ArrayAverage {
    public static void main(String[] args) {
        Object[] arr = {1, 2, 3, 4, 5, "9"};
        int summ = 0;

        try {
            for (int i = 0; i < arr.length; i++) {
                if (arr[i] instanceof String) {
                    throw new ClassCastException("Ошибка: элемент массива не является числом.");
                }
                summ += (int) arr[i];
            }
            System.out.println("Среднее арифм массива: " + summ/arr.length);
        } catch (IndexOutOfBoundsException e) {
            System.out.println("Ошибка: индекс вне массива.");
        } catch (ClassCastException e) {
            System.out.println(e.getMessage());
        } catch (Exception e) {
            System.out.println("Другой вид ошибки.");
        }
    }
}

// Массив из строк идёт по перебору int - выдать ошибку