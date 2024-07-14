from tkinter import *
from PIL import ImageTk
from tkinter import messagebox
import sqlite3
import time
import email_pass
import subprocess
import smtplib

class Login_System:
    def __init__(self, root):
        self.root = root
        self.root.title("Super Mart Inventory | Login")
        self.root.geometry("1350x700+0+0")
        self.root.config(bg="#fafafa")
        self.otp=''
        self.phone_image = ImageTk.PhotoImage(file="images/phone.png")
        self.lbl_phone_image = Label(self.root, image=self.phone_image).place(x=200, y=50)

        login_frame = Frame(self.root, bd=2, relief=RIDGE, bg="white")
        login_frame.place(x=650, y=90, width=350, height=460)
        
        title = Label(login_frame, text="Login", font=("Elephant", 30, "bold"), bg="white").place(x=0, y=30, relwidth=1)
        self.employee_id = StringVar()
        self.password = StringVar()
        
        lbl_user = Label(login_frame, text="Employee Id", font=("Andalus", 15), bg="white", fg="#767171").place(x=50, y=100)
        txt_employee_id = Entry(login_frame, textvariable=self.employee_id, font=("times new roman", 15), bg="#ECECEC").place(x=50, y=140, width=250)
        
        lbl_pass = Label(login_frame, text="Password", font=("Andalus", 15), bg="white", fg="#767171").place(x=50, y=200)
        txt_pass = Entry(login_frame, textvariable=self.password, show="*", font=("times new roman", 15), bg="#ECECEC").place(x=50, y=240, width=250)

        btn_login = Button(login_frame, text="Log In", font=("Arial Rounded MT Bold", 15), bg="#00B0F0", activebackground="#00B0F0", fg="white", activeforeground="white", cursor="hand2", command=self.login)
        btn_login.place(x=50, y=300, width=250)

        hr = Label(login_frame, bg="lightgrey").place(x=50, y=370, width=250, height=2)
        or_ = Label(login_frame, text="OR", fg="lightgrey", bg="white", font=("times new roman", 15)).place(x=150, y=355)

        btn_forget = Button(login_frame, text="Forgot Password?", font=("times new roman", 13), bg="white", fg="#00759E", bd=0, cursor="hand2", activebackground="white", activeforeground="#00759E",command=self.forget_window)
        btn_forget.place(x=100, y=390)

        register_frame = Frame(self.root, bd=2, relief=RIDGE, bg="white")
        register_frame.place(x=650, y=570, width=350, height=60)

        lbl_reg = Label(register_frame, text="Super Mart Inventory System", font=("times new roman", 15, "bold"), bg="white").place(x=50, y=18)

        self.im1 = ImageTk.PhotoImage(file="images/im1.png")
        self.im2 = ImageTk.PhotoImage(file="images/im2.png")
        self.im3 = ImageTk.PhotoImage(file="images/im3.png")

        self.lbl_change_image = Label(self.root, bg="grey")
        self.lbl_change_image.place(x=369, y=154, width=240, height=428)
        self.animate()
        

    def login(self):
        con = sqlite3.connect(database='ims.db')
        cur = con.cursor()
        try:
            if self.employee_id.get() == "" or self.password.get() == "":
                messagebox.showerror("Error", "Please enter username and password", parent=self.root)
            else:
                cur.execute("select name,utype from employee where eid=? and pass=?", (self.employee_id.get(), self.password.get()))
                user = cur.fetchone()
                if user is None:
                    messagebox.showerror("Error", "Invalid username or password", parent=self.root)
                else:
                    if user[1]=="Admin":
                        messagebox.showinfo("Success", f"Welcome {user[0]}")
                        self.root.destroy()
                        subprocess.Popen(['python', 'dashboard.py', user[0]])
                    else:
                        messagebox.showinfo("Login Successful!!!", f"Welcome {user[0]}")
                        self.root.destroy()
                        subprocess.Popen(['python', 'billing.py', user[0]])
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to {str(ex)}", parent=self.root)

    def animate(self):
        self.im = self.im1
        self.im1 = self.im2
        self.im2 = self.im3
        self.im3 = self.im
        self.lbl_change_image.config(image=self.im)
        self.lbl_change_image.after(2000, self.animate)

    def forget_window(self):
        con=sqlite3.connect(database='ims.db')
        cur=con.cursor()
        try:
            if self.employee_id.get()=="":
                messagebox.showerror("Error","Employee ID must be required",parent=self.root)
            else:
                cur.execute("select email from employee where eid=?",(self.employee_id.get(),))
                email=cur.fetchone()
                if email==None:
                    messagebox.showerror("Error","Invalid Employee Id",parent=self.root)
                else:
                    self.var_otp=StringVar()
                    self.var_new_pass=StringVar()
                    self.var_conf_pass=StringVar()
                    chk=self.send_email(email[0])
                    if chk=='f':
                        messagebox.showerror("Error","Conection Error",parent=self.root)
                    else:
                        self.forget_win=Toplevel(self.root)
                        self.forget_win.title("Reset Password")
                        self.forget_win.geometry("400x350+500+100")
                        self.forget_win.focus_force()

                        title=Label(self.forget_win,text="Reset Password",font=('goudy old style',15,"bold"),bg="#3f51b5",fg="white").pack(side=TOP,fill=X)
                        lbl_reset=Label(self.forget_win,text="Enter OTP sent on registered Email",font=("times new roman",15)).place(x=20,y=60)
                        txt_reset=Entry(self.forget_win,textvariable=self.var_otp,font=("times new roman",15),bg="lightyellow").place(x=20,y=100,width=250,height=30)

                        self.btn_reset=Button(self.forget_win,text="Submit",command=self.validate_otp,font=("times new roman",12),bg="lightblue",cursor="hand2")
                        self.btn_reset.place(x=280,y=100,width=100,height=30)

                        new_pass=Label(self.forget_win,text="New Password",font=("times new roman",15)).place(x=20,y=160)
                        txt_new_pass=Entry(self.forget_win,textvariable=self.var_new_pass,show="*",font=("times new roman",15),bg="lightyellow").place(x=20,y=190,width=250,height=30)

                        confirm_pass=Label(self.forget_win,text="Confirm Password",font=("times new roman",15)).place(x=20,y=225)
                        txt_confirm_pass=Entry(self.forget_win,textvariable=self.var_conf_pass,show="*",font=("times new roman",15),bg="lightyellow").place(x=20,y=255,width=250,height=30)

                        self.btn_update=Button(self.forget_win,text="Update",command=self.update_password,font=("times new roman",12),bg="lightblue",cursor="hand2",state=DISABLED)
                        self.btn_update.place(x=150,y=300,width=100,height=30)

        except Exception as ex:
            messagebox.showerror("Error",f"Error due to {str(ex)}")

    def validate_otp(self):
        if int(self.otp)==int(self.var_otp.get()):
            self.btn_update.config(state=NORMAL)
            self.btn_reset.config(state=DISABLED)
        else:
            messagebox.showerror("Error","Invalid OTP!!!\nPlease recheck and try again",parent=self.root)

    def update_password(self):
        if self.var_new_pass.get()=="" or self.var_conf_pass.get()=="":
            messagebox.showerror("Error","Please enter new password and confirm password",parent=self.root)
        elif self.var_new_pass.get()!=self.var_conf_pass.get():
            messagebox.showerror("Error","New Password and Confirm Password should be same",parent=self.root)
        else:
            con=sqlite3.connect(database='ims.db')
            cur=con.cursor()
            try:
                cur.execute("update employee set pass=? where eid=?",(self.var_new_pass.get(),self.employee_id.get(),))
                con.commit()
                messagebox.showinfo("Success","Password updated successfully")
                self.forget_win.destroy()

            except Exception as ex:
                messagebox.showerror("Error",f"Error due to {str(ex)}",parent=self.root)


    def send_email(self,to_):
        s=smtplib.SMTP('smtp.gmail.com',587)
        s.starttls()
        email_=email_pass.email_
        pass_=email_pass.pass_
        s.login(email_,pass_)
        self.otp=int(time.strftime("%H%S%M"))+int(time.strftime("%S"))
        subj='Reset Password-Super Mart Inventory'
        msg=f"Dear Sir/Madam,\n\nYour OTP for Reset Password is: {str(self.otp)}\nOTP is valid only for 5 minutes\nIf you have not requested this please ignore this mail\n\nWith Regards,\nSuper Mart Inventory Team"
        msg="Subject:{}\n\n{}".format(subj,msg)
        s.sendmail(email_,to_,msg)
        chk=s.ehlo()
        if chk[0]==250:
            return 's'
        else:
            return 'f'

        
root = Tk()
obj = Login_System(root)
root.mainloop()
