package tasks.task3;

import java.util.*;

public class FilterEven {
    public static void main(String[] args) {
        Scanner scan = new Scanner(System.in);
        String list = scan.nextLine().trim().replace("[", "").replace("]", "");
        String[] list1 = list.split(", ");
        int[] n = new int[list1.length];
        for (int i = 0; i < list1.length; i++) {
            n[i] = Integer.parseInt(list1[i]);
        }
        System.out.println(Arrays.toString(filterEven(n)));
    }

    public static String[] filterEven(int[] n) {
        String nums = "";
        for (int num: n) {
            if (num % 2 == 0) {
                nums += num + " ";
            }
        }
        String[] result = nums.split(" ");
        return result;
    }
}
