package task3;

import java.util.Scanner;

public class ReverseWords {
    public static void main(String[] args) {
        Scanner scan = new Scanner(System.in);
        String n =  scan.nextLine().trim();
        System.out.println(reverseWords(n));
    }

    public static String reverseWords(String n) {
        String[] words = n.split(" ");
        String[] reverse = new String[words.length];
        for (int i = 0; i < words.length; i++) {
            reverse[i] = words[words.length - i - 1];
        }
        return String.join(" ", reverse);
    }
}