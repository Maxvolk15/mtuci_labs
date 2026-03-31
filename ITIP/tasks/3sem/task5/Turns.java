package tasks.task5;
import java.util.*;


public class Turns {
    public static void main(String[] args) {
        Scanner scan = new Scanner(System.in);
        int n = scan.nextInt();
        System.out.println(turns(n));
    }

    public static int turns(int n) {
        int result = 0;
        boolean flag = true;
        String s = Integer.toString(n);
        if (s.charAt(0) - s.charAt(1) > 0) {
            flag = false;
        }

        for (int i = 0; i < s.length() - 1; i++) {
            if ((s.charAt(i) - s.charAt(i + 1) > 0) && (flag == true)) {
                result++;
                flag = false;
            } if ((s.charAt(i) - s.charAt(i + 1) < 0) && (flag == false)) {
                result++;
                flag = true;
            }
        }
        
        return result;
    }
}