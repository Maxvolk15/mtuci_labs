import java.util.Scanner;

public class C {

    public static int clamp(int value, int min, int max) {
        if (value < min) {
            return min;
        } else if (value > max) {
            return max;
        } else {
            return value;
        }
    }

    public static void main(String[] args) {
         Scanner scan = new Scanner(System.in);
        String input = scan.nextLine();
        String[] numbers = input.split(", ");
        
        int value = Integer.parseInt(numbers[0].trim());
        int min = Integer.parseInt(numbers[1].trim());
        int max = Integer.parseInt(numbers[2].trim());
        scan.close();
        
        System.out.println(clamp(value, min, max));
        
        scan.close();
    }
}