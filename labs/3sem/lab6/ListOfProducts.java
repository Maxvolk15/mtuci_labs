package lab6;
import java.util.*;

public class ListOfProducts {
    ArrayList<Table> soldProducts = new ArrayList<>();
    public void addSale(Table product) {
        soldProducts.add(product);
    }

    public void getSoldProducts() {
        if (soldProducts.isEmpty()) {
            System.out.println("Ничего не продано.");
            return;
        }
        System.out.println("Список проданных продуктов:");
        for (int i = 0; i < soldProducts.size(); i++) {
            System.out.println(i + 1 + ". " + soldProducts.get(i));
        }
    }

    public String getTotalSum() {
        double sum = 0;
        for (Table product: soldProducts) {
            sum += product.getPrice();
        }
        return "Общая сумма продаж: " + Math.round(sum * 100.00)/100.00 + " Rub";
    }

    public String getMostSold() {
        if (soldProducts.isEmpty()) {
            System.out.println("Ничего не продано.");
        }

        ArrayList<String> names = new ArrayList<>();
        ArrayList<Integer> counts = new ArrayList<>();

        for (Table p: soldProducts) {
            if (names.indexOf(p.getName()) == -1) {
                names.add(p.getName());
                counts.add(1);
            } else {
                counts.set(names.indexOf(p.getName()), counts.get(names.indexOf(p.getName())) + 1);
            }
        }

        int max = 0;
        for (int c: counts) {
            if (c >= max) max = c;
        }

        return "Наибольшее количество продаж: " + names.get(counts.indexOf(max));
    }

    public static void main(String[] args) {
        ListOfProducts track = new ListOfProducts();
        track.addSale(new Table("Moloko", 15.52));
        track.addSale(new Table("Xleb", 17.2));
        track.addSale(new Table("Moloko", 18.52));
        track.addSale(new Table("Pivo", 30.9));
        track.addSale(new Table("Moloko", 10.1));
        track.addSale(new Table("Pivo", 40));
        System.out.println(track.getMostSold());
        System.out.println(track.getTotalSum());
        track.getSoldProducts();
    }
}

class Table {
    private String name;
    private double price;
    
    public Table(String name, double price) {
        this.name = name;
        this.price = price;
    }

    public String getName() {
        return name;
    }

    public double getPrice() {
        return price;
    }

    @Override
    public String toString() {
        return name + " - " + price + " Rub";
    }
}