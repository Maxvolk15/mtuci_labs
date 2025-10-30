package lab5;

import java.util.*;
import java.util.regex.*;

public class Password {
    public static void main(String[] args) {
        Scanner scan = new Scanner(System.in);
        System.out.println("Введите пароль по данным требованиям: ");
        System.out.println("1) Пароль состоит из латинских букв и цифр");
        System.out.println("2) В пароле должна быть хотя бы 1 заглавная буква и 1 цифра");
        System.out.println("3) Длинна пароля от 8 до 16 символов");
        try {
            System.out.print("Пароль: ");
            String password = scan.nextLine().trim();
            if (isPasswordCorrect(password)) {
                System.out.println("Пароль введён правильно");
            } else {
                System.out.println("Пароль не подходит");
            }
        } catch (Exception e) {
            System.out.println("Ошибка: " + e.getMessage());
        }
    }

    public static boolean isPasswordCorrect(String password) {
        if (password.length() < 8 || password.length() > 16) {
            System.out.println("Пароль меньше 8 или больше 16 символов");
            return false;
        }

        Pattern patt1 = Pattern.compile("^[a-zA-Z0-9]+$");
        if (!patt1.matcher(password).matches()) {
            System.out.println("Пароль состоит не только из латинских букв и цифр");
            return false;
        }

        Pattern patt2 = Pattern.compile("[A-Z]");
        Pattern patt3 = Pattern.compile("[0-9]");
        if (!patt2.matcher(password).find() || !patt3.matcher(password).find()) {
            System.out.println("Пароль не содержит заглавную букву или цифру");
            return false;
        }

        return true;
    }
}
