package lab5;

import java.util.*;
import java.util.regex.*;

public class IPCheck {
    public static void main(String[] args) {
        Scanner scan = new Scanner(System.in);
        System.out.println("IP должен состоять из 4 чисел от 0 до 255, разделённых точками");
        System.out.print("IP: ");
        try {
            String ip = scan.nextLine().trim();
            if (isIPCorrect(ip)) {
                System.out.println("IP корректен");
            } else {
                System.out.println("IP введён неверно");
            }
        } catch (Exception e) {
            System.out.println("Ошибка: " + e.getMessage());
        }
    }

    public static boolean isIPCorrect(String ip) {
        Pattern patt = Pattern.compile("^((((25[0-5])|(2[0-4][0-9])|(1[0-9][0-9])|([1-9][0-9])|[0-9]))\\.){3}((((25[0-5])|(2[0-4][0-9])|(1[0-9][0-9])|([1-9][0-9])|[0-9])))$");
        if (!patt.matcher(ip).matches()) {
            System.out.println("IP должен состоять из 4 чисел от 0 до 255, разделенных точками");
            return false;
        }

        return true;
    }
}
