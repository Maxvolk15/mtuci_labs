package task5;
import java.util.*;

public class FindShift {
    public static void main(String[] args) {
        Scanner scan = new Scanner(System.in);
        String n = scan.nextLine().trim().replaceAll("[^a-zA-Z,]", "");
        System.out.println(findShift(n));
    }

    public static int findShift(String n) {
        String[] s = n.split(",");

        String a = s[0];
        String b = s[1];
        
        if (a.length() != b.length()) {
            return -1;
        }

        if (a.length() == 0) {
            return 0;
        }
        
        int shift = (b.charAt(0) - a.charAt(0) + 26) % 26;
        
        for (int i = 0; i < a.length(); i++) {
            char expected = (char) ((a.charAt(i) - 'a' + shift) % 26 + 'a');
            if (b.charAt(i) != expected) {
                return -1;
            }
        }
        
        return shift;
    }
}
