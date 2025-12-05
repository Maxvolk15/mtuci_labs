import java.util.Scanner;

public class CountIslands {

    public static int countIslands(int[][] grid) {
        if (grid == null || grid.length == 0 || grid[0].length == 0) {
            return 0;
        }

        int rows = grid.length;
        int cols = grid[0].length;
        int islands = 0;

        for (int i = 0; i < rows; i++) {
            for (int j = 0; j < cols; j++) {
                if (grid[i][j] == 1) {
                    islands++;
                    dfs(grid, i, j);
                }
            }
        }

        return islands;
    }

    private static void dfs(int[][] grid, int i, int j) {
        int rows = grid.length;
        int cols = grid[0].length;

        if (i < 0 || j < 0 || i >= rows || j >= cols || grid[i][j] == 0) {
            return;
        }

        grid[i][j] = 0;

        dfs(grid, i - 1, j);
        dfs(grid, i + 1, j);
        dfs(grid, i, j - 1);
        dfs(grid, i, j + 1);
    }

    public static int[][] parseMatrix(String input) {
        input = input.trim();
        if (input.startsWith("[[") && input.endsWith("]]")) {
            input = input.substring(2, input.length() - 2);
        }

        String[] rowStrings = input.split("\\],\\[|\\],|\\[");

        if (input.isEmpty()) {
            return new int[0][0];
        }

        int[][] matrix = new int[rowStrings.length][];

        for (int i = 0; i < rowStrings.length; i++) {
            String row = rowStrings[i].trim();
            if (row.isEmpty()) {
                matrix[i] = new int[0];
                continue;
            }
            String[] numStrings = row.split(",");
            matrix[i] = new int[numStrings.length];
            for (int j = 0; j < numStrings.length; j++) {
                matrix[i][j] = Integer.parseInt(numStrings[j].trim());
            }
        }

        return matrix;
    }

    public static void main(String[] args) {
        Scanner scan = new Scanner(System.in);
        String line = scan.nextLine();

        int[][] grid = parseMatrix(line);
        System.out.println(countIslands(grid));
    }
}