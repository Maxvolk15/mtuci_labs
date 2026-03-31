import java.util.*;

public class MUS {

    public static int[] mergeUniqueSorted(int[] a, int[] b) {
        Set<Integer> set = new TreeSet<>();
        
        for (int num : a) {
            set.add(num);
        }
        
        for (int num : b) {
            set.add(num);
        }
        
        int[] result = new int[set.size()];
        int index = 0;
        for (int num : set) {
            result[index++] = num;
        }
        
        return result;
    }

    public static void main(String[] args) {
        Scanner scan = new Scanner(System.in);

        String input = scan.nextLine();

        String[] arrays = input.split("\\], \\[");

        String arr1Str = arrays[0].replace("[", "");
        int[] array1 = new int[0];
        if (!arr1Str.trim().isEmpty()) {
            String[] parts1 = arr1Str.split(",");
            array1 = new int[parts1.length];
            for (int i = 0; i < parts1.length; i++) {
                if (!parts1[i].trim().isEmpty()) {
                    array1[i] = Integer.parseInt(parts1[i].trim());
                }
            }
        }

        String arr2Str = arrays[1].replace("]", "");
        int[] array2 = new int[0];
        if (!arr2Str.trim().isEmpty()) {
            String[] parts2 = arr2Str.split(",");
            array2 = new int[parts2.length];
            for (int i = 0; i < parts2.length; i++) {
                if (!parts2[i].trim().isEmpty()) {
                    array2[i] = Integer.parseInt(parts2[i].trim());
                }
            }
        }

        int[] result = mergeUniqueSorted(array1, array2);

        System.out.print("[");
        for (int i = 0; i < result.length; i++) {
            System.out.print(result[i]);
            if (i < result.length - 1) {
                System.out.print(",");
            }
        }
        System.out.println("]");
        
        scan.close();
    }
}