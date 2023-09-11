import java.util.Scanner;
public class Grading_Code {
    public static void main(String[]arg){
        Scanner myobj= new Scanner(System.in);
                System.out.println("ENTER THE SUBJECT MARKS M1: ");
        int m1= myobj.nextInt();
        System.out.println("ENTER THE SUBJECT MARKS M2: ");
        int m2= myobj.nextInt();
        System.out.println("ENTER THE SUBJECT MARKS M3: ");
        int m3= myobj.nextInt();
        System.out.println("ENTER THE SUBJECT MARKS M4: ");
        int m4= myobj.nextInt();
        System.out.println("ENTER THE SUBJECT MARKS M5: ");
        int m5= myobj.nextInt();
       int  Avg=(m1+m2+m3+m4+m5)/5;
        if(Avg>=90){
            System.out.println("GRADE :A ");}
        else if(Avg<=80&&Avg>89){
            System.out.println("GRADE :B ");
        }
        else if(Avg<70&&Avg>79){
            System.out.println("GRADE :C ");
        }
        else{
            System.out.println("GRADE :D ");
        }
        }
    }

