import java.util.Scanner;

public class SR {
    public static void main(String[] args) {
        Scanner scan = new Scanner(System.in);
        String input = scan.nextLine();
        String[] numbers = input.split(", ");
        
        int a = Integer.parseInt(numbers[0].trim());
        int b = Integer.parseInt(numbers[1].trim());
        scan.close();
        System.out.println(sumRange(a, b));
    }

    public static int sumRange(int a, int b) {
        int res = 0;
        for (int i = a; i <= b; i++) {
            res += i;
        }
        return res;
    }
    
}
