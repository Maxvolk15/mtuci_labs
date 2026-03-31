import java.util.Arrays;
import java.util.Scanner;

public class RR {

    public static int[] rotateRight(int[] arr, int k) {
        if (arr.length == 0) return new int[0];
        k = k % arr.length;
        if (k == 0) return arr;

        int[] result = new int[arr.length];
        for (int i = 0; i < arr.length; i++) {
            result[(i + k) % arr.length] = arr[i];
        }
        return result;
    }

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);

        String input = sc.nextLine().trim();

        String[] parts = input.split("\\],\\s*");


        String numbersPart = parts[0].replace("[", "").replace("]", "").trim();
        int k = Integer.parseInt(parts[1].trim());

        int[] arr;
        if (numbersPart.isEmpty()) {
            arr = new int[0];
        } else {
            String[] numberStrings = numbersPart.split(",\\s*");
            arr = new int[numberStrings.length];
            for (int i = 0; i < numberStrings.length; i++) {
                arr[i] = Integer.parseInt(numberStrings[i]);
            }
        }

        int[] rotated = rotateRight(arr, k);

        System.out.println(Arrays.toString(rotated));
    }
}