package lab4;

class CustomDivisionException extends Exception{
    public CustomDivisionException(String message){
        super(message);
    }
}

public class DivisionOnZero {
    public static double divide(double a, double b) throws CustomDivisionException {
        if (b==0) {
            throw new CustomDivisionException("Ошибка: деление на ноль.");
        }
        return a/b;
    }

    public static void main(String[] args) {
        try {
            double result = divide(10, 0);
            System.out.println("Результат деления: " + result);
        } catch (CustomDivisionException e) {
            System.out.println(e.getMessage());
        } catch (Exception e) {
            System.out.println("Ошибка: " + e.getMessage());
        }
    }
}