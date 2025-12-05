package task4;

import java.util.*;

public class BruteForce {
    public static void main(String[] args) {
        Scanner scan = new Scanner(System.in);
        String s = scan.nextLine();
        String[] n = s.split(",");
        List<String> res = bruteForce(Integer.parseInt(n[0]), Integer.parseInt(n[1]));
        System.out.print("[");
        for (int i = 0; i < res.size(); i++) {
            System.out.print("\"" + res.get(i) + "\"");
            if (i < res.size() - 1) System.out.print(",");
        }
        System.out.println("]");
    }

    public static List<String> bruteForce(int n, int k) {
        if (n > k) return new ArrayList<>();
        List<String> result = new ArrayList<>();
        if (n == 0) {
            result.add("");
            return result;
        }
        for (int i = 0; i < k; i++) {
            char c = (char) ('0' + i);
            for (String s : bruteForce(n - 1, k)) {
                if (!s.contains(String.valueOf(c))) {
                    result.add(c + s);
                }
            }
        }

        return result;
    }
}
