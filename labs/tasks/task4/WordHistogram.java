package task4;

import java.util.*;

public class WordHistogram {
    public static void main(String[] args) {
        Scanner scan = new Scanner(System.in);
        String n = scan.nextLine().replaceAll("\\p{Punct}+", "").toLowerCase();
        System.out.println(wordHistogram(n));
    }

    public static String wordHistogram(String n) {
        String[] s = n.split("\\s+");
        Map<String, Integer> map = new HashMap<>();
        for (String word: s) {
            if (map.containsKey(word)) {
                map.put(word, map.get(word) + 1);
            } else {
                map.put(word, 1);
            }
        }

        List<Map.Entry<String, Integer>> listMap = new ArrayList<>();
        for (Map.Entry<String, Integer> entry: map.entrySet()) {
            listMap.add(entry);
        }
        Collections.sort(listMap, new Comparator<Map.Entry<String, Integer>>() {
            @Override
            public int compare(Map.Entry<String, Integer> o1, Map.Entry<String, Integer> o2) {
                return (int) o2.getValue() - o1.getValue();
            }
        });

        StringBuilder result = new StringBuilder("{");
        boolean first = true;
        for (Map.Entry<String, Integer> entry : listMap) {
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

// package task4;

// import java.util.*;

// public class WordHistogram {
//     public static void main(String[] args) {
//         Scanner scan = new Scanner(System.in);
//         String n = scan.nextLine().replaceAll("\\p{Punct}+", "").toLowerCase();
//         System.out.println(wordHistogram(n));
//     }

//     public static String wordHistogram(String n) {
//         String[] s = n.split("\\s+");
//         Map<String, Integer> map = new LinkedHashMap<>();
//         for (String word: s) {
//             if (map.containsKey(word)) {
//                 map.put(word, map.get(word) + 1);
//             } else {
//                 map.put(word, 1);
//             }
//         }
//         StringBuilder result = new StringBuilder("{");
//         boolean first = true;
//         for (Map.Entry<String, Integer> entry : map.entrySet()) {
//             if (!first) {
//                 result.append(", ");
//             }
//             result.append(entry.getKey()).append(": ").append(entry.getValue());
//             first = false;
//         }
//         result.append("}");

//         return result.toString();
//     }
// }

