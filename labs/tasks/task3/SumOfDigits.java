package tasks.task3;

import java.util.Scanner;

public class SumOfDigits {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        int n = scanner.nextInt();
        scanner.close();
        System.out.println(digitSum(n));
    }

    public static int digitSum(int n) {
        int result = 0;
        while (n > 0) {
            int digit = n % 10;
            result += digit;
            n /= 10;
        }
        return result;
    }
}
