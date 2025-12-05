import java.util.*;

public class EvaluateGrades {
    public static void main(String[] args) {
        Scanner scan = new Scanner(System.in);
        String s = scan.nextLine();
        if (s.equals("[]")) {
            System.out.println("{}");
        } else {
            String[] n = s.replace("[", "").replace("]", "").split(",");
            System.out.println(evaluateGrades(n));
        }
    }

    public static String evaluateGrades(String[] n) {
        String[] marks = new String[n.length];
        for (int i = 0; i < n.length; i++) {
            int num = Integer.parseInt(n[i]);
            if (num >= 90 && num <= 100) { marks[i] = "A";}
            if (num >= 80 && num <= 89) { marks[i] = "B";}
            if (num >= 70 && num <= 79) { marks[i] = "C";}
            if (num >= 60 && num <= 69) { marks[i] = "D";}
            if (num >= 0 && num <= 59) { marks[i] = "F";}
        }

        Map<String, Integer> map = new LinkedHashMap<>();
        for (String mark: marks) {
            if (map.containsKey(mark)) {
                map.put(mark, map.get(mark) + 1);
            } else {
                map.put(mark, 1);
            }
        }

        StringBuilder result = new StringBuilder("{");
        boolean first = true;
        for (Map.Entry<String, Integer> entry : map.entrySet()) {
            if (!first) {
                result.append(", ");
            }
            result.append(entry.getKey()).append(": ").append(entry.getValue());
            first = false;
        }
        result.append("}");

        return result.toString();
    }
}
