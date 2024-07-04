import mysql.connector
mydb=mysql.connector.connect (
    host="localhost",
    user="root",
    password="Root@123",
    database="payment"
)
cursor =mydb.cursor()
import datetime
import csv
filename="payment.csv"
with open(filename,'r')as csvfile:
    csvreader=csv.reader(csvfile)
    a=next(csvreader)
    for row in csvreader:
        print(row)
        Payment_id=int(row[0])
        Date_of_Transaction = str(row[1])
        Donar_ID=int(row[2])
        Donar_name=(row[3])
        Amount=int(row[4])
        Transaction_ID=row[5]
       
        sql= "INSERT INTO PaymentDetails(Payment_id,Date_of_transaction,Donar_ID,Donar_name,Amount,Transaction_ID)VALUES(%s,%s,%s,%s,%s,%s)"
        val=(Payment_id,Date_of_Transaction,Donar_ID,Donar_name,Amount,Transaction_ID)
        cursor.execute(sql,val)
mydb.commit()