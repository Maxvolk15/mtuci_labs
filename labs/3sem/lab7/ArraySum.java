package lab7;

import java.util.*;
import java.util.concurrent.*;

public class ArraySum {
    public static void main(String[] args) throws InterruptedException{
        int[] array = {3, 7, 2, 8, 5, 1, 9, 4, 6, 0, 5, 3, 8, 2, 7, 1, 9, 4, 6, 0, 3, 7, 2, 8, 5, 1, 9, 4, 6, 0, 5, 3, 8, 2, 7, 1, 9, 4, 6, 0, 3, 7, 2, 8, 5, 1, 9, 4, 6, 0, 5, 3, 8, 2, 7, 1, 9, 4, 6, 0, 3, 7, 2, 8, 5, 1, 9, 4, 6, 0, 5, 3, 8, 2, 7, 1, 9, 4, 6, 0, 3, 7, 2, 8, 5, 1, 9, 4, 6, 0, 5, 3, 8, 2, 7, 1, 9, 4, 6, 0};
        int mid = array.length/2;
        SumThread thread1 = new SumThread(array, 0, mid);
        SumThread thread2 = new SumThread(array, mid, array.length);

        thread1.start();
        thread2.start();

        thread1.join();
        thread2.join();

        System.out.println("Сумма: " + (thread1.getSum() + thread2.getSum()));

    }
}

class SumThread extends Thread {
    private int[] array;
    private int part;
    private int index;
    private int sum = 0;

    public SumThread(int[] array, int part, int index) {
        this.array = array;
        this.part = part;
        this.index = index;
    }

    @Override
    public void run() {
        System.out.println("Поток выполняется: " + getName());
        for (int i = part; i < index; i++) {
            sum += array[i];
        }
    }

    public int getSum() {
        return sum;
    }
}