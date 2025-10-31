package lab5;

import java.util.*;
import java.util.regex.*;

public class WordsSearch {
    public static void main(String[] args) {
        Scanner scan = new Scanner(System.in);
        try {
            System.out.print("Текст: ");
            String text = scan.nextLine().trim();
            System.out.print("Буква: ");
            String letter = scan.nextLine().trim();
            wordsFinder(text, letter); //Добавить обработку ошибки, когда текст или буква пусты
        } catch (Exception e) {
            System.out.println("Ошибка: " + e.getMessage());
        }
    }

    public static void wordsFinder(String text, String letter) {
        if (letter.length() == 0) {
            System.out.println("Буква не указана");
            return;
        }
        Pattern patt = Pattern.compile("\\b[" + letter.toLowerCase() + letter.toUpperCase() + "][a-zA-Z]*\\b");
        Matcher match = patt.matcher(text);
        System.out.println("Слова в тексте, начинающиеся на букву " + letter + ": ");
        boolean flag = true;
        while (match.find()) {
            System.out.println(match.group());
            flag = false;
        }

        if (flag) {
            System.out.println("Слова в тексте, начинающиеся на букву " + letter + " не найдены");
        }
    }
}
