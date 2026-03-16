package lab6;

import java.io.*;
import java.util.*;
import java.util.ArrayList;

public class Topword {
    public static void main(String[] args) {
        File file = new File("text.txt");
        Scanner scan = null;
        try {
            scan = new Scanner(file);
        } catch (FileNotFoundException e) {
            e.printStackTrace();
        } catch (Exception e) {
            System.out.println(e.getMessage());
        }

        Map<String, Integer> map = new HashMap<>();
        while (scan.hasNext()) {
            String text = scan.nextLine();
            String[] words = text.split("[\\p{Punct}\\s]+");
            for (String word: words) {
                if (map.containsKey(word)) {
                    map.put(word, map.get(word) + 1);
                } else {
                    map.put(word, 1);
                }
            }
        }

        try {
            scan.close();
        } catch (Exception e) {
            e.printStackTrace();
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

        int i = 0;
        for (Map.Entry<String, Integer> ent: listMap) {
            System.out.println(ent.getKey() + " " + ent.getValue());
            if (i>=10) break;
            i++;
        }
    }   
}
