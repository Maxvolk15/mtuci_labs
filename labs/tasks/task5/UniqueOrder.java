import java.util.*;

public class UniqueOrder {
    public static void main(String[] args) {
        Scanner scan = new Scanner(System.in);
        String n = scan.nextLine();
        System.out.println(uniqueOrder(n));
    }

    public static String uniqueOrder(String n) {
        ArrayList<String> list = new ArrayList<>();
        for (String letter: n.split("")) {
            if (!list.contains(letter)) {
                list.add(letter);
            }
        }
        return String.join("", list);
    }
}