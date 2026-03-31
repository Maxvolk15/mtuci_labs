package tasks.task3;

import java.util.*;

public class IsTriangle {
    public static void main(String[] args) {
        Scanner scan = new Scanner(System.in);
        String nums = scan.nextLine().trim();
        String[] nums1 = nums.split(", ");
        int[] n = new int[nums1.length];
        for (int i = 0; i < nums1.length; i++) {
            n[i] = Integer.parseInt(nums1[i]);
        }
        System.out.println(isTriangle(n));
    }

    public static boolean isTriangle(int[] n) {
        if (n[0] < (n[1] + n[2]) && n[1] < (n[0] + n[2]) && n[2] < (n[0] + n[1])) {
            return true;
        } else {
            return false;
        }
    }
}
