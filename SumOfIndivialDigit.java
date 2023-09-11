public class SumOfIndivialDigit {
    public static void main (String[]arg)
    {
        int num=1234,a,b,c,d,e,f,sum;
        a=num%10;
        b=num/10;
        c=b%10;
        d=b/10;
        e=d%10;
        f=d/10;
        sum=a+c+e+f;
        System.out.println("THE SUM OF INDIVIDUAL DIGIT IS: "+sum );
    }
}
