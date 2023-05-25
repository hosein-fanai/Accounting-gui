import accounting as acc

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import font

import tkcalendar as cal

import sqlite3 as db

from datetime import datetime
from datetime import date


class Frm(tk.Frame):
    def __init__(self, root, con=None, msg=None, app=None):
        tk.Frame.__init__(self, root)
        self.con = con
        self.msg = msg
        self.app = app

        self.user_name = tk.StringVar()
        self.password = tk.StringVar()

    def reset(self):
        self.user_name.set("")
        self.password.set("")

    def search_cst(self):
        if not self.user_name.get() or not self.password.get():
            self.msg.config(text="Invalid input!", fg="red")
            return

        if self.con:
            self.msg.config(text="Connected to database.", fg="green")
        else:
            self.msg.config(text="Not connected to database.", fg="red")
            return

        cmd = f"SELECT * FROM customers WHERE user_name = '{self.user_name.get()}' AND password = '{self.password.get()}' "
        curs = self.con.cursor()

        try:
            curs.execute(cmd)
            result = curs.fetchone()

            if result:
                self.found_cst(result)
            else:
                self.msg.config(text="Not found.", fg="red")
                return

        except db.OperationalError as err:
            self.msg.config(text="Database error: " + str(err), fg="red")
            self.con.rollback()
            return

    def found_cst(self, result):
        pass

    def update(self):
        pass


class emp_fr_1(Frm):

    def __init__(self, root, con, msg):
        super().__init__(root, con, msg)

        self.address = tk.StringVar()
        self.code = tk.StringVar()

        tk.Label(self, text="Username :").grid(row=0, column=0)
        tk.Label(self, text="Password :").grid(row=2, column=0)
        tk.Label(self, text="Address :").grid(row=4, column=0)
        tk.Label(self, text="National Code :").grid(row=6, column=0)

        tk.Entry(self, textvariable=self.user_name).grid(row=0, column=1)
        tk.Entry(self, textvariable=self.password, show="*").grid(row=2, column=1, pady=10)
        tk.Entry(self, textvariable=self.address).grid(row=4, column=1)
        tk.Entry(self, textvariable=self.code).grid(row=6, column=1, padx=20, pady=10)

        ttk.Button(self, text="Signup", command=self.signup, width=15).grid(row=8, column=0, columnspan=2, pady=10)

    def reset(self):
        self.user_name.set("")
        self.password.set("")
        self.address.set("")
        self.code.set("")

    def signup(self):
        if not self.user_name.get() or not self.password.get():
            self.msg.config(text="Invalid input!", fg="red")
            return

        if self.con:
            self.msg.config(text="Connected to database.", fg="green")
        else:
            self.msg.config(text="Not connected to database.", fg="red")
            return

        cmd = f"INSERT INTO customers VALUES('{self.code.get()}' ,'{self.user_name.get()}' ,'{self.password.get()}' ,'{self.address.get()}' ,0 ,0)"
        curs = self.con.cursor()

        try:
            curs.execute(cmd)
            self.con.commit()

        except db.OperationalError as err:
            self.msg.config(text="Database error: " + str(err), fg="red")
            self.con.rollback()
            return

        except db.IntegrityError as err:
            self.msg.config(text="Username already exists.", fg="red")
            self.con.rollback()
            return

        messagebox.showinfo("Accounting", "Signup succesful!")


class emp_fr_2(Frm):

    def __init__(self, root, con, msg):
        super().__init__(root, con, msg)

        self.address = tk.StringVar()
        self.code = tk.StringVar()
        self.new_password = tk.StringVar()

        tk.Label(self, text="First search for the customer account then edit it.", fg="blue").grid(row=0, column=0, columnspan=4, pady=10)
        tk.Label(self, text="Username :").grid(row=1, column=0)
        tk.Label(self, text="Password :").grid(row=2, column=0, rowspan=2, pady=10)
        tk.Label(self, text="Address :").grid(row=4, column=0, pady=5)
        tk.Label(self, text="National Code :").grid(row=5, column=0)
        tk.Label(self, text="New Password :").grid(row=6, column=0, pady=5)

        tk.Entry(self, textvariable=self.user_name).grid(row=1, column=1)
        tk.Entry(self, textvariable=self.password, show="*").grid(row=2, column=1)
        tk.Entry(self, textvariable=self.address).grid(row=4, column=1)
        tk.Entry(self, textvariable=self.code, state="disable").grid(row=5, column=1, padx=20)
        tk.Entry(self, textvariable=self.new_password, show="*").grid(row=6, column=1)

        ttk.Button(self, text="Search", command=self.search_cst, width=15).grid(row=1, column=2, columnspan=2, rowspan=2)
        ttk.Button(self, text="Edit", command=self.edit, width=15).grid(row=5, column=2, columnspan=2)

    def reset(self):
        self.user_name.set("")
        self.password.set("")
        self.address.set("")
        self.code.set("")
        self.new_password.set("")

    def found_cst(self, result):
        self.code.set(result[0])
        self.new_password.set(result[2])
        self.address.set(result[3])
        self.msg.config(text="Found customer account.", fg="blue")

    def edit(self):
        if self.con:
            self.msg.config(text="Connected to database.", fg="green")
        else:
            self.msg.config(text="Not connected to database.", fg="red")
            return

        cmd = f"UPDATE customers SET address = '{self.address.get()}' ,password = '{self.new_password.get()}' WHERE user_name = '{self.user_name.get()}' AND password = '{self.password.get()}' "
        curs = self.con.cursor()

        try:
            curs.execute(cmd)
            self.con.commit()

        except db.OperationalError as err:
            self.msg.config(text="Database error: " + str(err), fg="red")
            self.con.rollback()
            return

        messagebox.showinfo("Accounting", "Customer's account information updated.")


class emp_fr_3(Frm):

    def __init__(self, root, con, msg):
        super().__init__(root, con, msg)

        tk.Label(self, text="Enter customer's info to delete their account.", fg="blue").grid(row=0, column=0, columnspan=3)
        tk.Label(self, text="Username :").grid(row=2 ,column=0, rowspan=2, pady=20)
        tk.Label(self, text="Password :").grid(row=4, column=0)

        tk.Entry(self, textvariable=self.user_name).grid(row=2, column=1, pady=20)
        tk.Entry(self, textvariable=self.password, show="*").grid(row=4, column=1)

        ttk.Button(self, text="Delete", command=self.search_cst, width=15).grid(row=8, column=0, columnspan=2, pady=20)

    def found_cst(self, result):
        cmd = f"DELETE FROM customers WHERE user_name = '{self.user_name.get()}' AND password = '{self.password.get()}' "
        curs = self.con.cursor()

        try:
            curs.execute(cmd)
            self.con.commit()

        except db.OperationalError as err:
            self.msg.config(text="Database error: " + str(err), fg="red")
            self.con.rollback()

            return

        except db.IntegrityError as err:
            self.msg.config(text="Username already exists.", fg="red")
            self.con.rollback()

            return

        messagebox.showinfo("Accounting", "Customer's account deleted.")


class emp_fr_4(Frm):

    def __init__(self, root, con, msg):
        super().__init__(root, con, msg)

        # self.deadline = tk.StringVar()
        self.price = tk.StringVar()

        self.code = ""

        self.lb = tk.Label(self, text="First search for the customer account.", fg="blue")
        self.lb.grid(row=0, column=0, columnspan=4, pady=10)

        tk.Label(self ,text="Username :").grid(row=1 ,column=0)
        tk.Label(self ,text="Password :").grid(row=2 ,column=0 ,rowspan=2 ,pady=10)
        tk.Label(self ,text="Check's Deadline :").grid(row=4 ,column=0 ,pady=5)
        tk.Label(self ,text="Check's Price :").grid(row=5 ,column=0)

        self.user_ent = tk.Entry(self ,textvariable=self.user_name)
        self.pass_ent = tk.Entry(self ,textvariable=self.password, show="*")
        # tk.Entry(self ,textvariable=self.deadline).grid(row=4, column=1)
        tk.Entry(self ,textvariable=self.price).grid(row=5 ,column=1 ,padx=20)
        self.user_ent.grid(row=1 ,column=1)
        self.pass_ent.grid(row=2 ,column=1)

        self.de = cal.DateEntry(self ,dateformat=4)
        self.de.grid(row=4, column=1)

        ttk.Button(self, text="Search", command=self.search_cst, width=15).grid(row=1, column=2, columnspan=2, rowspan=2)
        ttk.Button(self, text="Buy", command=self.buy, width=15).grid(row=4, column=2, columnspan=2, rowspan=2)

    def found_cst(self, result):
        self.result = result

        self.user_ent["state"] = "disable"
        self.pass_ent["state"] = "disable"
        self.msg.config(text="Found customer's account.", fg="blue")

    def buy(self):
        if not self.de.get_date() or not self.price.get():
            self.msg["text"] = "Wrong input."
            self.msg["fg"] = "red"
            return

        if not self.result:
            self.msg["text"] = "Search first."
            self.msg["fg"] = "red"
            return

        if self.de.get_date() < datetime.today().date():
            self.msg["text"] = "Wrong Deadline. Must be after today."
            self.msg["fg"] = "red"
            return

        if self.con:
            self.msg.config(text="Connected to database.", fg="green")
        else:
            self.msg.config(text="Not connected to database.", fg="red")
            return

        cmd = f"INSERT INTO checks VALUES('{self.result[0]}' ,'{self.price.get()}' ,'{self.de.get_date()}' ,'{date.today()}' , 0)"
        cmd2 = f"UPDATE customers SET totalTransaction = {self.result[4] + 1} WHERE user_name = '{self.user_name.get()}' AND password = '{self.password.get()}' "

        curs = self.con.cursor()

        try:
            curs.execute(cmd)
            curs.execute(cmd2)
            self.con.commit()

        except db.OperationalError as err:
            self.msg.config(text="Database error: " + str(err), fg="red")
            self.con.rollback()
            return

        messagebox.showinfo("Accounting", "Check assigned succesfully.")


class emp_fr_5(Frm):
    def __init__(self, root, con, msg):
        super().__init__(root, con, msg)

        self.interval = tk.StringVar()
        self.price = tk.StringVar()
        self.number = tk.StringVar()

        self.code = ""

        self.lb = tk.Label(self, text="First search for the customer account.", fg="blue")
        self.lb.grid(row=0, column=0, columnspan=4, pady=10)

        tk.Label(self, text="Username :").grid(row=1, column=0)
        tk.Label(self, text="Password :").grid(row=2, column=0, rowspan=2, pady=10)
        tk.Label(self, text="Installment's Interval(days) :").grid(row=4, column=0, pady=5)
        tk.Label(self, text="Installment's Price :").grid(row=5, column=0)
        tk.Label(self, text="Installment's Number(s) :").grid(row=6, column=0, pady=5)

        self.user_ent = tk.Entry(self, textvariable=self.user_name)
        self.pass_ent = tk.Entry(self, textvariable=self.password, show="*")
        tk.Entry(self, textvariable=self.interval).grid(row=4, column=1)
        tk.Entry(self, textvariable=self.price).grid(row=5, column=1, padx=20)
        tk.Entry(self, textvariable=self.number).grid(row=6, column=1)
        self.user_ent.grid(row=1, column=1)
        self.pass_ent .grid(row=2, column=1)

        ttk.Button(self, text="Search", command=self.search_cst, width=15).grid(row=1, column=2, columnspan=2, rowspan=2)
        ttk.Button(self, text="Buy", command=self.buy, width=15).grid(row=5, column=2, columnspan=2)

    def found_cst(self, result):
        self.result = result

        self.user_ent["state"] = "disable"
        self.pass_ent["state"] = "disable"
        self.msg.config(text="Found customer's account.", fg="blue")

    def buy(self):
        if not self.result:
            self.msg["text"] = "Search first."
            self.msg["fg"] = "red"
            return

        try:
            int(self.interval.get())
            int(self.price.get())
            int(self.number.get())
            if not self.interval.get() or not self.price.get() or not self.number.get():
                raise Exception("oops")
        except:
            self.msg["text"] = "Wrong input."
            self.msg["fg"] = "red"
            return

        if self.con:
            self.msg.config(text="Connected to database.", fg="green")
        else:
            self.msg.config(text="Not connected to database.", fg="red")
            return

        cmd = f"INSERT INTO installments VALUES('{self.code}' ,'{self.price.get()}' ,'{self.number.get()}' ,{self.interval.get()} ,'{date.today()}' ,0 ,0)"
        cmd2 = f"UPDATE customers SET totalTransaction = {self.result[4] + 1} WHERE user_name = '{self.user_name.get()}' AND password = '{self.password.get()}' "
        curs = self.con.cursor()

        try:
            curs.execute(cmd)
            curs.execute(cmd2)
            self.con.commit()

        except db.OperationalError as err:
            self.msg.config(text="Database error: " + str(err), fg="red")
            self.con.rollback()
            return

        messagebox.showinfo("Accounting", "Installment assigned succesfully.")


class emp_fr_6(Frm):

    def __init__(self, root, con, msg):
        super().__init__(root, con, msg)

        tk.Label(self, text="Username :").grid(row=1, column=0)
        tk.Label(self, text="Password :").grid(row=2, column=0, pady=10)
        self.trust_status = tk.Label(self, text="Trust status", fg="blue")
        self.trust_status.grid(row=4, column=0, columnspan=2, rowspan=2)

        tk.Entry(self, textvariable=self.user_name).grid(row=1, column=1)
        tk.Entry(self, textvariable=self.password, show="*").grid(row=2, column=1)

        ttk.Button(self, text="Search", command=self.search_cst, width=15).grid(row=1, column=2, columnspan=2, rowspan=2, padx=10)

    def found_cst(self, result):
        if not result[4]:
            self.trust_status["text"] = "No checks or installments yet!"
            self.trust_status["fg"] = "blue"
            return

        temp = (result[5] / result[4]) * 100
        if temp < 20:
            self.trust_status["text"] = "\tGood trust status."
            self.trust_status["fg"] = "green"

        elif temp > 70:
            self.trust_status["text"] = "\tBad trust status."
            self.trust_status["fg"] = "red"

        else:
            self.trust_status["text"] = "\tMid-level trust status."
            self.trust_status["fg"] = "gold"


class emp_fr_7(Frm):

    def __init__(self, root, con, msg, app):
        super().__init__(root, con, msg, app)

        tk.Label(self, text="Enter customer's info to search for their account.", fg="blue").grid(row=0, column=0, columnspan=3)
        tk.Label(self, text="Username :").grid(row=2, column=0, rowspan=2, pady=20)
        tk.Label(self, text="Password :").grid(row=4, column=0)

        tk.Entry(self, textvariable=self.user_name).grid(row=2, column=1, pady=20)
        tk.Entry(self, textvariable=self.password, show="*").grid(row=4, column=1)

        ttk.Button(self, text="Search", command=self.search_cst, width=15).grid(row=8, column=0, columnspan=2, pady=20)

    def found_cst(self, result):
        class temp():
            def __init__(self ,app ,result):
                self.win = app.win
                if isinstance(app.user ,acc.employee):
                    self.user = acc.customer(result[1], result[2], result[3], result[0])

                elif isinstance(app.user ,acc.customer):
                    self.user = app.user

        self.app = temp(self.app ,result)

        self.top = tk.Toplevel(self.app.win)
        self.top.title("Payment")
        # self.top.iconbitmap(".\\.ico")
        self.top.geometry("+600+250")
        self.top.resizable("false", "false")

        #for modal view popup
        self.app.win.wm_attributes("-disabled", True)
        self.top.transient(self.app.win)
        self.top.protocol("WM_DELETE_WINDOW", self.closed_top)

        self.top_widgets()

    def top_widgets(self):
        installment_frame = tk.LabelFrame(self.top ,text="Installments" ,labelanchor=tk.N ,fg="orange" ,pady =5 ,padx=5 ,relief=tk.RAISED)
        check_frame = tk.LabelFrame(self.top ,text="Checks" ,labelanchor=tk.N ,fg="orange" ,pady =5,padx=5 ,relief=tk.RAISED)
        debt_frame = tk.LabelFrame(self.top ,text="Debts" ,labelanchor=tk.N ,fg="orange" ,pady =5,padx=5 ,relief=tk.RAISED)

        installment_frame.grid(row=2 ,column=0 ,rowspan=15 ,padx=5)
        check_frame.grid(row=2 ,column=1 ,rowspan=15 ,padx=5)
        debt_frame.grid(row=2 ,column=2 ,rowspan=15 ,padx=5)

        self.msg_ = self.msg
        tk.Label(self.top ,text="Choose wich payment is needed." ,fg="purple").grid(row=0 ,column=0 ,columnspan=5 ,rowspan=2 ,pady=5 ,sticky=tk.W)
        msg1 = tk.Label(installment_frame)
        msg2 = tk.Label(check_frame)
        msg3 = tk.Label(debt_frame)
        self.msg = tk.Label(self.top ,text="Welcome." ,fg="blue")

        msg1.pack(side=tk.BOTTOM)
        msg2.pack(side=tk.BOTTOM)
        msg3.pack(side=tk.BOTTOM)
        self.msg.grid(row=19 ,column=0 ,sticky=tk.SW)

        self.show_installment = cst_fr_1(installment_frame, self.con, msg=msg1, app=self.app ,event=self.choose)
        self.show_check = cst_fr_2(check_frame, self.con, msg=msg2, app=self.app ,event=self.choose)
        self.show_debt = cst_fr_3(debt_frame, self.con, msg=msg3, app=self.app ,event=self.choose)

        self.show_installment.update()
        self.show_check.update()
        self.show_debt.update()
        self.show_installment.pack(side=tk.TOP)
        self.show_check.pack(side=tk.TOP)
        self.show_debt.pack(side=tk.TOP)

        self.sb = tk.Spinbox(self.top ,state="disable")
        validation = self.top.register(self.sb_validate)
        self.sb.config(validate ="key" ,validatecommand =(validation ,'% P'))
        self.sb.grid(row=10 ,column=3)

        ttk.Button(self.top ,text="Back" ,command=self.closed_top).grid(row=19 ,column=3 ,pady=10)
        self.pay_button = ttk.Button(self.top ,text="Pay" ,command=self.pay ,state="disable")
        self.pay_button.grid(row=11 ,column=3)
        
    def closed_top(self):
        self.app.win.wm_attributes("-disabled", False)
        self.top.destroy()
        self.app.win.deiconify()
        self.msg = self.msg_

    def pay(self):
        if not messagebox.askyesno("Warning" ,"Are you sure you want to pay?"):
            return

        if self.choice_type == "installment" :
            payment = self.show_installment.results[self.choice_tag]
            if payment[5] or payment[2] == payment[6]:
                messagebox.showinfo("Payment" ,"This installment is already payed.")
                return

            try:
                if int(self.sb.get()) + payment[6] > payment[2]:
                    raise Exception("whoops")
            except:
                messagebox.showinfo("Payment" ,"Number of installments you are paying is wrong. Plaese try again.")
                return

            cmd = f'''UPDATE {self.choice_type}s SET  lastPayment = {payment[6] + int(self.sb.get())} , isPayed = {int(payment[2] == payment[6] + int(self.sb.get()))} WHERE 
            cstCode = '{payment[0]}' AND price = {payment[1]} AND number = {payment[2]} AND interval = '{payment[3]}' AND startingDate = '{payment[4]}' AND isPayed = {payment[5]} 
            AND lastPayment = {payment[6]} '''

        elif self.choice_type == "check" :
            payment = self.show_check.results[self.choice_tag]
            if payment[4]:
                messagebox.showinfo("Payment" ,"This check is already payed.")
                return

            cmd = f'''UPDATE {self.choice_type}s SET isPayed = 1  WHERE cstCode = '{payment[0]}' AND price = {payment[1]} 
            AND deadLine = '{payment[2]}' AND startingDate = '{payment[3]}' AND isPayed = {payment[4]} '''

        elif self.choice_type == "debt" :
            payment = self.show_debt.results[self.choice_tag]
            if payment[7]:
                messagebox.showinfo("Payment" ,"This debt is already payed.")
                return
            
            if (payment[1] == "check") or (payment[1] == "installment" and payment[2] == payment[6] + int(self.sb.get())):
                isPayed = 1
            else :
                isPayed = 0

            if payment[1] == "check":
                lastPayment = 0
            elif payment[1] == "installment":
                try:
                    if int(self.sb.get()) + payment[6] > payment[2]:
                        raise Exception("whoops")
                except:
                    messagebox.showinfo("Payment" ,"Number of installments you are paying is wrong. Plaese try again.")
                    return
                lastPayment = payment[6] + int(self.sb.get())

            cmd = f'''UPDATE {self.choice_type}s SET lastPayment = {lastPayment} , isPayed = {isPayed} WHERE cstCode = '{payment[0]}' AND 
            type = '{payment[1]}' AND price = {payment[2]} AND startingDate = '{payment[3]}' AND deadLine = '{payment[4]}' AND number = {payment[5]} AND 
            interval = '{payment[6]}' AND isPayed = {payment[7]} AND lastPayment = {payment[8]} '''

        if self.con:
            self.msg.config(text="Connected to database.", fg="green")
        else:
            self.msg.config(text="Not connected to database.", fg="red")
            return

        curs = self.con.cursor()

        try:
            curs.execute(cmd)
            self.con.commit()

            messagebox.showinfo("Payment","Payment succesfully done.")

        except db.OperationalError as err:
            self.msg.config(text="Database error: " + str(err), fg="red")
            self.con.rollback()
            return

        self.show_installment.update()
        self.show_check.update()
        self.show_debt.update()

    def sb_validate(self ,user_input):
        if  user_input.isdigit(): 
            minval = int(self.top.nametowidget(self.sb).config("from")[4]) 
            maxval = int(self.top.nametowidget(self.sb).config("to")[4]) 
    
            if int(user_input) not in range(minval, maxval): 
                print ("Out of range") 
                return False
    
            print(user_input) 
            return True
    
        elif user_input == "": 
            print(user_input) 
            return True
    
        else: 
            print("Not numeric") 
            return False

    def choose(self ,type_ ,tag ,text_w):
        self.choice_type = type_
        self.choice_tag = tag

        self.pay_button["state"] = "enable"

        if type_ == "installment":
            payment = self.show_installment.results[self.choice_tag]
            remaining_payments = payment[2] - payment[6]
            
            if remaining_payments >= 1:
                self.sb.config(state="normal" ,from_=1 ,to=remaining_payments)
            else:
                self.pay_button["state"] = "disable"

        elif type_ == "check":
            self.sb.config(state="disable") 

        elif type_ == "debt":
            self.sb.config(state="disable") 

        for item in self.show_installment.txt.tag_names():
            self.show_installment.txt.tag_config(item ,background='white') 

        for item in self.show_check.txt.tag_names():
            self.show_check.txt.tag_config(item ,background='white')

        for item in self.show_debt.txt.tag_names():
            self.show_debt.txt.tag_config(item ,background='white')

        text_w.tag_config(str(tag) ,background="powder blue")
        

class emp_fr_8(Frm):

    def __init__(self, root, app):
        super().__init__(root, app=app)

        tk.Label(self, text="Are you sure you want to logout?", bg="red").grid(row=0, column=2, columnspan=2)

        ttk.Button(self, text="Yes", command=self.app.logout, width=10).grid(row=4, column=1, pady=50)
        ttk.Button(self, text="No", command=lambda: self.app.main_label_frame.place_forget(), width=10).grid(row=4, column=4)


class cst_fr_1(Frm):

    def __init__(self, root ,con ,msg ,app ,width=30 ,event=None):
        super().__init__(root ,con ,msg ,app)
        self.event = event

        self.txt = tk.Text(self ,state="disable" ,width=width)
        sc = tk.Scrollbar(self ,command=self.txt.yview)
        self.txt.config(yscrollcommand=sc.set)

        sc.pack(side=tk.RIGHT ,fill=tk.Y)
        self.txt.pack(side=tk.LEFT)
        
        self.cmd = ""
        # self.search_m()

    def search_m(self):
        if self.con:
            self.msg.config(text="Connected to database.", fg="green")
        else:
            self.msg.config(text="Not connected to database.", fg="red")
            return

        self.cmd = f"SELECT * FROM {self.get_type()}s WHERE cstCode = '{self.app.user.code}'"
        curs = self.con.cursor()

        try:
            curs.execute(self.cmd)
            results = curs.fetchall()

            if results:
                self.msg.config(text="Found." ,fg="green")
                self.results = results
                self.show()

            else:
                self.msg.config(text="Not found any.", fg="red")
                return

        except db.OperationalError as err:
            self.msg.config(text="Database error: " + str(err), fg="red")
            self.con.rollback()
            return

    def get_type(self):
        return "installment"

    def show(self):
        self.txt.config(state="normal")
        self.txt.delete("1.0" ,tk.END)

        i=0
        for item in self.results:
            obj = self.create_obj(item)

            # start = float(self.txt.index("end")) - 1
            self.txt.insert(tk.INSERT ,str(obj) ,str(i))
            # self.txt.tag_add(str(i) ,str(start) ,tk.INSERT)
            if self.event:
                self.txt.tag_bind(str(i) ,"<Button-1>" ,lambda event ,i=i: self.event(self.get_type() ,i ,self.txt))
            self.txt.tag_bind(str(i) ,"<Enter>" ,lambda event ,i=i: self.enter_tag(i))
            self.txt.tag_bind(str(i) ,"<Leave>" ,lambda event ,i=i: self.leave_tag(i))

            self.txt.insert(tk.INSERT ,"\n\n")

            i+=1

        self.txt.config(state="disable")

    def create_obj(self ,item):
        inst = acc.installment(item[1] ,item[2] ,datetime.strptime(item[3], "%d").date() ,datetime.strptime(item[4], "%Y-%m-%d").date())
        inst.is_payed = bool(item[5])
        inst.lastPayment = item[6]

        return inst

    def update(self):
        self.search_m()

    def enter_tag(self ,tag):
        self.txt.config(cursor="hand2")

        self.txt.tag_config(str(tag) ,foreground="blue")
        fnt = font.Font(self.txt ,self.txt.cget("font"))
        fnt.configure(underline=True)
        self.txt.tag_config(str(tag) ,font=fnt)
        
    def leave_tag(self ,tag):
        self.txt.config(cursor="arrow")

        self.txt.tag_config(str(tag) ,foreground="black")
        fnt = font.Font(self.txt, self.txt.cget("font"))
        fnt.configure(underline=False)
        self.txt.tag_config(str(tag) ,font=fnt)


class cst_fr_2(cst_fr_1):

    def __init__(self, root ,con ,msg ,app ,width=28 ,event=None):
        super().__init__(root ,con ,msg ,app ,width ,event)

    def get_type(self):
        return "check"

    def create_obj(self ,item):
        chck = acc.check(item[1] ,datetime.strptime(item[2], "%Y-%m-%d").date() ,datetime.strptime(item[3], "%Y-%m-%d").date())
        chck.is_payed = bool(item[4])

        return chck


class cst_fr_3(cst_fr_1):

    def __init__(self, root ,con ,msg ,app ,width=28 ,event=None):
        super().__init__(root ,con ,msg ,app ,width ,event)

    def get_type(self):
        return "debt"

    def create_obj(self ,item):
        if item[1] == "check":
            dbt = acc.check(item[2] ,datetime.strptime(item[4] ,"%Y-%m-%d").date() ,datetime.strptime(item[3] ,"%Y-%m-%d").date())
            dbt.is_payed = bool(item[7])

        elif item[1] == "installment":
            dbt = acc.installment(item[2] ,item[5] ,datetime.strptime(item[6], "%d").date() ,datetime.strptime(item[3] ,"%Y-%m-%d").date())
            dbt.is_payed = bool(item[7])
            dbt.lastPayment = item[8]

        return dbt


class cst_fr_4(emp_fr_6):

    def __init__(self, root, con, msg, app):
        Frm.__init__(self, root, con, msg, app)

        self.trust_status = tk.Label(self, text="Trust status", fg="blue")
        self.trust_status.pack(side=tk.LEFT)

    def update(self):
        self.user_name.set(self.app.user._user_name)
        self.password.set(self.app.user._password)

        self.search_cst()


class cst_fr_5(emp_fr_7):

    def __init__(self, root, con, msg, app):
        Frm.__init__(self, root, con, msg, app)

        ttk.Button(self, text="Pay", command=self.update).pack()

    def update(self):
        self.user_name.set(self.app.user._user_name)
        self.password.set(self.app.user._password)

        self.search_cst()


class cst_fr_6(Frm):

    def __init__(self, root):
        super().__init__(root)

        tk.Label(self, text="Please ask an employee to take your payments in cash.", fg="purple").pack()