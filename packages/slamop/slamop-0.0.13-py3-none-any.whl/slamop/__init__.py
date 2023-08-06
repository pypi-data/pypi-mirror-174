def p1():
	code="""
college_name="Mount Carmel College"
Course="Science"

class Student:
    def getStudentDetails(ob):
        ob.rollno=input("Enter Roll Number : ")
        ob.name = input("Enter Name : ")
        ob.physics =int(input("Enter Physics Marks : "))
        ob.chemistry = int(input("Enter Chemistry Marks : "))
        ob.maths = int(input("Enter Math Marks : "))

    def printResult(ob):
        ob.percentage = (int)( (ob.physics + ob.chemistry + ob.maths) / 300 * 100 ); 
        
        print("Student Roll Number:",ob.rollno)
        print("Student Name:",ob.name)
        print("Student College:",college_name)
        print("Student Course:",Course)
        print("Student Percentage:",ob.percentage,"%")

S1=Student()
S1.getStudentDetails()

print("Results ")
print("_________________________")
S1.printResult()
"""
	print(code)


def p2():
	code="""
# Adding two numbers
def add(a, b):  
    sum = a + b  
    print(a, "+", b, "=", sum)  
 
# Subtract two numbers
def subtract(a, b):  
    difference = a - b  
    print(a, "-", b, "=", difference)  
 
# Multiply two numbers
def multiply(a, b):  
    product = a * b  
    print(a, "x", b, "=", product)  
 
# Divide two numbers
def divide(a, b):  
    division = a / b  
    print(a, "/", b, "=", division)  
 
# Menu Driven Heading
print("WELCOME TO CALCULATOR\n")  
 
# using the while loop to print menu list  
while True:  
    print("MENU")  
    print("1. Addition of two Numbers")  
    print("2. Difference between two Numbers")  
    print("3. Multiplication of two Numbers")  
    print("4. Division of two Numbers")  
    print("5. Exit")  
    users_choice = int(input("\nEnter your Choice: "))  
 
# based on the users choice the relevant method is called
    if users_choice == 1:  
        print( "\nPERFORMING ADDITION\n")  
        a = int( input("Enter First Number: "))  
        b = int( input("Enter Second Number: "))  
        add(a, b)  
 
    elif users_choice == 2:  
        print( "\nPERFORMING SUBTRACTION\n")  
        a = int( input("Enter First Number: "))  
        b = int( input("Enter Second Number: "))  
        subtract(a, b)  

    elif users_choice == 3:  
        print( "\nPERFORMING MULTIPLICATION\n")  
        a = int( input("Enter First Number: "))  
        b = int( input("Enter Second Number: "))  
        multiply(a, b)  

 
    elif users_choice == 4:  
        print( "\nPERFORMING DIVISION\n")  
        a = int( input("Enter First Number: "))  
        b = int( input("Enter Second Number: "))  
        divide(a, b)  

 
  # exit the while loop
    elif users_choice == 5:  
        break  
     
    else:  
        print( "Please enter a valid Input from the list")
"""	
	print(code)


def p3():
	code="""
import array as arr
a=arr.array("i",[1,2,3,4,2,3,2,4,5,6,71,1,10,12])
print(a)
print("Menu")
print("1.Append")
print("2.Extend")
print("3.Accessing Array")
print("4.Pop")
print("5.Remove")
print("6.Slicing")
print("7.Reverse")
print("8.Count")
print("9.Insert")
print("10. Search")
print("11.exit")
while True:
   
    x=int(input("\n enter your choice:"))
    if x==1:
        print("original list",a)
        a.append(77)
        print("after use of append (),update array is :",a)
        print("--------------")
       
    elif x==2:
            print("original list",a)
            a.extend([21,22,23,24])
            print("after use of extend (),update array is :",a)
            print("--------------")
       
    elif x==3:
            print("original list",a)
            print("element at 2nd index of array is :",a[2])
            print("--------------")
       
    elif x==4:
            print("original list",a)
            a.pop()
            print("update array is :",a)
            print("--------------")
       
    elif x==5:
            print("original list",a)
            a.remove(71)
            print("update array is :",a)
            print("--------------")
       
    elif x==6:
            print("original list",a)
            print("sliced array is :",a[1:3])
            print("sliced array is :",a[:3])
            print("sliced array is :",a[5:])
            print("negative slicing is:",a[-5:-2])
            print("alternative numbers",a[1:5:2])
            print("--------------")
       
    elif x==7:
            print("original list",a)
            a.reverse()
            print("reverse of array",a)
            print("--------------")
       
       
    elif x==8:
            print("original list",a)
            ct=a.count(4)
            print("occurance of element",ct)
            print("--------------")
       
    elif x==9:
            print("original list",a)
            a.insert(4,8)
            print("occurance of element",a)
            print("--------------")
       
    elif x==10:
            print("original list",a)
            x=a.index(10)
            print("serched of element",x)
            print("--------------")
       
    elif x==11:
            print("exiting the program")
            exit(0)
       
    else:
            print("please enter a valid input from the list")
            print("----------")
"""
	print(code)


def p4():
	code="""
class sal:
    def printdetails(ob):
        print("\n\n")
        print("SALARY- DETAILED BREAK UP")
        print("-------------------------")
        print("NAME OF EMPLOYEE : ",name)
        print("BASIC SALARY     : ",basic)
        print("DEARNESS ALLOW.  : ",da)
        print("HOUSE RENT ALLOW.: ",hra)
        print("TRAVEL ALLOW.    : ",ta)
        print("------------------------")
        print("NET SALARY       : ",netpay)
        print("PROVIDENT FUND   : ",pf)
        print("------------------------")
        print("GROSS PAY        : ",grosspay)

print("EMPLOYEE SALARY SLIP")
name=str(input("Enter name of employee: "))
basic=float(input("Enter basic salary: "))
print("1. Manager")
print("2. HR")
print("3. Team Leader")
ch=int(input("Enter your choice: "))
if ch==1:
    da=float(basic*0.50)
    hra=float(basic*0.15)
    pf=float((basic+da)*0.12)
    ta=float(basic*0.075)
    netpay=float(basic+da+hra+ta)
    grosspay=float(netpay-pf)
    s1=sal()
    s1.printdetails();
elif ch==2:
    da=float(basic*0.)
    hra=float(basic*0.)
    pf=float((basic+da)*0.1)
    ta=float(basic*0.0)
    netpay=float(basic+da+hra+ta)
    grosspay=float(netpay-pf)
    s1=sal()
    s1.printdetails();
elif ch==3:
    da=float(basic*0.05)
    hra=float(basic*0.05)
    pf=float((basic+da)*0.10)
    ta=float(basic*0.015)
    netpay=float(basic+da+hra+ta)
    grosspay=float(netpay-pf)
    s1=sal()
    s1.printdetails();
else: print("Invalid entry")
"""
	print(code)


def p5():
	code="""
import random
import math
lower=int(input("Enter Lower Bound:-  "))
upper=int(input("Enter Upper Bound:-  "))
x=random.randint(lower,upper)
print("\n\t You 've only ",
     round(math.log(upper-lower+1,2)),
     "chances to guess the integer! \n")
count=0
while count<=math.log(upper-lower+1,2):
    count+=1
    guess=int(input("Guess a number :- "))
    if x==guess:
        print("Congratulations you did it in ",count,"try")
        break
    elif x>guess:
        print("You guessed too small")
    elif x<guess:
        print("You guessed too high ")

if count>=math.log(upper-lower+1,2):
    print("\n The number is %d "%x)
    print("\n Better luck next time !")
"""
	print(code)


def p6():
	code="""
import os
stack=[]
while True:
    print("Stack Operations")
    print("---------------------------")
    print("1.Push      2.Pop      3.Traverse      6.Exit")
    print()
   
    ch=int(input("Enter your choice: "))
    if ch==1:
        while True:
            a=input("Enter the value to be inserted * to stop: ")
            if a!='*':
                stack.append(int(a))
            else:
                print()
                break
               
    elif ch==2:
        if len(stack)==0:
            print("Empty Stack")
            print()
        else:
            print("The value deleted is: ",stack.pop())
            print("stack after deletion")
            print(stack)
            print()
           
    elif ch==3:
        if len(stack)==0:
            print("Stack Underflow")
            print()
        else:
            print("The stack element is: ",stack)
            print()
           
    elif ch==4:
        print("Exiting....")
        break
   
    else:
        print("\n Invalid Choice")
        print()
"""
	print(code)


def p7():
	code="""
words=("zero","one","two","three","four","five","six","seven","eight","nine")
tenswords=("","ten","twenty","thirty","forty","fifty","sixty","seventy","eighty","ninety")
teenswords=("","eleven","twelve","thirteen","fourteen","fiveteen","sixteen","seventeen","eighteen","nineteen")
while True:
    num=int(input("Enter a number (max 9999): "))
    if num>=0 and num<10000:
        break;
if num==0:
    print("zero")
else:
    thousands=num//1000;
    hundreds=num//100%10;
    tens=num//10%10;
    ones=num%10;
    if thousands>0:
        print("{} thousand ".format(words[thousands]),end='')
    if hundreds>0:
        print("{} hundred".format(words[hundreds]),end='')
    if (thousands>0 or  hundreds>0) and (tens>0 or ones>0):
        print(" and ",end='')
    if tens==1 and ones>0:
        print(teenswords[ones],end='')
    else:
        if tens>0:
            print(tenswords[tens],'',end='')
        if ones>0:
            print(words[ones],end='')
            print()
"""
	print(code)


def p8():
	code="""
country={'Madagascar':'Antananarivo','Marshall Islands':'Majoro','Bahamas':'Nassau','Armenia':'Yerevan','Chile':'Santiago','Norway':'Oslo','Qatar':'Doha','Egypt':'Cairo','Somalia':'Mogadishu','Fiji':'Suwa','Greece':'Athens','Guinea':'Conakey','Taiwan':'Taipei','Kenya':'Nairoba','Yemen':"Sana'a"}
#Display all keys
print("All Country name")
for x in country:
    print(x)
#Dispaly all values
print("\n All Capitals")
for x in country:
    print(country[x])
#Adding items
country["Brazil"]="Janeiro"
#Updated dictionary
print("\n Updated country is: ",country)
#change values
country["Kenya"]="Nairoba"
print("\n Updated country is: ",country)
#removing items
country.pop("Fiji");
print("\n Updated country is: ",country)
#length of dictionary
print("Length of country is: ",len(country))
#copy a dictionary
dict2=country.copy()
#New dictionary
print("\n New country is: ",dict2)
#empties the dictionary
dict2.clear()
print("\n Updated country is: ",dict2)
ch=input("Choose country from list: ")
if ch in country:
    print("The capital of "+ch+" is "+country[ch])
else:
    print("Country not available in list")
"""
	print(code)


def p9():
	code="""
def build_word_freq_dict(text):
    text=text.lower()
    for punctuation in[',','=','.','"','!','?','--','(',')','\n','\r']:
        text=text.replace(punctuation,' ')
        all_words=text.split(" ")
        word_count={}
        for word in all_words:
            current_count=word_count.get(word,0)
            new_count=current_count+1
            word_count[word]=new_count
        return word_count
ge_text=open("sakeena.txt").read()
ge_word_freqs=build_word_freq_dict(ge_text)
for word,count in ge_word_freqs.items():
    if count>5:
        print(word,count)
"""
	print(code)


def p10():
	code="""
import sys
m,n=map(lambda x:int(x),input("Enter the order of matrix A: ").split(' '))
print("Enter matrix A elements one row at a time: ")
A=[list(map(lambda x:int(x),input().split(' ')))for row in range(m)]
p,q=map(lambda x:int(x),input("Enter the order of matrix B: ").split(' '))
print("Enter matrix B elements one row at a time: ")
B=[list(map(lambda x:int(x),input().split(' ')))for row in range(p)]
print("Matrix of order {} by {} : ".format(m,n))
print("\n".join([" ".join(["{:5}".format(value) for value in row])for row in A]))
print("Matrix of order {} by {} : ".format(p,q))
print("\n".join([" ".join(["{:5}".format(value) for value in row])for row in B]))
while 1:
    print("1. Add (A+B)")
    print("2. Subtract (A-B)")
    print("3. Multiply (A*B)")
    print("4. Transpose A~")
    print("5. Exit")
    print()
    choice=int(input("Enter your choice: "))
    if (choice==1) or (choice==2):
        if(m!=p) or (n!=q):
            print("Order of the matrices do not agree. Cannot be addded / subtracted.")
        else:
            if choice==1:
                res=[[A[i][j]+B[i][j] for j in range(n)]for i in range(m)]
                print("Matrix Addition (A+B): ")
            else:
                res=[[A[i][j]-B[i][j] for j in range(n)]for i in range(m)]
                print("Matrix Subtraction (A-B): ")
        print("------------------------------")
        print("\n".join([" ".join(["{:5}".format(value) for value in row]) for row in res]))
    elif(choice==3):
        if(n!=p):
            print("Order of the matrices do not agree. Cannot be multiplied.")
        else:
            res=[[0 for j in range(q)]for i in range(m)]
            for i in range(len(A)):
                for j in range(len(B[0])):
                    for k in range(len(B)):
                        res[i][j]+=A[i][k]*B[k][j]
            print("Matrix Multiplication (A*B): ")
            print("------------------------------")
            print("\n".join([" ".join(["{:5}".format(value) for value in row]) for row in res]))
    elif(choice==4):
        trans=list(list(row[col] for row in A)for col in range(n))
        print("Transpose of matrix A or order {} by {}: ".format(n,m))
        print("\n".join([" ".join(["{:5}".format(value) for value in row]) for row in trans]))
        trans=list(list(row[col] for row in B)for col in range(q))
        print("Transpose of matrix B or order {} by {}: ".format(p,q))
        print("\n".join([" ".join(["{:5}".format(value) for value in row]) for row in trans]))
    elif choice==5:
        print("Quiting")
        sys.exit()
    else:
        print("Wrong choice. Try again")
"""
	print(code)


def p11():
	code="""
import math
import sys
def isPrime(num):
    if num>1:
        for i in range(2,int(math.sqrt(num))+1):
            if (num%i)==0:
                return False
    return True
while True:
    lower=int(input("Enter Lower Range: "))
    upper=int(input("Enter Upper Range: "))
    if lower<=upper and lower>=1:
        count=0
        for num in range(lower,upper+1):
            if isPrime(num):
                count+=1
                print(num)
            if count==0:
                print("No prime numbers between {}".format(lower),"and {}".format(upper))
    else:
        print("Enter Lower Limit<Upper Limit and +ve limits")
    ans=input("Wish to continue(y/n)")
    if ans=="n":
        sys.exit()
"""
	print(code)


def p13():
	code="""
class Date:
    _daysInMonth=[0,31,28,31,30,31,30,31,31,30,31,30,31]
    def __init__(self,d,m,y):
        self.setDate(1,1,1970)
        self.setDate(d,m,y)
   
    def setDate(self,d,m,y):
        if Date.isValid(d,m,y):
            self._day,self._month,self._year=d,m,y
        else:
            print("Invalid date")
           
    def getDay(self):
        return self._day

    def getMonth(self):
        return self._month
   
    def getYear(self):
        return self._year
   
    def print(self):
        print("{}/{}/{}".format(self.getDay(),self.getMonth(),self.getYear()))
       
    def isValid(d,m,y):
        Date._daysInMonth[2]=28
        if y<1 or y>9999:
            return False
       
        if Date.isLeap(y):
            Date._daysInMonth[2]=29
           
        if m<1 or m>12:
            return False
       
        if d<1 or d>Date._daysInMonth[m]:
            return False
       
        return True
   
    def isLeap(y):
        return((y%4==0 and y%100!=0)or(y%400==0))
   
class USDate(Date):
    def __init___(self,d,m,y):
        super().__init__(d,m,y)
       
    def print(self):
        print("{}/{}/{}".format(self.getMonth(),self.getDay(),self.getYear()))
       
d1=Date(1,2,2000)
print("Date in dd/mm/yyyy format: ")
d1.print()

d2=USDate(1,2,2000)
print("Date in US format: ")
d2.print()
"""
	print(code)


def p14():
	code="""
class Bank_Account:
    def __init__(self):
        self.balance=0
        self.acc=int(input("Enter Account no: "))
        self.name=str(input("Enter Name: "))
        print("HELLO!! WELCOME TO DEPOSIT AND WITHDRAWAL MACHINE")
    def deposit(self):
        amount=float(input("\n Enter amount to be deposited: "))
        self.balance+=amount
        print("\n Amount Deposited: ",amount)
       
    def withdraw(self):
        amount=float(input('Enter amount to be withdrawn: '))
        if self.balance>=amount:
            self.balance-=amount
            print("\n You withdraw: ",amount)
        else:
            print("\n Insufficient balance ")
       
    def display(self):
        print("ThankYou")
       
class Bank(Bank_Account):
    def display(self):
        print("\n Account no: ",self.acc)
        print("\n Name: ",self.name)
        print("\n Net Available Balance=",self.balance)
       
s=Bank()
s.deposit()
s.withdraw()
s.display()
"""
	print(code)


def p15():
	code="""
import sqlite3
conn=sqlite3.connect('sample1.db')
cursor=conn.cursor()
table2='''CREATE TABLE EMPLOYEE2(ID int,FIRST_NAME VARCHAR(255),LAST_NAME VARCHAR(255),AGE int, Gender VARCHAR(255),Salary int,dept varchar(25));'''
cursor.execute(table2)

cursor.execute('''INSERT INTO EMPLOYEE2(ID,FIRST_NAME,LAST_NAME,AGE,Gender,Salary,dept)VALUES(101,'Anand','Choubey',25,'M',10000,'HR')''')

cursor.execute('''INSERT INTO EMPLOYEE2(ID,FIRST_NAME,LAST_NAME,AGE,Gender,Salary,dept)VALUES(102,'Mukesh','Sharma',20,'M',9000,'HR')''')

cursor.execute('''INSERT INTO EMPLOYEE2(ID,FIRST_NAME,LAST_NAME,AGE,Gender,Salary,dept)VALUES(103,'Ankit','Pandey',24,'M',6300,'IT')''')

cursor.execute('''INSERT INTO EMPLOYEE2(ID,FIRST_NAME,LAST_NAME,AGE,Gender,Salary,dept)VALUES(104,'Shubha','Singh',26,'F',8000,'IT')''')

cursor.execute('''INSERT INTO EMPLOYEE2(ID,FIRST_NAME,LAST_NAME,AGE,Gender,Salary,dept)VALUES(105,'Tanu','Mishra',24,'F',9000,'b')''')

print("EMPLOYEE TABLE: ")
data=cursor.execute('''SELECT * FROM EMPLOYEE2''')
for row in data:
  print(row)

cursor.execute('''Update employee2 set salary= Salary+5000 WHERE dept='HR';''')
print('\n After Updating ....\n ')

print("EMPLOYEE TABLE: ")
data=cursor.execute('''SELECT * FROM EMPLOYEE2''')
for row in data:
  print(row)

cursor.execute('''DELETE from EMPLOYEE2 where ID=103;''')
print('\n After deleting ....\n')

print('EMPLOYEE TABLE:')
data=cursor.execute('''SELECT * FROM EMPLOYEE2''')
for row in data:
  print(row)

conn.commit()
conn.close()
"""
	print(code)


def p16():
	code="""
from tkinter import *
class MyWindow:
    def __init__(self, win):
        self.lbl1=Label(win, text='First number')
        self.lbl2=Label(win, text='Second number')
        self.lbl3=Label(win, text='Result')
        self.t1=Entry(bd=3) #The size of the border around the indicator
        self.t2=Entry() #The Entry widget is used to accept single-line text strings fr
        self.t3=Entry()
        self.btn1 = Button(win, text='Add')
        self.btn2=Button(win, text='Subtract')
        self.lbl1.place(x=100, y=50)
        self.t1.place(x=200, y=50)
        self.lbl2.place(x=100, y=100)
        self.t2.place(x=200, y=100)
        self.b1=Button(win, text='Add', command=self.add) #It is set to the function ca
        self.b2=Button(win, text='Subtract')
        self.b2.bind('<Button-1>', self.sub) # BUtton-1: Left mouse button click. The
        self.b1.place(x=100, y=150)
        self.b2.place(x=200, y=150)
        self.lbl3.place(x=100, y=200)
        self.t3.place(x=200, y=200)
    def add(self):
        self.t3.delete(0, 'end') # this is used to clear the entry widget
        num1=int(self.t1.get())
        num2=int(self.t2.get())
        result=num1+num2
        self.t3.insert(END, str(result))
    def sub(self, event):
        self.t3.delete(0, 'end')
        num1=int(self.t1.get())
        num2=int(self.t2.get())
        result=num1-num2
        self.t3.insert(END, str(result))
   
window=Tk()
mywin=MyWindow(window)
window.title('This is my first GUI Program')
window.geometry("400x300+10+10")
window.mainloop() 
"""
	print(code)


def p12():
	code="""
def add(a,b):
    c=a+b
    return c
def sub(a,b):
    c=a-b
    return c
def mul(a,b):
    c=a*b
    return c
def div(a,b):
    c=a/b
    return c
def exp(a,b):
    c=a**b
    return c

from arth import add
from arth import sub
from arth import mul
from arth import div
from arth import exp
num1=float(input("Enter first number: "))
num2=float(input("Enter second number: "))
print(("addition is: ",add(num1,num2)))
print(("subtraction is: ",sub(num1,num2)))
print(("multiplication is: ",mul(num1,num2)))
print(("division is: ",div(num1,num2)))
print(("modulus is: ",mod(num1,num2)))
print(("exponent is: ",exp(num1,num2)))
"""
	print(code)


def p17():
	code="""
class complexerror(Exception):
    pass
msg='enter the equation in the form of 1 2 1 if equation is x^2 +2x+ 1: '
print(msg)
k=input()
k=k.strip()
k=list(map(int,k.split()))
try:
    t=k[1]**2-4*k[0]*k[2]
    if(t<0):
        raise complexerror
    else:
        print('roots are: ')
        print((-1*k[1]+float(t)**0.5)/(2*k[0]))
        print((-1*k[1]-float(t)**0.5)/(2*k[0]))
except complexerror:
    print('roots are imaginary')
finally:
    print('The values of variables satisfying the given quadratic equation are called its roots')
"""
	print(code)	

