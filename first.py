"""#var = "fu babe"
#print(f"what i have to say is {var}")
#em = "johan@gmail.cpm"
#print (f"hit me up on {em}")
age = 1.76
age = int(age)
print(age)
nm =  input ("name?: ")
print (f"hello {nm}")
radius = float( input("Enter the radius of a n"))
area = math.pi * pow(radius,2)
print(f"area of the circle is {area} sq units")
print("py calc")
num1= float(input ("1st number "))
op = input("whats the operation (type + - * / % ) ")
num2 = float(input("input the next number "))
if op == "+" :
    ans = num1 + num2
    print (round(ans,2))
elif op == "-":
    ans= num1 - num2
    print (round(ans,2))
elif op == "*":
    ans = num1 * num2
    print (round(ans,2))
elif op == "/":
    if num2 != 0:
        ans = num1 / num2
        print (round(ans,2))
    else:
        ans= "invalid division"
        print(ans)    
elif op == "%":
    ans = num1 % num2
    print (round(ans,2))
else :
    ans ="invalit op pls try again "
    print(ans)
import math
ops = float(input("enter what to want u to convert, press 1 for pound to kgs, 2 for kg to pound "))
if ops ==1:
    lbs = float(input ("input the pound value "))
    kgs = lbs * 0.453592
    print(f"{lbs} lbs is {round(kgs,2)} kgs")
elif ops==2: 
    kgs = float(input ("input the kgs value "))
    lbs = kgs / 0.453592
    print(f"{kgs} kgs is {round(lbs,2)} lbs")
inp = float(input("num? "))
result = "even" if inp %2==0 else "odd"
print (result)
usr=input("enter user name ")
if len(usr) >12:
    print("user name cant be more than 12 chars")
elif not  usr.find(" ")== -1:
    print("username cant have spaces")
elif not usr.isalpha() :
    print("not numbers")
else :
    print("welcome ")
crd_no = input("enter card number")
last=crd_no[-4:]
print (f"card num is  XXXX-XXXX-XXXX-{last}")
crdno_2e=int(crd_no[::-1])
print(f"card no in reverse encryp is {crdno_2e:+,.2f}") 

name=input("enter your name ")
while len(name)<2 or name=="   ":
    print("wrong try again")
    name=input("enter your name ")
while not name.isalpha() :
    print("wrong try again")
    name=input("enter your name ")
    
print(f"hello {name}!")
print("******************************COMPUND INTREST CALCULATOR******************************")
pamt=0
intrs=0
tym=0
while True :
    pamt=int(input("enter the principle amt in ruppes  "))
    if pamt<=0 :
        print("nuh uh!!!!")
        pamt=int(input("enter the principle amt in ruppes  "))
    else :
        break
while True :
    intrs=int(input("enter the enter the intrest rate  "))
    if intrs<=0 :
        print("nuh uh!!!!")
        intrs=int(input("enter the principle amt in ruppes  "))
    else :
        break

while True :
    tym=int(input("enter the tymk in years  "))
    if tym<=0 :
        print("nuh uh!!!!")
        tym=int(input("enter the principle amt in ruppes  "))
    else :
        break
sum=pamt*pow((1+intrs),tym)
print(sum)"""
acc_bal=232312
intmoney= int(input("enter a valid amount to be transfred "))
if acc_bal>intmoney:
    acc_bal = acc_bal -intmoney
    print(f"money has been successfully tranfred current balance is {acc_bal}")
else :
    print("error 101 inssufficent funds!")