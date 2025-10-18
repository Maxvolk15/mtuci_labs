import java.util.Scanner;

public class HD {
    public static void main(String[] args) {
        Scanner scan = new Scanner(System.in);
        String input = scan.nextLine();
        String[] nums = input.split(", ");
        int[] n = new int[nums.length];
        for (int i = 0; i < nums.length; i++) {
            n[i] = Integer.parseInt(nums[i].trim());
        }

        scan.close();
        System.out.println(hasDuplicates(n));
    }

    public static boolean hasDuplicates(int[] n) {
        int sum = 0;
        if (n.length == 0) {
            return false;
        }

        for (int a : n) {
            for (int b : n) {
                if (a == b) {
                    sum++;
                }
            }
        }
        if (sum == n.length) {
            return false;
        } else {
            return true;
        }
    }
    
}
