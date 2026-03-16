import java.util.Scanner;

public class SOP {
    public static void main(String[] args) {
        Scanner scan = new Scanner(System.in);
        String input = scan.nextLine();
        String[] nums = input.split(", ");
        int[] n = new int[nums.length];
        for (int i = 0; i < nums.length; i++) {
            n[i] = Integer.parseInt(nums[i].trim());
        }

        scan.close();
        System.out.println(sumOfPositives(n));
    }

    public static int sumOfPositives(int[] n) {
        int res = 0;
        for (int num : n) {
            if (num > 0) {
                res += num;
            }
        }
        return res;
    }
    
}
