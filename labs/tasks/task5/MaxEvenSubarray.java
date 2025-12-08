
import java.util.*;

public class MaxEvenSubarray {
    public static void main(String[] args) {
        Scanner scan = new Scanner(System.in);
        String n = scan.nextLine().trim().replaceAll("[^\\d,]", "");
        System.out.println(maxEvenSubarray(n));
    }

    public static int maxEvenSubarray(String n) {
        int[] s = new int[n.split(",").length];
        int max = 0;
        for (int i = 0; i < n.split(",").length; i++) {
            s[i] = Integer.parseInt(n.split(",")[i].trim());
            max += Integer.parseInt(n.split(",")[i].trim());
        }

        int result = 0;
        boolean flag = false;

        for (int i = 0; i < s.length; i++) {
            int check = 0;
            for (int j = i; j < s.length; j++) {
                check += s[j];
                if ((check % 2 == 0) && (check != max)) {
                    flag = true;
                    if (check > result) {
                        result = check;
                    }
                }
            }
        }

        if (flag) {
            return result;
        } else {
            return 0;
        }
    }
}
