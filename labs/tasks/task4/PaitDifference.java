package task4;

import java.util.*;

public class PaitDifference {
    public static void main(String[] args) {
        Scanner scan = new Scanner(System.in);
        String[] n = scan.nextLine().trim().replaceAll("\\s+", "").replace("[", "").replace("]", "").split(",");
        System.out.println(pairDifference(n));
    }

    public static int pairDifference(String[] n) {
        int k = Integer.parseInt(n[n.length-1]);
        int result = 0;
        for (int i = 0; i < n.length - 1; i++) {
            for (int j = 0; j < n.length - 1; j++) {
                if ((Integer.parseInt(n[i]) > Integer.parseInt(n[j])) && (Integer.parseInt(n[i]) - Integer.parseInt(n[j]) == k)) {
                    result++;
                }
            }
        }

        return result;
    }
}
