import java.util.*;

public class NonRepeat {
    public static void main(String[] args) {
        Scanner scan = new Scanner(System.in);
        String n = scan.nextLine().trim();
        System.out.println(nonRepeat(n));
    }

    public static String nonRepeat(String n) {
        Map<Character, Integer> map = new HashMap<>();
        for (int i = 0; i < n.length(); i++) {
            char c = Character.toLowerCase(n.charAt(i));
            map.put(c, map.getOrDefault(c, 0) + 1);
        }

        Set<Character> toRemove = new HashSet<>();
        for (Map.Entry<Character, Integer> entry : map.entrySet()) {
            if (entry.getValue() > 3) {
                toRemove.add(entry.getKey());
            }
        }

        if (toRemove.isEmpty()) {
            return n;
        }

        StringBuilder sb = new StringBuilder();
        for (int i = 0; i < n.length(); i++) {
            if (!toRemove.contains(Character.toLowerCase(n.charAt(i)))) {
                sb.append(n.charAt(i));
            }
        }

        return nonRepeat(sb.toString());
    }
}