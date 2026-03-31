import java.util.Scanner;

public class CEOD {

    public static int[] countEvenOddDigits(int n) {
        int num = Math.abs(n);

        if (num == 0) {
            return new int[]{1, 0};
        }
        
        int evenCount = 0;
        int oddCount = 0;

        while (num > 0) {
            int digit = num % 10;
            if (digit % 2 == 0) {
                evenCount++;
            } else {
                oddCount++;
            }
            num /= 10;
        }
        
        return new int[]{evenCount, oddCount};
    }

    public static void main(String[] args) {
        Scanner scan = new Scanner(System.in);

        int n = scan.nextInt();
        int[] result = countEvenOddDigits(n);

        System.out.println(result[0] + ", " + result[1]);
        
        scan.close();
    }
}