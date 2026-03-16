package tasks.task3;

import java.util.*;

public class DifferenceMaxMin {
    public static void main(String[] args) {
        Scanner scan = new Scanner(System.in);
        String list = scan.nextLine().trim().replace("[", "").replace("]", "");
        String[] list1 = list.split(", ");
        int[] n = new int[list1.length];
        for (int i = 0; i < list1.length; i++) {
            n[i] = Integer.parseInt(list1[i]);
        }
        System.out.println(differenceMaxMin(n));
    }

    public static int differenceMaxMin(int[] n) {
          Arrays.sort(n);
          return n[n.length - 1] - n[0];
    }
}