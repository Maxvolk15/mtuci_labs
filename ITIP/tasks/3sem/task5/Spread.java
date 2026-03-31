package tasks.task5;

import java.util.*;

public class Spread {
    public static void main(String[] args) {
        Scanner scan = new Scanner(System.in);
        String n = scan.nextLine().trim().replaceAll("[^\\d,]", "");
        System.out.println(spread(n));
    }

    public static double spread(String n) {
        int[] s = new int[n.split(",").length];
        double mid = 0;
        for (int i = 0; i < n.split(",").length; i++) {
            s[i] = Integer.parseInt(n.split(",")[i].trim());
            mid += Integer.parseInt(n.split(",")[i].trim());
        }
        mid /= s.length;

        return (s[s.length - 1] - s[0]) / mid;
    }
}
