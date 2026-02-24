package tasks.task3;

import java.util.*;

public class CountWords {
    public static void main(String[] args) {
        Scanner scan = new Scanner(System.in);
        String n = scan.nextLine().trim();
        System.out.println(countWords(n));
    }

    public static int countWords(String n) {
        String[] words = n.split("\\s+");
        return words.length;
    }
}
