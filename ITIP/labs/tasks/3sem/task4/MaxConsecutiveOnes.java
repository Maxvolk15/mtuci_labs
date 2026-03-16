import java.util.*;

public class MaxConsecutiveOnes {
    public static void main(String[] args) {
        Scanner scan = new Scanner(System.in);
        String s = scan.nextLine().trim();
        if (s.equals("[]")) {
            System.out.println(0);
        } else {
        String[] n = s.replace("[", "").replace("]", "").split(",");
        System.out.println(maxConsecutiveOnes(n));
        }
    }

    public static int maxConsecutiveOnes(String[] n) {
        int result = 0;
        int count = 0;
        for (String nums: n) {
            int num = Integer.parseInt(nums.trim());
            if (num == 1) { count++; }
            else {
                if (result < count) {
                    result = count;
                }    
                count = 0;
            }
        }
        if (count > result) {return count;}
        else {return result;}
    }
}