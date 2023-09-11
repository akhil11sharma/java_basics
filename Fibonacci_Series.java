import java.util.Scanner;

public class Fibonacci_Series {
    public static void main(String[] args) {
        Scanner obj = new Scanner(System.in);
        System.out.println("Enter the Number: ");

        int num = obj.nextInt();
        int a = 0;
        int b = 1;

        System.out.print("THE FIBONACCI SERIES IS: " + a + " " + b);

        for (int i = 3; i <= num; i++) {
            int c = a + b;
            System.out.print(" " + c);
            a = b;
            b = c;
        }
    }
}

