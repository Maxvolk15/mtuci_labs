package tasks.task5;

import java.util.*;

public class MemeSum {
    public static void main(String[] args) {
        Scanner scan = new Scanner(System.in);
        String n = scan.nextLine().trim().replaceAll("[^\\d,]", "");
        System.out.println(memeSum(n));
    }

    public static String memeSum(String n) {
        String[] s = n.split(",");
        String result = "";
        while (s[0].length() > s[1].length()) {
            s[1] = "0" + s[1];
        }

        while (s[1].length() > s[0].length()) {
            s[0] = "0" + s[0];
        }

        for (int i = 0; i < s[0].length(); i++) {
            int n1 = Integer.parseInt(s[0].split("")[i]);
            int n2 = Integer.parseInt(s[1].split("")[i]);
            int sum = n1 + n2;
            result += sum;
        }

        return result;
    }
}
