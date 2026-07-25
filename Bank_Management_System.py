import random
from datetime import datetime
from getpass import getpass
print("----------BANK----------")
print("----------------------------------\n")
atm = {}
transaction = {}
fd = {}

try:
    with open("atm.txt","r") as file:
        for line in file:
            acc_num,name,balance,pin,last_withdraw_date,today_withdraw_amount= line.strip().split(",")
            atm[int(acc_num)] = [name,float(balance),int(pin),last_withdraw_date,float(today_withdraw_amount)]
except FileNotFoundError:
    pass

def transactions(acc_num,message):
    with open("transaction.txt","a") as file:
        current_time = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        file.write(f"{acc_num},{current_time},{message}\n")

def save_accounts():
    with open("atm.txt","w") as file:
        for acc_num,details in atm.items():
            name,balance,pin,last_withdraw_date,today_withdraw_amount = details
            file.write(f"{acc_num},{name},{balance},{pin},{last_withdraw_date},{today_withdraw_amount}\n")

def create_account():
    name = input("Enter Name : ")
    balance =0
    while True: 
        try:
            pin = int(getpass("Enter 4 digit Pin : "))
            if len(str(pin)) !=4:
                print("Pin must be 4 digits")
            else:
                break
        except ValueError:
            print("Pin must be only in numbers")

    while True:
        try:
            balance = float(input("Enter intial deposit **Minimun ₹5000** : ₹ "))
            if balance < 5000:
                print("Minimum deposit is ₹5000\n")
            else:
                break
        except ValueError:
            print("Enter a Valid Amount\n")
    while True:
        acc_num = random.randint(100000,999999)
        if acc_num not in atm:
            break
    today = datetime.now().strftime("%d-%m-%Y")
    last_withdraw_date = today
    today_withdraw_amount = 0
    atm[acc_num] = [name,balance,pin,last_withdraw_date,today_withdraw_amount]
    print("Account Created Succesfully\n")
    print(f"Your Account Number is : {acc_num}\n")
    print(f"Your Opening Balance is ₹ {balance}\n")
    return name, pin, acc_num

try:
    with open("fd.txt","r") as file:
        for line in file:
            fd_num,acc_num,fd_amount,duration,interest,maturity_amount,created_date = line.strip().split(",")
            fd[int(fd_num)] = [int(acc_num),float(fd_amount),int(duration),float(interest),float(maturity_amount),datetime.fromisoformat(created_date)]
except FileNotFoundError:
    pass

def fd_save():
    with open("fd.txt","w") as file:
        for fd_num,details in fd.items():
            acc_num,fd_amount,duration,interest,maturity_amount,created_date = details
            file.write(f"{fd_num},{acc_num},{fd_amount},{duration},{interest},{maturity_amount},{created_date.isoformat()}\n")

def fd_account():
    acc_num , pin = login()
    balance = atm[acc_num][1]
    name = atm[acc_num][0]
    while True:
        try:
            fd_amount = float(input("Enter FD Amount : ₹"))
            break
        except ValueError:
            print("Amount must be in Numbers!\n")
    if fd_amount <= 0:
        print("Amount should be Greater than 0!\n")
    elif fd_amount > balance:
        print("Insufficient Balance to get FD!\n")
    elif balance - fd_amount <5000:
        print("Minimum Balance is ₹5000\n")
    else:
        print("----FD Interests----\n")
        print("1. 1 - 90 days → 4% interest")
        print("2. 91 - 364 days → 6% interest")
        print("3. More than 365 days → 7% interest\n")
        while True:
            try:
                duration = int(input("Enter Time Period :"))
                
            
                if duration <= 0:
                    print("Time period must be Greater than 0!\n")

                elif duration <=90:
                    print("Interest → 4%")
                    interest = (fd_amount*4*duration) / (100*365)
                    maturity_amount = fd_amount + interest
                    print(f"Your Interest Amount is {interest}\n")
                    print(f"Your Maturity Amount is {maturity_amount}\n")
                    break

                elif duration <=364:
                    print("Interest → 6%")
                    interest = (fd_amount * 6 * duration) / (100*365)
                    maturity_amount = fd_amount + interest
                    print(f"Your Interest Amount is {interest:.2f}\n")
                    print(f"Your Maturity Amount is {maturity_amount:.2f}\n")
                    break

                else:
                    print("Interest → 7%")
                    interest = (fd_amount * 7 * duration) / (100*365)
                    maturity_amount = fd_amount + interest
                    print(f"Your Interest Amount is {interest:.2f}\n")
                    print(f"Your Maturity Amount is {maturity_amount:.2f}\n")
                    
                    break

            except ValueError:
                        print("Time Period must be in Numbers!\n")

        atm[acc_num][1] -= fd_amount
        save_accounts()
        while True:
            fd_num = random.randint(1000,9999)
            if fd_num not in fd:
                break
        print(f"Your FD Number is FD{fd_num}\n")
        created_date = datetime.now()
        fd[fd_num] = [acc_num,fd_amount,duration,interest,maturity_amount,created_date]
        fd_save()
        transactions(acc_num,f"FD created : {fd_amount}")
        print("FD Created Successfully!\n")


def login():
    attempt = 0
    while attempt < 3:
            try: 
                acc_num = int(input("Enter Account Number : "))
                pin = int(getpass("Enter Pin : "))
                if acc_num not in atm:
                        print("Account Not Found!\n")
                elif atm[acc_num][2] != pin:
                        print("Incorrect Pin!\n")
                else:
                        return acc_num , pin
            
            except ValueError:
                print("Invalid Input\n")
            attempt +=1
            print(f"Attempts remaining = {3 - attempt}\n")
        
    print("Attempt Exhausted !! Exiting............!!!\n")
    exit()


           
while True:
    print("1.Create Account")
    print("2.Check Balance")
    print("3.Deposit Money")
    print("4.Withdraw Money")
    print("5.Change Pin")
    print("6.Delete Account")
    print("7.Transfer Money")
    print("8.Transaction History")
    print("9.Fixed Deposit")
    print("10.Statement")
    print("11.Exit\n")

    try:
        choice = int(input("Enter your choice (1-11) : "))
    except ValueError:
        print("Enter only Valid Choice (1-11)!")
        continue

    match choice:

        case 1:
            name ,pin,acc_num = create_account()
            save_accounts()
            transactions(acc_num,"Account Created")
            
        case 2:
            acc_num , pin = login()
            print(f"Your Account Balance = ₹{atm[acc_num][1]:.2f}\n")
            

                    

        case 3:
            acc_num , pin = login()
            try:
                amount = float(input("Enter Deposit Amount : ₹ "))
            except ValueError:
                print("Amount must be only Numbers!\n")
                continue
            if amount <= 0:
                print("Amount must be greater than 0!\n")
             
            elif acc_num not in atm:
                print("Account Not Found!\n")
            
            else:
                atm[acc_num][1]+=amount
                save_accounts()
                transactions(acc_num,f"Deposit : {amount}")
                print("Deposit Successfull!\n")
        
        case 4:
            while True:
                try:
                    acc_num = int(input("Enter Account Number : "))
                    break
                except ValueError:
                    print("Account Number must be only in Numbers!\n")
            while True:
                        try:
                            amount = float(input("Enter Amount to Withdraw : ₹ "))
                            if amount<=0:
                                print("Amount must be greater than 0!")
                            
                            else:
                                break
                        except ValueError:
                            print("Please Enter a Valid Number!")  
            
            pin = int(getpass("Enter Pin : "))


            if acc_num not in atm:
                print("Account Not Found!\n")
            elif atm[acc_num][2] != pin:
                print("Incorrect Pin!\n")
            elif amount > atm[acc_num][1]:
                print("Insufficient Balance!\n") 
            elif amount > atm[acc_num][1]- 5000 :
                print("Insufficient Balance! Minimun Balance of 5000 should be maintained!")
            else:
                last_withdraw_date = atm[acc_num][3]
                today_withdraw_amount = atm[acc_num][4]
                today = datetime.now().strftime("%d-%m-%Y")

                if last_withdraw_date != today:
                    atm[acc_num][3] = today
                    atm[acc_num][4] = 0

                today_withdraw_amount = atm[acc_num][4]
                if today_withdraw_amount + amount > 200000:
                    print("Daily Withdrwal Limit ₹200000 exceeded!\n")

                else:
                    atm[acc_num][1] -= amount
                    atm[acc_num][4] +=amount
                    

                    save_accounts()
                    transactions(acc_num , f"Withdraw : {amount}")
                    print("Withdraw Successfull!\n")

        case 5:
            acc_num , pin = login()
            while True:
                try:
                    new_pin = int(getpass("Enter New Pin : "))
                    if len(str(new_pin)) != 4:
                        print("Pin must be 4 digits only!")
                    else:
                        break
                except ValueError:
                    print("Pin must be only in Numbers\n")

            atm[acc_num][2] = new_pin
            save_accounts()
            transactions(acc_num,"PIN Changed")
            print("Pin changed Successfully!\n")
                        
        
        case 6:
            acc_num , pin = login()

            for fd_num in list(fd):
                if fd[fd_num][0] == acc_num:
                    del fd[fd_num]
            fd_save()          
            transactions(acc_num,"Account Deleted")   
            del atm[acc_num]
            save_accounts()
            print("Account Deleted Successfully!\n")

        case 7:
            sender_acc_num,sender_pin = login()
            receiver_acc_num = int(input("Enter Receiver Account Number : "))

            if receiver_acc_num not in atm:
                print("Receiver Account Not Found!\n")    
            elif sender_acc_num == receiver_acc_num:
                print("No Transaction between Same Account\n")       
            else:
                while True:
                        try:
                            amount = float(input("Enter Amount to Tranfer : ₹ "))
                            if amount<=0:
                                print("Amount must be greater than 0!")
                            else:
                                break
                        except ValueError:
                            print("Please Enter a Valid Number!")    
 
                if amount > atm[sender_acc_num][1]:
                    print("Insufficent Balance\n")  
                elif atm[sender_acc_num][1]- amount <5000:
                    print("Minimum Balance of ₹5000 should be maintained!")    
                else:
                    atm[receiver_acc_num][1]+=amount
                    atm[sender_acc_num][1]-=amount
                    save_accounts()
                    transactions(sender_acc_num,f"Transferred {amount} to {receiver_acc_num}")
                    transactions(receiver_acc_num,f"Received {amount} from {sender_acc_num}")
                    print("Transaction Success!\n")
 
        
        
        case 8:
            acc_num , pin = login()
            try:
                found = False
                with open("transaction.txt","r") as file:
                    for line in file:
                        account, current_time ,message = line.strip().split(",",2)

                        if int(account) == acc_num:
                            print(current_time, "-" , message)
                            found = True
                    if not found:
                            print("No Transaction History\n")            
            except FileNotFoundError:
                print("Transaction History Not Found\n")
                    
        case 9:
            while True:
                print("-----Fixed Deposit-----\n")
                print("1.Create FD")
                print("2.View FD details")
                print("3.Close FD")
                print("4.Back")

                while True:
                    try:
                        fd_choice = int(input("Enter your Choice : "))
                        if fd_choice in [1,2,3,4]:
                            break
                        else:
                            print("Option should be only (1-4)\n")
                    except ValueError:
                        print("Enter only Numbers!\n")
                        
                match fd_choice:
                    case 1:
                        fd_account()

                    case 2:
                        acc_num,pin = login()

                        found = False

                        for fd_num , details in fd.items():
                            if details[0] == acc_num:
                                found = True

                                print("-----FD Details-----\n")
                                print(f"FD Number : {fd_num}")
                                print(f"FD Amount : ₹{details[1]}")
                                print(f"Duration : {details[2]} days")
                                print(f"Interest Amount : {details[3]:.2f}")
                                print(f"Maturity Amount : ₹{details[4]:.2f}")
                                print()

                        if not found:
                            print("No FD Found!")

                    case 3:
                        acc_num,pin = login()
                        while True:
                            try:
                                fd_num = int(input("Enter FD Number : "))
                                if fd_num not in fd:
                                    print("FD Account Not Found!\n")
                                else:
                                    break
                            except ValueError:
                                print("FD number should be only Numbers!\n")
        
                        details = fd[fd_num]
                        fd_amount = details[1]
                        created_date = details[5]

                        if details[0] != acc_num:
                            print("This FD does not belong to your Account!")
                            break
                  
                        days_completed = (datetime.now() - created_date).days 

                        if days_completed <= 0:
                            print("FD cannot be closed on the same day it was created!")
                            break

                        elif days_completed <= 90:
                            rate = 4
                            interest = (fd_amount * rate * days_completed) / (100 * 365)

                        elif days_completed <= 364:
                            rate = 6
                            interest = (fd_amount * rate * days_completed) / (100 * 365)

                        else:
                            rate = 7
                            interest = (fd_amount * rate * days_completed) / (100 * 365)

                        closing_amount = fd_amount + interest

                        atm[acc_num][1] += closing_amount

                        del fd[fd_num]
                        save_accounts()
                        fd_save()
                        transactions(acc_num , f"FD Closed : {closing_amount}")
                        print("FD Closed Successfully!\n")
                        print(f"₹{closing_amount:.2f} is added to your account\n")
                        
                    case 4:
                        print("------------------\n")
                        break
                        

                    case _:
                        print("Invalid Choice\n")
                        print("------------------\n")

        
        case 10:
            print("-----Statement-----\n")
            start_date = input("Enter Start date (dd-mm-yyyy) : ")
            end_date = input("Enter End date (dd-mm-yyyy) : ")
            try:
                start_date = datetime.strptime(start_date,"%d-%m-%Y")
                end_date = datetime.strptime(end_date,"%d-%m-%Y")
                if start_date > end_date:
                    print("Start date cannot be greater the End date!")
                    continue
            except ValueError:
                print("It must be in the format of (dd-mm-yyyy)!\n")
                continue
            acc_num,pin = login()

            with open("transaction.txt","r") as file:
                found = False
                for line in file:
                    account,current_time,message = line.strip().split(",",2)
                    current_date = datetime.strptime(current_time.split()[0],"%d-%m-%Y")

                    if int(account) == acc_num and start_date <= current_date <= end_date:
                        found = True
                        print(current_time , "-" , message)
                if not found:
                    print("No Transactions found for selected Period \n")


        case 11:
            print("----Thank You----\n")
            print("-------------------\n")
            break

        case _:
            print("INVALID CHOICE!")