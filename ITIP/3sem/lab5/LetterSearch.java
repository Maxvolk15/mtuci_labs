package lab5;

import java.util.*;
import java.util.regex.*;

public class LetterSearch {
    public static void main(String[] args) {
        Scanner scan = new Scanner(System.in);
        System.out.print("Текст: ");
        String text = scan.nextLine().trim();

        Pattern patt = Pattern.compile("[a-z][A-Z]");
        Matcher match = patt.matcher(text);
        StringBuilder result = new StringBuilder();
        while (match.find()) {
            String replace = "!" + match.group() + "!";
            match.appendReplacement(result, replace);
        }
        match.appendTail(result);

        System.out.println("Результат:");
        System.out.println(result.toString());
    }
}
