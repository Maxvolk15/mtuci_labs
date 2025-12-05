import java.util.*;

public class ConvertToRome {
    public static void main(String[] args) {
        Scanner scan = new Scanner(System.in);
        int n = scan.nextInt();
        System.out.println(convertToRome(n));
    }

    public static String convertToRome(int n) {
        int[] values = {1000, 900, 500, 400, 100, 90, 50, 40, 10, 9, 5, 4, 1};
        String[] nums = {"M", "CM", "D", "CD", "C", "XC", "L", "XL", "X", "IX", "V", "IV", "I"};

        StringBuilder result = new StringBuilder();

        for (int i = 0; i < values.length; i++) {
            while (n >= values[i]) {
                result.append(nums[i]);
                n -= values[i];
            }
        }

        return result.toString();
    }
}