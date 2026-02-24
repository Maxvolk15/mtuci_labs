package tasks.task5;

import java.util.*;

public class IsLandscape {
    public static void main(String[] args) {
        Scanner scan = new Scanner(System.in);
        String n = scan.nextLine().trim();
        System.out.println(isLandscape(n));
    }

    public static boolean isLandscape(String n) {
        String s = n.replaceAll("[^\\d]", "");

        if (s.length() < 3) {
            return false;
        }

        for (int i = 0; i < s.length() - 1; i++) {
            if (s.charAt(i) == s.charAt(i + 1)) {
                return false;
            }
        }

        int i = 0;
        while (i < s.length() - 1 && s.charAt(i) < s.charAt(i + 1)) {
            i++;
        }

        if (i == 0 || i == s.length() - 1) {
            return false;
        }

        while (i < s.length() - 1 && s.charAt(i) > s.charAt(i + 1)) {
            i++;
        }

        return i == s.length() - 1;
    }
}
