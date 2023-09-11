import java.util.Scanner;

public class Salary_Sales {
    public static void main(String[] args) {
        Scanner myobj = new Scanner(System.in);
        System.out.println("ENTER SALES: ");
        int s = myobj.nextInt();
        System.out.println("ENTER SALARY: ");
        int sal = myobj.nextInt();

        if (sal < 10000) {
            s = (int) (0.02 * sal);
        } else if (sal > 10000 && sal < 20000) {
            s = (int) (0.05 * sal);
        } else {
            s = (int) (0.07 * sal);
        }

        System.out.println("SALES COMMISSION: " + s);
    }
}
