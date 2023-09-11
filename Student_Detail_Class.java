public class Student_Detail_Class {

    static class Student {
        String name;
        int age;
        long mobileNo;
        int level;

        public Student() {
        }

        public Student(String name, int age, long mobileNo, int level) {
            this.name = name;
            this.age = age;
            this.mobileNo = mobileNo;
            this.level = level;
        }

        void displayStudent() {
            System.out.println("Name: " + this.name);
            System.out.println("Age: " + this.age);
            System.out.println("Mobile No: " + this.mobileNo);
            System.out.println("Level: " + this.level);
        }

        void updateAge() {
            this.age += 2;
        }
    }

    public static void main(String args[]) {

        Student s1 = new Student("Akhil", 19, 1234567891, 10);
        Student s2 = new Student("Mohit", 20, 1987654321, 11);

        s1.updateAge();
        s2.updateAge();

        s1.displayStudent();
        s2.displayStudent();
    }
}
