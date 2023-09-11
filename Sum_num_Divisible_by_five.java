public class Sum_num_Divisible_by_five {
    public static void main(String[] args) {
        int sum = 0;
        for (int i = 1; i <= 1000; i++) {
            if (i % 5 == 0) {
                sum = sum + i;
            }
        }
        System.out.println("SUM = " + sum);
    }
}
