package lab1;

public class Palindrome {
    public static void main(String[] args) {
        for (int i = 0; i < args.length; i++) {
            String s = args[i];
            System.out.println("Слова " + s + " и " + reverseString(s) + " палиндромы? -- " + isPalindrome(s));
        }
    }

    public static String reverseString(String s) {
        String revString = "";
        for (int i = s.length()-1; i >= 0; i--) {
            revString += s.charAt(i);
        }
        return revString;
    }

    public static boolean isPalindrome(String s) {
        return s.equals(reverseString(s));
    }
}