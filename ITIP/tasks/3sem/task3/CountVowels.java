package tasks.task3;

import java.util.Scanner;

public class CountVowels {
    public static void main(String[] args) {
        Scanner scan = new Scanner(System.in);
        String n = scan.nextLine().trim();
        System.out.println(countVowles(n));
    }

    public static int countVowles(String n) {
        String[] words = {"a", "e", "i", "o", "u"};
        int result = 0;
        String[] word  = n.split("");
        for (String letter1: word) {
            for (String letter: words) {
                if (letter1.toLowerCase().equals(letter) || letter1.toUpperCase().equals(letter)) {
                    result++;
                }
            }
        }
        return result;
    }
}
