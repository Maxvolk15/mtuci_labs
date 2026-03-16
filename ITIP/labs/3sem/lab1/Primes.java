package lab1;
import java.lang.Math;

public class Primes {
    public static void main(String[] args) {
        for (int num = 2; num < 101; num++) {
            if (isPrime(num)) {
                System.out.print(num + " ");
            }
        }
        System.out.println(" ");
    }

    public static boolean isPrime(int num) {
        for (int i = 2; i <= Math.sqrt(num); i++) {
            if (num % i == 0) {
                return false;
            }
        }
        return true;
    }
}