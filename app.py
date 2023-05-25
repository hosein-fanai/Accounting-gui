import accounting as acc
import frames as fr

from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter import font

import sqlite3

from datetime import datetime
from datetime import date


class App(object):
    def __init__(self, win):
        self.win = win
        self.con = sqlite3.connect(".\\accounts.db")
        self.user = None
        self.option_frames = {}
        self.emp_options = (
            "1.Create new account for customer",
            "2.Edit customer's information",
            "3.Delete customer's account",
            "4.Create Checks for a customer",  # check ha
            "5.Create Installments for a customer", # aqsat
            "6.Show customer's trust status",  
            "7.Confirm customer's payment(in cash)", # taiidieye pardakhte naqdi
            "8.Logout"
        )  # todo put this tuple in accounting.py and use it for menu options
        self.cst_options = (
            "1.Show Installment's status",
            "2.Show Check's status",
            "3.Show Debt's status",
            "4.Show customer's trust status",
            "5.Pay online",
            "6.Pay in cash",
            "7.Logout"
        )

        # self.win.protocol("WM_DELETE_WINDOW" ,self.closed_win )
        self.accs_widgets()
        self.start_log()
        self.debt_checker()

    def __del__(self):
        self.con.close()

    def start_log(self):
        self.win.withdraw()

        self.top = Toplevel(self.win)
        self.top.title("Login")
        self.top.iconbitmap(".\\budget.ico")
        self.top.geometry("300x250+600+250")
        self.top.resizable("false", "false")
        self.top.protocol("WM_DELETE_WINDOW" ,self.win.destroy)

        self.logs_widgets(self.top)
        self.login_menu()

    def login_menu(self):
        # self.user_name.set("")
        # self.password.set("")

        self.signup_frame.pack_forget()
        self.login_frame.pack(fill='both', expand=True)

    def signup_menu(self, event):
        # self.user_name.set("")
        # self.password.set("")

        if self.cb.get() == "Employee":
            self.login_frame.pack_forget()
            self.top.title("Signup")
            self.signup_frame.pack(fill="both", expand=True)

        else:
            messagebox.showwarning(
                "Oops!", "Customers need to ask employees for creating accounts!")

    def logs_widgets(self, win):
        if not win:
            win = self.win

        self.login_frame = Frame(win)

        lf = LabelFrame(self.login_frame, text="Enter your information.")

        ttk.Button(lf, text="Login", command=self.login).grid(row=3, column=0, columnspan=2, pady=10)
        ttk.Button(self.login_frame, text="Cancel", command=win.quit).place(relx=0.73, rely=0.88)

        img = PhotoImage(file=".\\user.png")

        lb1 = Label(self.login_frame, image=img)
        Label(self.login_frame, text="What type of user are you?").place( relx=0.25, rely=0)
        Label(lf, text="Username :").grid(row=0, column=0, padx=5)
        Label(lf, text="Password :").grid(row=2, column=0, padx=5, pady=10)
        lb2 = Label(self.login_frame, text="Don't have an account?", fg="blue")

        self.msg = Label(self.login_frame)
        self.msg.place(relx=0, rely=0.92)
        if self.con:
            self.msg.config(text="Connected to database.", fg="green")
        else:
            self.msg.config(text="Not connected to database.", fg="red")

        lb1.place(relx=0.02, rely=0.02)
        lb1.image = img
        lb2.place(relx=0.12, rely=0.76)
        lb2.bind("<Button-1>", self.signup_menu)
        lb2.bind("<Enter>", self.enter_label)
        lb2.bind("<Leave>", self.leave_label)

        self.user_name = StringVar()
        self.password = StringVar()
        ent1 = Entry(lf, textvariable=self.user_name)
        ent2 = Entry(lf, textvariable=self.password, show='*')

        ent1.bind("<Return>", lambda e: ent2.focus_set())
        ent1.grid(row=0, column=1, padx=10)
        ent2.bind("<Return>", lambda e: self.login())
        ent2.grid(row=2, column=1, padx=10)

        lf.place(relx=0.12, rely=0.25)

        self.cb = ttk.Combobox(self.login_frame, values=("Customer", "Employee"), state="readonly")
        # self.cb.current(0)
        self.cb.focus_set()
        self.cb.bind("<Return>", lambda e: ent1.focus_set())
        self.cb.place(relx=0.25, rely=0.1)

        self.signup_frame = Frame(win)

        lf2 = LabelFrame(self.signup_frame, text="Enter your information.")

        ttk.Button(lf2,text="Signup", command=self.signup).grid(row=6, column=0, columnspan=2, pady=10)
        ttk.Button(self.signup_frame,text="Back",command=self.login_menu).place(relx=0.73, rely=0.88)

        Label(self.signup_frame, text="Only use signup when you are an employee.", fg="blue").place(relx=0, rely=0)
        Label(lf2, text="Username :").grid(row=0, column=0, padx=5, pady=10)
        Label(lf2, text="Password :").grid(row=2, column=0, padx=5)
        Label(lf2, text="Password check :").grid(row=4, column=0, padx=5, pady=10)

        self.pass_check = StringVar()
        ent3 = Entry(lf2, textvariable=self.user_name)
        ent4 = Entry(lf2, textvariable=self.password, show='*')
        ent5 = Entry(lf2, textvariable=self.pass_check, show='*')

        ent3.focus_set()
        ent3.bind("<Return>", lambda e: ent4.focus_set())
        ent3.grid(row=0, column=1, padx=10)

        ent4.bind("<Return>", lambda e: ent5.focus_set())
        ent4.grid(row=2, column=1, padx=10)

        ent5.bind("<Return>", lambda e: self.signup())
        ent5.grid(row=4, column=1, padx=10)

        self.msg2 = Label(self.signup_frame)
        self.msg2.place(relx=0, rely=0.92)
        if self.con:
            self.msg2.config(text="Connected to database.", fg="green")
        else:
            self.msg2.config(text="Not connected to database.", fg="red")

        img2 = PhotoImage(file=".\\employee.png")
        lb3 = Label(self.signup_frame, image=img2)
        lb3.image = img2
        lb3.place(relx=0.83, rely=0.01)

        lf2.place(relx=0.08, rely=0.17)

    def accs_widgets(self):
        menubar = Menu(self.win)
        self.win.config(menu=menubar)
        file_menu = Menu(menubar, tearoff="false")
        help_menu = Menu(menubar, tearoff="false")
        help_menu.add_command(label="About",command=lambda: messagebox.showinfo("About","Hello from EchineF !"))
        menubar.add_cascade(label="File", menu=file_menu)
        menubar.add_cascade(label="Help", menu=help_menu)

        self.welcome = Label(self.win, fg="blue")
        self.welcome.place(relx=0, rely=0)

        self.options_box = ttk.Combobox(self.win, state="readonly", width=40)
        self.options_box.place(relx=0.5, rely=0.13, anchor=CENTER)
        self.options_box.bind("<<ComboboxSelected>>", self.option_chooser)

        self.main_label_frame = LabelFrame(self.win)

        self.msg3 = Label(self.win)
        self.msg3.place(relx=0, rely=0.94)
        if self.con:
            self.msg3["text"] = "Connected to database."
            self.msg3["fg"] = "green"
        else:
            self.msg3["text"] = "Not connected to database."
            self.msg3["fg"] = "red"

    def emp_menu(self, emp):
        self.ready_main_win(emp)

        self.options_box["values"] = self.emp_options

    def cst_menu(self, cst):
        self.ready_main_win(cst)

        self.options_box["values"] = self.cst_options

    def login(self):
        if self.con:
            self.msg.config(text="Connected to database.", fg="green")
        else:
            self.msg.config(text="NOt connected to database.", fg="red")
            return

        cmd = f"SELECT * from {self.cb.get().lower() + 's'} WHERE user_name = '{self.user_name.get() }' AND password = '{self.password.get() }' "
        curs = self.con.cursor()
        try:
            curs.execute(cmd)
            result = curs.fetchone()

            if not result:
                self.msg.config(text="Wrong input!", fg="red")
                return

        except sqlite3.OperationalError as err:
            self.msg.config(text="Database error: " + str(err), fg="red")
            self.con.rollback()
            return

        if self.cb.get() == "Employee":
            emp = acc.employee(result[0], result[1])
            messagebox.showinfo("Accounting","Login succesful!")

            self.emp_menu(emp)

        elif self.cb.get() == "Customer":
            cst = acc.customer(result[1], result[2], result[3], result[0])
            messagebox.showinfo("Accounting", "Login succesful!")

            self.cst_menu(cst)

        else:
            self.msg.config(text="Oops try again!", fg="red")

    def signup(self):
        if self.password.get() != self.pass_check.get():
            self.msg2.config(text="Passwords do not match.", fg="red")
            return

        if not self.user_name.get() or not self.password.get():
            self.msg2.config(text="Invalid input!", fg="red")
            return

        if self.con:
            self.msg2.config(text="Connected to database.", fg="green")
        else:
            self.msg2.config(text="NOt connected to database.", fg="red")
            return

        cmd = f"INSERT INTO employees VALUES('{self.user_name.get()}' ,'{self.password.get()}' )"
        curs = self.con.cursor()

        try:
            curs.execute(cmd)
            self.con.commit()

        except sqlite3.OperationalError as err:
            self.msg2.config(text="Database error: " + str(err), fg="red")
            self.con.rollback()
            return

        except sqlite3.IntegrityError as err:
            self.msg2.config(text="Username already exists.", fg="red")
            self.con.rollback()
            return

        emp = acc.employee(self.user_name.get(), self.password.get())
        messagebox.showinfo("Accounting", "Signup succesful!")

        self.emp_menu(emp)

    def logout(self):
        self.main_label_frame.place_forget()
        self.options_box.set("")
        self.start_log()

        for child in self.main_label_frame.winfo_children():
            child.destroy()

        self.option_frames.clear()

    def enter_label(self, event):
        lb = event.widget

        fnt = font.Font(lb, lb.cget("font"))
        fnt.configure(underline=True)

        lb.config(font=fnt, cursor="hand2")

    def leave_label(self, event):
        lb = event.widget

        fnt = font.Font(lb, lb.cget("font"))
        fnt.configure(underline=False)

        lb.config(font=fnt, cursor="arrow")

    def ready_main_win(self, user):
        self.top.destroy()
        self.top = None

        self.win.title("Accounting")
        self.win.iconbitmap(".\\budget.ico")
        self.win.geometry("500x350+480+200")
        self.win.resizable("false", "false")
        self.win.deiconify()

        self.user = user
        self.welcome["text"] = f"You are logged in as:\n{self.user}"

        self.add_frames()

        self.debt_checker()

    def add_frames(self):
        if isinstance(self.user ,acc.employee):
            self.option_frames[self.emp_options[0]] = fr.emp_fr_1(self.main_label_frame, self.con, self.msg3)
            self.option_frames[self.emp_options[1]] = fr.emp_fr_2(self.main_label_frame, self.con, self.msg3)
            self.option_frames[self.emp_options[2]] = fr.emp_fr_3(self.main_label_frame, self.con, self.msg3)
            self.option_frames[self.emp_options[3]] = fr.emp_fr_4(self.main_label_frame, self.con, self.msg3)
            self.option_frames[self.emp_options[4]] = fr.emp_fr_5(self.main_label_frame, self.con, self.msg3)
            self.option_frames[self.emp_options[5]] = fr.emp_fr_6(self.main_label_frame, self.con, self.msg3)
            self.option_frames[self.emp_options[6]] = fr.emp_fr_7(self.main_label_frame, self.con, self.msg3, self)
            self.option_frames[self.emp_options[7]] = fr.emp_fr_8(self.main_label_frame, self)

        if isinstance(self.user ,acc.customer):
            self.option_frames[self.cst_options[0]] = fr.cst_fr_1(self.main_label_frame, self.con ,self.msg3 ,self ,60)
            self.option_frames[self.cst_options[1]] = fr.cst_fr_2(self.main_label_frame, self.con ,self.msg3 ,self ,60)
            self.option_frames[self.cst_options[2]] = fr.cst_fr_3(self.main_label_frame, self.con ,self.msg3 ,self ,60)
            self.option_frames[self.cst_options[3]] = fr.cst_fr_4(self.main_label_frame, self.con ,self.msg3 ,self)
            self.option_frames[self.cst_options[4]] = fr.cst_fr_5(self.main_label_frame, self.con ,self.msg3 ,self)
            self.option_frames[self.cst_options[5]] = fr.cst_fr_6(self.main_label_frame)
            self.option_frames[self.cst_options[6]] = fr.emp_fr_8(self.main_label_frame, self)

    def option_chooser(self, event):
        self.main_label_frame.place(relx=0.5, rely=0.55, anchor=CENTER, relwidth=1, relheight=0.7 ,width = -5)
        self.main_label_frame["text"] = self.options_box.get()[2:]

        if self.con:
            self.msg3.config(text="Connected to databese.", fg="green")
        else:
            self.msg3.config(text="Not connected to databese.", fg="red")

        frm = self.option_frames[self.options_box.get()]

        for value in self.option_frames.values():  # hides all other frames except passed frame
            if value is not frm:
                value.pack_forget()
                value.reset()

        frm.pack()
        frm.update()

        self.debt_checker()

    def debt_checker(self):
        if not self.con:
            messagebox.showwarning("Accounting" ,"Failed to update database.")
            return

        try:
            cmd_checks_find = f"SELECT * FROM checks WHERE isPayed = 0"
            cmd_intallments_find = f"SELECT * FROM installments"

            debts = []
            curs = self.con.cursor()

            curs.execute(cmd_checks_find)
            results = curs.fetchall()

            for item in results:
                if datetime.strptime(item[2] ,"%Y-%m-%d").date() < datetime.today().date():
                    debts.append(item)
                    cmd_customer = f"UPDATE customers SET totalDebt = totalDebt + 1 WHERE code = {item[0]}"
                    curs.execute(cmd_customer)

            curs = self.con.cursor()
            for item in debts:
                cmd_debts_add = f"INSERT INTO debts VALUES({item[0]} , 'check' , {item[1]} , '{item[3]}' , '{item[2]}' , 0 , 0 , {item[4]} , 0 )"
                curs.execute(cmd_debts_add)
                # self.con.commit()

            curs = self.con.cursor()
            for item in debts:
                cmd_checks_delete = f"DELETE FROM checks WHERE cstCode = {item[0]} AND price = {item[1]} AND deadline = '{item[2]}' AND startingDate = '{item[3]}' AND isPayed = {item[4]}"
                curs.execute(cmd_checks_delete)
                # self.con.commit()


            debts = []
            curs = self.con.cursor()

            curs.execute(cmd_intallments_find)
            results = curs.fetchall()

            for item in results:
                temp1 = (date.today() - datetime.strptime(item[4] ,"%Y-%m-%d").date()).days / int(item[3])
                temp2 = int(temp1) - item[6]

                if temp2 >= 1 and not item[5]:
                    debts.append(item)
                    cmd_customer = f"UPDATE customers SET totalDebt = totalDebt + {temp2} WHERE code = {item[0]}"
                    curs.execute(cmd_customer)

            curs = self.con.cursor()
            for item in debts:
                temp1 = (date.today() - datetime.strptime(item[4] ,"%Y-%m-%d").date()).days / int(item[3])
                temp2 = int(temp1) - item[6]

                cmd_debts_add = f"INSERT INTO debts VALUES({item[0]} , 'installment' , {item[1]} , '{item[4]}' , '' , {temp2} , {item[3]} , {item[5]} , 0 )"
                curs.execute(cmd_debts_add)
                # self.con.commit()

            curs = self.con.cursor()
            for item in debts:
                temp1 = (date.today() - datetime.strptime(item[4] ,"%Y-%m-%d").date()).days / int(item[3])
                temp2 = int(temp1) - item[6]
                temp3 = item[2] - temp2 - item[6]

                if temp3 > 0:
                    cmd_intallments = f'''UPDATE installments SET number = {item[2] - temp2}  WHERE cstCode = {item[0]} AND price = {item[1]} AND number = {item[2]} AND 
                    interval = '{item[3]}' AND startingDate = '{item[4]}' AND isPayed = {item[5]} AND lastPayment = {item[6]}'''
                    
                else:
                    cmd_intallments = f'''UPDATE installments SET isPayed = {1} , number = {item[2] - temp2} WHERE cstCode = {item[0]} AND price = {item[1]} AND number = {item[2]} AND 
                    interval = '{item[3]}' AND startingDate = '{item[4]}' AND isPayed = {item[5]} AND lastPayment = {item[6]}'''
                    
                curs.execute(cmd_intallments)
                # self.con.commit()

            self.con.commit()

        except sqlite3.OperationalError as err:
            messagebox.showwarning("Accounting" ,"Database error: " + str(err))
            self.con.rollback()
            return

        except sqlite3.IntegrityError as err:
            messagebox.showwarning("Accounting" ,"Payment already exists.")
            self.con.rollback()
            return

        except:
            messagebox.showwarning("Accounting" ,"Whoops")
            self.con.rollback()
            return


if __name__ == "__main__":
    win = Tk()
    App(win)
    win.mainloop()