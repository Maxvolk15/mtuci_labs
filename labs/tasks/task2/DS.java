import java.util.Scanner;

public class DS {

    public static int diagonalSum(int[][] matrix) {
        int sum = 0;
        for (int i = 0; i < matrix.length; i++) {
            sum += matrix[i][i];
        }
        return sum;
    }

    public static void main(String[] args) {
        Scanner scan = new Scanner(System.in);
        
        String input = scan.nextLine().trim();
        String n = input.substring(1, input.length() - 1);
        String[] rows = n.split("\\],\\[");
        int[][] matrix = new int[rows.length][rows.length];
        
        for (int i = 0; i < rows.length; i++) {
            String row = rows[i].replace("[", "").replace("]", "");
            String[] elements = row.split(",");
            for (int j = 0; j < elements.length; j++) {
                matrix[i][j] = Integer.parseInt(elements[j].trim());
            }
        }


        System.out.println(diagonalSum(matrix));
        
        scan.close();
    }
}