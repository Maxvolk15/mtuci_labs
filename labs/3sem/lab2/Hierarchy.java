package lab2;

public class Hierarchy {
    public static void main(String[] args) {
        Animals c1 = new Cat("Mors", "Bad");
        Animals c2 = new Cat("Cvas", "Great");
        Animals p1 = new Parrot("Cracker", "Good");
        Animals f1 = new Fish("Bubble", "Hungry");
        Animals f2 = new Fish("Rockie", "Hungry");
        Animals f3 = new Fish("Shell", "Optimal");
        
        System.out.println(Cat.CountCat());
    }
    static String getCount() {
        return "Общее количество животных: " + (Parrot.CountParrot() + Cat.CountCat() + Fish.CountFish());
    }
}

abstract class Animals {
    abstract String mood();
}

class Cat extends Animals {
    private static int count = 0;
    private String name;
    private String mood;
    public Cat(String name, String mood) {
        this.name = name;
        this.mood = mood;
        count++;
    }
    public static int CountCat() { return count;}

    @Override
    String mood() {
        return "Настроение кота " + name + ": " + mood;
    }
}

class Parrot extends Animals {
    private static int count = 0;
    private String name;
    private String mood;
    public Parrot(String name, String mood) {
        this.name = name;
        this.mood = mood;
        count++;
    }
    public static int CountParrot() { return count;}

    @Override
    String mood() {
        return "Настроение попугая " + name + ": " + mood;
    }
}

class Fish extends Animals {
    private static int count = 0;
    private String name;
    private String mood;
    public Fish(String name, String mood) {
        this.name = name;
        this.mood = mood;
        count++;
    }
    public static int CountFish() { return count;}

    @Override
    String mood() {
        return "Настроение рыбки " + name + ": " + mood;
    }
}