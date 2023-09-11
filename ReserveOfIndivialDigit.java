public class ReserveOfIndivialDigit {
    public static void main (String[]arg)
    {
        int num=1234,a,b,c,d,e,f,rev;
        a=num%10;
        b=num/10;
        c=b%10;
        d=b/10;
        e=d%10;
        f=d/10;
        rev=a*1000+c*100+e*10+f;
        System.out.println("THE REVERSE OF INDIVIDUAL DIGIT IS: "+rev);
    }
}

