package lab7;

import java.util.*;
import java.util.concurrent.locks.ReentrantLock;

class Item {
    private final String name;
    private final int weight;

    public Item(String name, int weight) {
        this.name = name;
        this.weight = weight;
    }

    public String getName() { return name; }
    public int getWeight() { return weight; }

    @Override
    public String toString() {
        return name + "-" + weight + " кг";
    }
}

class Warehouse {
    private final Queue<Item> items;
    private final ReentrantLock lock = new ReentrantLock();

    public Warehouse(List<Item> items) {
        this.items = new LinkedList<>(items);
    }

    public Item takeItem() {
        lock.lock();
        try {
            return items.poll();
        } finally {
            lock.unlock();
        }
    }

    public boolean isEmpty() {
        lock.lock();
        try {
            return items.isEmpty();
        } finally {
            lock.unlock();
        }
    }
}

class Loader extends Thread {
    private final Warehouse warehouse;
    private final int id;
    private static final int maxTotalWeight = 150;
    private static int currentTotalWeight = 0;
    private static final ReentrantLock weightLock = new ReentrantLock();

    public Loader(int id, Warehouse warehouse) {
        this.id = id;
        this.warehouse = warehouse;
        setName("Грузчик_" + id);
    }

    @Override
    public void run() {
        List<Item> currentBatch = new ArrayList<>();
        int currentWeight = 0;

        while (true) {
            Item item = warehouse.takeItem();
            if (item == null) {
                if (!currentBatch.isEmpty()) {
                    unload(currentBatch, currentWeight);
                }
                System.out.println(getName() + " завершил перегрузку.");
                break;
            }

            weightLock.lock();
            try {
                if (currentTotalWeight + item.getWeight() > maxTotalWeight) {
                    if (!currentBatch.isEmpty()) {
                        unload(currentBatch, currentWeight);
                        currentTotalWeight -= currentWeight;
                        currentBatch = new ArrayList<>();
                        currentWeight = 0;
                    }
                    
                    if (currentTotalWeight + item.getWeight() > maxTotalWeight) {
                        continue;
                    }
                }
                
                currentBatch.add(item);
                currentWeight += item.getWeight();
                currentTotalWeight += item.getWeight();
                System.out.println(getName() + " загрузил: " + item + ", вес: " + currentWeight + " кг, общий вес грузчиков: " + currentTotalWeight + " кг");
            } finally {
                weightLock.unlock();
            }
        }
    }

    private void unload(List<Item> batch, int weight) {
        System.out.println(getName() + " разгрузил " + weight + " кг");
    }
}

public class Storage {
    public static void main(String[] args) {
        List<Item> items = Arrays.asList(
            new Item("Ящики", 40),
            new Item("Мешки", 30),
            new Item("Коробки", 20),
            new Item("Бочки", 60),
            new Item("Паллеты", 100),
            new Item("Канистры", 25),
            new Item("Мебель", 80),
            new Item("Электроника", 15),
            new Item("Стекло", 50),
            new Item("Одежда", 10),
            new Item("Книги", 35),
            new Item("Инструменты", 45),
            new Item("Golikov", 72)
        );

        Warehouse warehouse = new Warehouse(items);

        Loader loader1 = new Loader(1, warehouse);
        Loader loader2 = new Loader(2, warehouse);
        Loader loader3 = new Loader(3, warehouse);

        loader1.start();
        loader2.start();
        loader3.start();

        try {
            loader1.join();
            loader2.join();
            loader3.join();
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }

        System.out.println("Перегрузка завершена.");
    }
}