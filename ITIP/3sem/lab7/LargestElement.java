package lab7;
import java.util.*;
import java.util.concurrent.*;

public class LargestElement {
    public static void main(String[] args) throws InterruptedException, ExecutionException{
        int[][] matrix = {
            {1,  5,  9,  3},
            {7,  2,  8,  6},
            {4, 10,  3, 12},
            {11, 1, 15,  2}
        };

        int row = matrix.length;
        int line = matrix[0].length;

        ExecutorService executor = Executors.newFixedThreadPool(row);
        @SuppressWarnings("unchecked")
        Future<Integer>[] maxResults = new Future[row];

        for (int i = 0; i < row; i++) {
            maxResults[i] = executor.submit(() -> {
                int max = 0;
                for (int j = 0; j < line; j++) {
                    if (max <= matrix[row - 1][j]) {
                        max = matrix[row - 1][j];
                    }
                }
                return max;
            });
        }

        int result = 0;
        for (int i = 0; i < row; i++) {
            int m = maxResults[i].get();
            if (m >= result) {
                result = m;
            }
        }

        executor.shutdown();
        System.out.println("Наибольшее значение матрицы: " + result);
    }
}
