import java.util.Scanner;
public class Check_Positive_Negative {
    public static void main(String[] arg) {
        Scanner myobj = new Scanner(System.in);
        System.out.println("Enter any number:");
        int num=myobj.nextInt();
        if (num > 0) {
            System.out.println("POSITIVE");
        }
        else if  (num < 0) {
            System.out.println("NEGATIVE");
        }
        else  {
            System.out.println("VALUE IS ZERO");
        }
    }
}
