import java.util.Scanner;

public class CD {
    public static void main(String[] args) {
        Scanner scan = new Scanner(System.in);
        int n = scan.nextInt();
        scan.close();
        System.out.println(countDivisots(n));
    }

    public static int countDivisots(int n) {
        int res = 0;
        for (int i = 1; i <= n; i++) {
            if (n % i == 0) {
                res += 1;
            }
        }
        return res;
    }
    
}
