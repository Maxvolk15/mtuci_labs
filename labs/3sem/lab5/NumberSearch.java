package lab5;

import java.util.*;
import java.util.regex.*;

public class NumberSearch {
    public static void main(String[] args) {
        String text = "I'm 99.8% sure this is 10% wrong";
        Pattern patt = Pattern.compile("\\d+(?:\\.\\d+)?");
        Matcher match = patt.matcher(text);
        int i = 0;
        System.out.println("Числа в данной строке:");
        while (match.find()) {
            try {
                i++;
                System.out.println(i + ")" + " " + match.group());
            } catch (Exception e) {
                System.out.println("Ошибка: " + e.getMessage());
            }
        }
    }
}
