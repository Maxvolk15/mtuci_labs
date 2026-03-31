package tasks.task3;

import java.util.*;

public class Fibonacci {
    public static void main(String[] args) {
        Scanner scan = new Scanner(System.in);
        int n = scan.nextInt();
        System.out.println(fibonacci(n));
    }

    public static int fibonacci(int n) {
        if (n == 0) {  
            return 0;  
        } else if (n == 1) {  
            return 1;  
        } else {  
            return fibonacci(n - 1) + fibonacci(n - 2);  
        }  
    }
}
