from datetime import datetime
from datetime import date
import os


class check:  # check
    is_payed = False

    def __init__(self, price, deadLine, starting_date):
        self.price = price
        self._deadLine = deadLine
        self.starting_date = starting_date

    def __str__(self):
        return f"Price: {self.price}\nDeadline: {self._deadLine}\nStarting date: {self.starting_date}\nPayment status: {self.is_payed}\nRemaining days: {self.getRemainingDay()}"

    def print(self):
        # print(
        #     f"Price: {self.price}\nDeadline: {self._deadLine}\nStarting date: {self.starting_date}\nPayment status: {self.is_payed}")
        # print(
        #     f"Remaining days: {(self._deadLine - self.starting_date).days}\n")
        print(str(self))

    def getRemainingDay(self):
        if not self.is_payed:
            return (self._deadLine - self.starting_date).days

        return 0

    def getPayStatus(self):
        return self.is_payed

    def pay(self):
        self.is_payed = True


class installment:  # aqsat
    lastPayment = 0  # akharin pardakhti ke bayad anjam shavad
    is_payed = False  # tamami pardakht ha tamam shode

    def __init__(self, price, number, interval, startingDate):
        self.price = price  # qeymate har pardakht
        self._number = number  # tedade kolle pardakht ha
        self._interval = interval  # moddat zamane har pardakht
        self.startingDate = startingDate  # tarikhe shuru

    def __str__(self):
        return str(f"Price: {self.price}\nPayment number(s): {self._number}\nStarting date: {self.startingDate}\nPayment interval: {self._interval.day} day(s)\nAll payments finished: {self.is_payed}\nPaid payments: {self.lastPayment}\nRemaining days untill next payment: {self.getRemainingDaysToLastPayment()}")

    def print(self):
        # print(f"Price: {self.price}\nPayment number(s): {self._number}\nStarting date: {self.startingDate}\nPayment interval: {self._interval.day} day(s)\nPayment status: {self.is_payed}")
        # print(f"{self.lastPayment} paid  or out of time installment(s).")
        # print(f"Remaining days untill next payment: {self.getRemainingDaysToLastPayment()}\n")
        print(str(self))

    def isFinished(self):
        return self.lastPayment - 1 == self._number

    def notPayed(self):  # returns installments that are out of time
        temp1 = (date.today() - self.startingDate).days / self._interval.day
        temp2 = int(temp1) - (self.lastPayment - 1)

        if temp2 >= 1:
            self.lastPayment += temp2

            return installment(
                self.price,
                int(temp2),
                self._interval,
                self.startingDate)

        return False

    def pay(self, num):
        if not self.is_payed and self.lastPayment - 1 + num <= self._number:
            self.lastPayment += num

            if self.lastPayment - 1 == self._number:
                self.is_payed = True

            return True

        else:
            return False

    def getRemainingDaysToLastPayment(self):
        return self._interval.day * (self.lastPayment + 1) - (date.today() - self.startingDate).days

    def getPayStatus(self):
        return self.is_payed


class customer:  # moshtari
    total_transaction = 0  # kolle tedade tarakonesh ha
    total_debt = 0  # kolle tedade bedehi ha

    def __init__(self, user_name, password, address, code):
        self._user_name = user_name
        self._password = password
        self.address = address
        self.code = code

        self._checks_list = []
        self._installment_list = []
        self._debt_list = set()

    def __str__(self):
        return str(
            f"Customer's information (Name: {self._user_name}, Address: {self.address}, National Code: {self.code})")

    def getInfo(self):  # returns a tuple of username and password
        return (self._user_name, self._password)

    def add_check(self, chk):
        self._checks_list.append(chk)
        self.total_transaction += 1

    def add_inst(self, inst):
        self._installment_list.append(inst)
        self.total_transaction += 1

    def show_checks(self):
        if len(self._checks_list) == 0:
            print("No checks yet.")
            return

        i = 1
        for item in self._checks_list:
            print("Check", i, ':')
            i += 1
            item.print()

    def show_installments(self):
        if len(self._installment_list) == 0:
            print("No installment yet.")
            return

        i = 1
        for item in self._installment_list:
            print("Installment", i, ':')
            i += 1
            item.print()

    def show_debts(self):
        if len(self._debt_list) == 0:
            print("No debt yet.")
            return

        i = 1
        for item in self._debt_list:
            print("Number", i, ':')
            item.print()

            i += 1

    def trust_status(self):
        if self.total_transaction == 0:
            print("No checks yet!")
            return

        else:
            temp = (self.total_debt / self.total_transaction) * 100
            if temp < 20:
                print("\tGood trust status.")

            elif temp > 70:
                print("\tBad trust status.")

            else:
                print("\tMid-level trust status.")

    def setUser(self, newUser):
        self._user_name = newUser

    def setPassword(self, newPass):
        self._password = newPass

    def setAddress(self, newAddress):
        self.address = newAddress

    # evaluates if there is any check that is 1 day ahead to it's deadline
    def oneDayToFinishCheck(self):
        i = 0

        for item in self._checks_list:
            if item.getRemainingDay() is not None:
                if item.getRemainingDay() <= 1:
                    i += 1

        return i

    # evaluates if there is any installment that is 1 day ahead to it's
    # deadline
    def oneDayToFinishInstallment(self):
        i = 0

        for item in self._installment_list:
            if item.getRemainingDaysToLastPayment() <= 1:
                i += 1

        return i

    def debts(self):  # returns number of debts
        i = 0

        for item in self._checks_list:
            if item.getRemainingDay() is not None:  # if it's not payed
                if item.getRemainingDay() <= 1 and not item.getPayStatus(
                ):  # if it's out of time and not payed
                    i += 1
                    self._debt_list.add(item)

        for item in self._installment_list:
            inst = item.notPayed()  # if it's out of time and not payed

            if inst:
                i += 1
                self._debt_list.add(inst)

        self.total_debt = i
        return i

    def payCheck(self, index):
        if index < len(
                self._checks_list) and not self._checks_list[index].getPayStatus():
            self._checks_list[index].pay()

            flag = False
            for item in self._debt_list:  # cleaning the check if it is in debt list
                if item == self._checks_list[index]:
                    flag = True
                    break

            if flag:
                self._debt_list.remove(item)

            return True
        return False

    def payInstallment(self, index, num):
        if index < len(
                self._installment_list) and not self._installment_list[index].getPayStatus():
            return self._installment_list[index].pay(num)

        return False

    def payDebt(self, choice):
        i = 0

        for item in self._debt_list:

            if i == choice:  # finding the item for payment

                if not item.getPayStatus():  # checking if we can pay it or not
                    item.pay()  # paying

                    if item.getPayStatus() or isinstance(
                            item, check):  # checking if it is finished or not
                        self._debt_list.remove(item)

                    return True

            i += 1


class employee:  # karmand
    def __init__(self, user_name, password):
        self._user_name = user_name
        self._password = password

    def __str__(self):
        return str(f"Employee's information (Name: {self._user_name})")

    def getInfo(self):  # returns a tuple of username and password
        return (self._user_name, self._password)


# global list of customer and list of employees
customers = []
employees = []


def writeToFile(string):
    file1 = open("payments.txt", "a")
    file1.write(string)

    file1.close()


def clear():  # waits for an input then clears the screen
    input("\nPress ENTER key to continue")
    os.system("cls")


def clear2():  # just clears the screen
    os.system("cls")


def payments_menu(cst):

    while(True):
        clear()

        print("What do you want to pay?")
        print("\t\t\t1.Pay a check\n")
        print("\t\t\t2.Pay an installment\n")
        print("\t\t\t3.Pay a debt\n")
        print("\t\t\t4.Pay multiple installments\n")
        print("\t\t\t5.Back to Customers menu\n")

        sel = input("\t\t\tYour selection: ")

        clear2()

        if sel == '1':
            if len(cst._checks_list) == 0:
                print("No checks yet.")
                continue

            print("Checks list: ")
            cst.show_checks()
            print(
                "Enter which check do you want to pay? (enter the number beside the check)")

            choice = int(input("Your selection: ")) - 1

            if cst.payCheck(choice):
                writeToFile(
                    f"----{str(cst)} payed for :\n{str(cst._checks_list[choice])}\nPayment date:{date.today()}\n\n")

                print("Payment successfull!")

            else:
                print("Wrong choice!")

        elif sel == '2':
            if len(cst._installment_list) == 0:
                print("No checks yet.")
                continue

            print("Installments list: ")
            cst.show_installments()
            print(
                "Enter which installment do you want to pay? (enter the number beside the installment)")

            choice = int(input("Your selection: ")) - 1

            if cst.payInstallment(choice, 1):
                writeToFile(
                    f"----{str(cst)} payed for :\n{str(cst._installment_list[choice])}\nPayment date:{date.today()}\n\n")

                print("Payment successfull!")

            else:
                print("Wrong choice!")

        elif sel == '3':
            if len(cst._debt_list) == 0:
                print("No checks yet.")
                continue

            print("Debt list: ")
            cst.show_debts()
            print(
                "Enter which debt do you want to pay? (enter the number beside the debt)")

            choice = int(input("Your selection: ")) - 1

            if cst.payDebt(
                    choice):  # as we didn't change the set therfore the indexes are the same
                i = 0
                tmp = ""

                for item in cst._debt_list:
                    if i == choice:
                        tmp = str(item)
                        break

                    i += 1

                writeToFile(
                    f"----{str(cst)} payed for :\n{tmp}\nPayment date:{date.today()}\n\n")

                print("Payment successfull!")

            else:
                print("Wrong choice!")

        elif sel == '4':
            if len(cst._installment_list) == 0:
                print("No checks yet.")
                continue

            print("Installments list: ")
            cst.show_installments()
            print(
                "Enter which installment do you want to pay? (enter the number beside the installment)")

            choice = int(input("Your selection: ")) - 1

            num = int(input("Enter how many installment you do want to pay: "))

            if cst.payInstallment(choice, num):
                writeToFile(
                    f"----{str(cst)} payed for :\n{str(cst._installment_list[choice])}\nPayment date:{date.today()}\n\n")

                print("Payment successfull!")

            else:
                print("Wrong choice!")

        elif sel == '5':
            return

        else:
            print("Wrong selection, please try again!")


def employee_menu(emp):
    while(True):
        clear()

        for item in customers:  # updating all customers debts
            item.debts()

        print("You are logged in as:")
        print(emp)

        print("\nOptions:")
        print("\t\t\t1.Create new account for customer\n")
        print("\t\t\t2.Edit customer's information\n")
        print("\t\t\t3.Delete customer's account\n")
        print("\t\t\t4.Create checks for a customer\n")  # check ha
        print("\t\t\t5.Create Installments for a customer\n")
        print("\t\t\t6.Show customer's trust status\n")  # aqsat
        # taiidieye pardakhte naqdi
        print("\t\t\t7.Confirm customer's payment(in cash)\n")
        print("\t\t\t8.Logout\n")

        # temperary variables for exchanging inputs
        cst_user = ""
        cst_pass = ""
        cst_add = ""
        cst_code = ""

        sel = input("\t\t\tYour selection: ")

        clear2()

        if sel == '1':
            print("Please enter customer's information!")
            cst_user = input("Username: ")
            cst_pass = input("Password: ")
            cst_add = input("Address: ")
            cst_code = input("National code: ")
            # to do : check the user pass if is duplicate

            cst = customer(cst_user, cst_pass, cst_add, cst_code)
            customers.append(cst)
            del cst

            print("New customer account successfully added.")

        elif sel == '2':
            print(
                "Please enter customer's username and password to edit their information!")
            cst_user = input("Username: ")
            cst_pass = input("Password: ")

            flag = False
            for item in customers:
                info_tuple = item.getInfo()

                if info_tuple[0] == cst_user and info_tuple[1] == cst_pass:
                    print("Customer account found.\n")

                    str1 = input("Please enter new password: ")
                    str2 = input("Please enter new address: ")
                    item.setPassword(str1)
                    item.setAddress(str2)

                    print("Info changed.")
                    flag = True
                    break

            if not flag:
                print("User not found! Wrong username or password.")

        elif sel == '3':
            print(
                "Please enter customer's username and password to delete their account!")
            cst_user = input("Username: ")
            cst_pass = input("Password: ")

            flag = False
            for item in customers:
                info_tuple = item.getInfo()

                if info_tuple[0] == cst_user and info_tuple[1] == cst_pass:
                    customers.remove(item)
                    print("Customer's account deleted from list.")

                    flag = True
                    break

            if not flag:
                print("User not found! Wrong username or password.")

        elif sel == '4':
            print("Please enter customer's username and password!")
            cst_user = input("Username: ")
            cst_pass = input("Password: ")

            flag = False
            for item in customers:
                info_tuple = item.getInfo()

                if info_tuple[0] == cst_user and info_tuple[1] == cst_pass:
                    print("Customer found.\n")

                    deadLine = input(
                        "Please enter deadline of check(in the from of date.month.year): ")
                    price = input("Please enter price of check: ")

                    chk = check(int(price), datetime.strptime(
                        deadLine, "%d.%m.%Y").date(), date.today())
                    item.add_check(chk)
                    print("Check succesfully added.")

                    flag = True
                    break

            if not flag:
                print("User not found! Wrong username or password.")

        elif sel == '5':
            print("Please enter customer's username and password!")
            cst_user = input("Username: ")
            cst_pass = input("Password: ")

            flag = False
            for item in customers:
                info_tuple = item.getInfo()

                if info_tuple[0] == cst_user and info_tuple[1] == cst_pass:
                    print("Customer found.\n")

                    # hatman be vahede ruz bashe
                    interval = input(
                        "Please enter time between each payment(beware that it should be in DAYS form): ")
                    price = input(
                        "Please enter price of each payment of installment: ")
                    number = input(
                        "Please enter number of payments for installment: ")

                    inst = installment(int(price), int(number), datetime.strptime(interval, "%d").date(), date.today())
                    item.add_inst(inst)
                    print("Installment succesfully added.")

                    flag = True
                    break

            if not flag:
                print("User not found! Wrong username or password.")

        elif sel == '6':
            print("Please enter customer's username and password!")
            cst_user = input("Username: ")
            cst_pass = input("Password: ")

            flag = False
            for item in customers:
                info_tuple = item.getInfo()

                if info_tuple[0] == cst_user and info_tuple[1] == cst_pass:
                    print("Trust Status:")
                    item.trust_status()

                    flag = True
                    break

            if not flag:
                print("User not found! Wrong username or password.")

        elif sel == '7':
            print("Please enter customer's username and password.")
            cst_user = input("Username: ")
            cst_pass = input("Password: ")

            flag = False
            for item in customers:
                info_tuple = item.getInfo()

                if info_tuple[0] == cst_user and info_tuple[1] == cst_pass:
                    payments_menu(item)

                    flag = True
                    break

            if not flag:
                print("User not found! Wrong username or password.")

        elif sel == '8':
            print("Logged out!")
            return

        else:
            print("Wrong selection, please try again!")


def customer_menu(cst):
    while(True):
        clear()

        print("You are logged in as:")
        print(cst)

        print("\nWARNINGS:")
        print(
            f"-You have {cst.oneDayToFinishCheck()} check(s) that have one or less than one day to pay.")
        print(
            f"-You have {cst.oneDayToFinishInstallment()} installment(s) that have one or less than one day to pay.")
        print(
            f"-You have {cst.debts()} debt(s).\n")

        print("Options:")
        print("\t\t\t1.Show Installment's status\n")
        print("\t\t\t2.Show Check's status\n")
        print("\t\t\t3.Show Debt's status\n")
        print("\t\t\t4.Show customer's trust status\n")
        print("\t\t\t5.Pay online\n")
        print("\t\t\t6.Pay in cash\n")
        print("\t\t\t7.Logout\n")

        sel = input("\t\t\tYour selection: ")

        clear2()

        if sel == '1':
            cst.show_installments()

        elif sel == '2':
            cst.show_checks()

        elif sel == '3':
            cst.show_debts()

        elif sel == '4':
            print("Trust Status:")
            cst.trust_status()

        elif sel == '5':
            payments_menu(cst)

        elif sel == '6':
            print("Please ask an employee to take your payments in cash.")

        elif sel == '7':
            print("Logged out!")
            return

        else:
            print("Wrong selection, please try again!")


def main():
    print("\t\t\t\t** Welcome! **")

    while(True):  # Main menu
        clear()

        print("What type of user are you?(Customer or Employee)\n")
        print("\t\t\t1.Customer\n")
        print("\t\t\t2.Employee\n")
        print("\t\t\t3.Exit\n")
        sel = input("\t\t\tYour selection: ")

        # resetting username and password for login
        cst_user = ""
        cst_pass = ""

        if sel == '1':  # Customer login
            print("\n")

            print("Please enter your username and password!")
            cst_user = input("Username: ")
            cst_pass = input("Password: ")

            flag = False  # flag is a boolean for saving the login status
            for item in customers:
                info_tuple = item.getInfo()

                if info_tuple[0] == cst_user and info_tuple[1] == cst_pass:
                    print("Login successfull!")
                    customer_menu(item)

                    flag = True
                    break

            if not flag:
                print("Login not successfull! Wrong username or password.")

        elif sel == '2':  # Employee login
            while(True):
                clear()

                # reseting username and password for login
                emp_user = ""
                emp_pass = ""

                print("What type of employee are you?\n")
                print("\t\t\t1.Log in(for already signed up employees)\n")
                print("\t\t\t2.Sign up(for new employees)\n")
                print("\t\t\t3.Back to Main menu\n")

                sel2 = input("Your selection: ")

                if sel2 == '1':
                    print("Please enter your username and password!")
                    emp_user = input("Username: ")
                    emp_pass = input("Password: ")

                    flag = False  # flag is a boolean for saving the login status
                    for item in employees:
                        info_tuple = item.getInfo()

                        if info_tuple[0] == emp_user and info_tuple[1] == emp_pass:
                            print("Login successful!")
                            employee_menu(item)

                            flag = True
                            break

                    if not flag:
                        print("Login not successful! Wrong username or password.")

                elif sel2 == '2':
                    print("Please enter your username and password!")
                    emp_user = input("Username: ")
                    emp_pass = input("Password: ")
                    # to do : check the user pass if duplicate

                    # adding new employee(emp) to list of employees
                    emp = employee(emp_user, emp_pass)
                    employees.append(emp)

                    print("Sign up successful!")

                    # it can be uncommented for going to employee menu right after signing up
                    # employee_menu(emp)

                elif sel2 == '3':
                    break

                else:
                    print("Wrong selection, please try again!")

        elif sel == '3':
            quit()

        else:
            print("Wrong selection, please try again!")


if __name__ == "__main__":
    main()