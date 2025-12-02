package task4;

import java.util.*;

public class Decode {
    public static void main(String[] args) {
        Scanner scan = new Scanner(System.in);
        String s = scan.nextLine().replace("\"", "");
        String[] n = s.split(",");
        System.out.println(Arrays.toString(decode(n)));
    }

    public static int[] decode(String[] n) {
        String text = n[0];
        String key = n[1];
        int s = text.length();
        int[] result = new int[s];
        for (int i = 0; i < s; i++) {
            int t = text.charAt(i) - 'A' + 1;
            int k = key.charAt(i) - 'A' + 1;
            result[i] = t ^ k;
        }
        return result;
    }
}
