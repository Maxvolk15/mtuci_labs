package task4;

import java.util.*;

public class DigitHistogram {
    public static void main(String[] args) {
        Scanner scan = new Scanner(System.in);
        int n = scan.nextInt();
        System.out.println(Arrays.toString(digitHistogram(n)).replaceAll("\\s+", ""));
    }

    public static int[] digitHistogram(int n) {
        int[] result = {0,0,0,0,0,0,0,0,0,0};
        while (n>0) {
            result[n%10] += 1;
            n /= 10;
        }

        return result;
    }
}
