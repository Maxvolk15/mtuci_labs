package tasks.task5;
import java.util.*;

public class SameLetterPattern {
    public static void main(String[] args) {
        Scanner scan = new Scanner(System.in);
        String n = scan.nextLine().trim();
        System.out.println(sameLetterPattern(n));
    }

    public static boolean sameLetterPattern(String n) {
        String[] s = n.replaceAll("[^a-zA-Z,\"]", "").split(",");
        if (s.length != 2) {
            return false;
        }
        
        String s1 = s[0];
        String s2 = s[1];
        
        if (s1.length() != s2.length()) {
            return false;
        }
        
        Map<Character, Integer> map1 = new HashMap<>();
        Map<Character, Integer> map2 = new HashMap<>();
        
        int id1 = 0;
        int id2 = 0;
        
        for (int i = 0; i < s1.length(); i++) {
            char c1 = s1.charAt(i);
            char c2 = s2.charAt(i);
            
            if (!map1.containsKey(c1)) {
                map1.put(c1, id1++);
            }
            if (!map2.containsKey(c2)) {
                map2.put(c2, id2++);
            }
            
            if (!map1.get(c1).equals(map2.get(c2))) {
                return false;
            }
        }
        
        return true;
    }
}