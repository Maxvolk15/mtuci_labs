package lab4;

import java.nio.file.*;
import java.io.*;

class CustomDivisionException extends Exception{
    public CustomDivisionException(String message){
        super(message);
    }
}

public class DivisionOnZero {
    public static double divide(double a, double b) throws CustomDivisionException {
        if (b==0) {
            throw new CustomDivisionException("Ошибка: деление на ноль.");
        }
        return a/b;
    }

public static void logsError(String message) {
    Path logs = Paths.get("logs.txt");
    try {
        Files.write(logs, message.getBytes(), StandardOpenOption.CREATE, StandardOpenOption.APPEND);

    } catch (IOException e) {
        System.out.println("Ошибка не записана в логи: " + e.getMessage());
    }
}

    public static void main(String[] args) {
        try {
            double result = divide(10, 0);
            System.out.println("Результат деления: " + result);
        } catch (CustomDivisionException e) {
            System.out.println(e.getMessage());
            logsError(e.getMessage() + "\n");
        } catch (Exception e) {
            System.out.println("Ошибка: " + e.getMessage());
            logsError(e.getMessage());
        }
    }
}