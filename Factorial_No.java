import java.util.Scanner;

public class Factorial_No {
    public static void main(String[] args) {
        Scanner obj = new Scanner(System.in);
        System.out.println("ENTER THE VALUE: ");
        int num = obj.nextInt();
        int fact = 1;
        for (int i = 1; i <= num; i++) {
            fact = fact * i;
        }
        System.out.print("Factorial of " + num + " is " + fact);
    }
}
