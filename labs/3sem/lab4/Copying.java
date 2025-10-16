package lab4;
import java.nio.file.*;
import java.io.*;

public class Copying {
    public static void main(String[] args) {
        Path file = Paths.get("File.txt");
        Path copy = Paths.get("CopyFile.txt");

        try {
            Files.copy(file, copy, StandardCopyOption.REPLACE_EXISTING);
            System.out.println("Файл File.txt скопирован в CopyFile.txt");
        } catch (NoSuchFileException e) {
            System.out.println("Ошибка: файл " + e.getMessage() + " не найден.");
        } catch (IOException e) {
            System.out.println("Ошибка: " + e.getMessage());
        }
    }
}
// Не сущ файл - выдать ошибку