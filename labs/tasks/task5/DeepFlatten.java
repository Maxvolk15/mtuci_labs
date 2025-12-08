package task5;

import java.util.*;

public class DeepFlatten {
    public static void main(String[] args) {
        Scanner scan = new Scanner(System.in);
        String n = scan.nextLine().trim();
        System.out.println(Arrays.toString(deepFlatten(n)));
    }

    public static String[] deepFlatten(String n) {
        return n.replaceAll("[,\\s\\[\\]]+", "").split("");
    }
}
