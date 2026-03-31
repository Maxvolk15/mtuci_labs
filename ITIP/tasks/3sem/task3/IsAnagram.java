package tasks.task3;

import java.util.*;

public class IsAnagram {
    public static void main(String[] args) {
        Scanner scan = new Scanner(System.in);
        String n = scan.nextLine().trim();
        System.out.println(isAnagram(n));
    }

    public static boolean isAnagram(String n) {
        String[] words = n.split(", ");
        String[] word1 = words[0].split("");
        String[] word2 = words[1].split("");
        Arrays.sort(word1);
        Arrays.sort(word2);
        if (String.join("", word1).equals(String.join("", word2))) {
            return true;
        } else {
            return false;
        }
    }
}
