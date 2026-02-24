package tasks.task5;
import java.util.*;

public class SkipSevenSum {
    public static void main(String[] args) {
        Scanner scan = new Scanner(System.in);
        int n = scan.nextInt();
        System.out.println(skipSevenSum(n));
    }

    public static int skipSevenSum(int n) {
        int result = 0;

        for (int i = 1; i <= n; i++) {
            if (!checkSeven(i)) {
                result += i;
            }
            
        }

        return result;
    }

    public static boolean checkSeven(int n) {
        while (n>0) {
            if (n % 10 == 7) {
                return true;
            }
            n /= 10;
        }
        return false;
    }
}