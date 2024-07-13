from tkinter import *
from PIL import Image,ImageTk
from employee import employeeClass
from supplier import supplierClass
from category import categoryClass
from product import productClass
from sales import salesClass
import sqlite3
from tkinter import messagebox
import os
import time
import sys

class IMS:
    def __init__(self,root,admin_name):
        self.root=root
        self.root.geometry("1350x700+0+0")
        self.root.title("Super Mart Inventory | Dashboard")
        self.root.config(bg="white")
        #....title...#
        self.icon_title=PhotoImage(file="images/logo1.png")
        title=Label(self.root,text="Inventory Management System",image=self.icon_title,compound=LEFT,font=("times new roman",40,"bold"),bg="#010c48",fg="white",anchor="w",padx=40).place(x=0,y=0,relwidth=1,height=70)
        self.admin_name=admin_name
        #....btn_logout.....#
        btn_logout=Button(self.root,text="Logout",font=("times new roman",15,"bold"),bg="yellow",cursor="hand2",command=self.logout)
        btn_logout.place(x=1150,y=10,height=50,width=150)

        #....clock....#
        self.lbl_clock=Label(self.root,text=f"Welcome {self.admin_name} to Super Mart \t\tDate: DD/MM/YYYY\t\t Time: HH:MM:SS",font=("times new roman",15),bg="#4d636d",fg="white")
        self.lbl_clock.place(x=0,y=70,relwidth=1,height=30)
        #...left menu....#
        self.MenuLogo=Image.open("images/menu_im.png")
        self.MenuLogo=self.MenuLogo.resize((200,200))
        self.MenuLogo=ImageTk.PhotoImage(self.MenuLogo)
        LeftMenu=Frame(self.root,bd=2,relief=RIDGE,bg="white")
        LeftMenu.place(x=0,y=102,width=200,height=565)
        lbl_menuLogo=Label(LeftMenu,image=self.MenuLogo)
        lbl_menuLogo.pack(side=TOP,fill=X)

        self.icon_side=PhotoImage(file="images/side.png")

        lbl_menu=Label(LeftMenu,text="Menu",font=("times new roman",20),bg="#009688").pack(side=TOP,fill=X)
        btn_employee=Button(LeftMenu,text="Employee",image=self.icon_side,compound=LEFT,padx=5,anchor="w",command=self.employee,font=("times new roman",20,"bold"),bg="white",bd=3,cursor="hand2").pack(side=TOP,fill=X)
        btn_supplier=Button(LeftMenu,text="Supplier",image=self.icon_side,compound=LEFT,padx=5,anchor="w",command=self.supplier,font=("times new roman",20,"bold"),bg="white",bd=3,cursor="hand2").pack(side=TOP,fill=X)
        btn_category=Button(LeftMenu,text="Category",image=self.icon_side,compound=LEFT,padx=5,anchor="w",command=self.category,font=("times new roman",20,"bold"),bg="white",bd=3,cursor="hand2").pack(side=TOP,fill=X)
        btn_product=Button(LeftMenu,text="Product",image=self.icon_side,compound=LEFT,padx=5,anchor="w",command=self.product,font=("times new roman",20,"bold"),bg="white",bd=3,cursor="hand2").pack(side=TOP,fill=X)
        btn_sales=Button(LeftMenu,text="Sales",image=self.icon_side,compound=LEFT,padx=5,anchor="w",command=self.sales,font=("times new roman",20,"bold"),bg="white",bd=3,cursor="hand2").pack(side=TOP,fill=X)
        btn_exit=Button(LeftMenu,text="Exit",image=self.icon_side,compound=LEFT,padx=5,anchor="w",font=("times new roman",20,"bold"),bg="white",bd=3,cursor="hand2").pack(side=TOP,fill=X)
        #======Content====#
        self.lbl_employee=Label(self.root,text="Total Employee\n[ 0 ]",bd=5,relief=RIDGE,bg="#33bbf9",fg="white",font=("goudy old style",20,"bold"))
        self.lbl_employee.place(x=300,y=120,height=150,width=300)

        self.lbl_supplier=Label(self.root,text="Total Supplier\n[ 0 ]",bd=5,relief=RIDGE,bg="#ff5722",fg="white",font=("goudy old style",20,"bold"))
        self.lbl_supplier.place(x=650,y=120,height=150,width=300)

        self.lbl_category=Label(self.root,text="Total Category\n[ 0 ]",bd=5,relief=RIDGE,bg="#009688",fg="white",font=("goudy old style",20,"bold"))
        self.lbl_category.place(x=1000,y=120,height=150,width=300)

        self.lbl_product=Label(self.root,text="Total Product\n[ 0 ]",bd=5,relief=RIDGE,bg="#607d8b",fg="white",font=("goudy old style",20,"bold"))
        self.lbl_product.place(x=300,y=300,height=150,width=300)

        self.lbl_sales=Label(self.root,text="Total Sales\n[ 0 ]",bd=5,relief=RIDGE,bg="#ffc107",fg="white",font=("goudy old style",20,"bold"))
        self.lbl_sales.place(x=650,y=300,height=150,width=300)


         #....footer....#
        lbl_footer=Label(self.root,text="IMS- Inventory Management System | Developed By Srijan\nFor any Technical Issue Contact: 8620018912 ",font=("times new roman",12),bg="#4d636d",fg="white").pack(side=BOTTOM,fill=X)
        self.update_content()
        #=======================================================
    def employee(self):
        self.new_win=Toplevel(self.root)
        self.new_obj=employeeClass(self.new_win)

    def supplier(self):
        self.new_win=Toplevel(self.root)
        self.new_obj=supplierClass(self.new_win)

    def category(self):
        self.new_win=Toplevel(self.root)
        self.new_obj=categoryClass(self.new_win)

    def product(self):
        self.new_win=Toplevel(self.root)
        self.new_obj=productClass(self.new_win)

    def sales(self):
        self.new_win=Toplevel(self.root)
        self.new_obj=salesClass(self.new_win)

    def update_content(self):
        con=sqlite3.connect(database='ims.db')
        cur=con.cursor()
        try:
            cur.execute("select * from employee")
            employee=cur.fetchall()
            self.lbl_employee.config(text=f"Total Employee\n[ {str(len(employee))} ]")
            cur.execute("select * from supplier")
            supplier=cur.fetchall()
            self.lbl_supplier.config(text=f"Total Supplier\n[ {str(len(supplier))} ]")
            cur.execute("select * from category")
            category=cur.fetchall()
            self.lbl_category.config(text=f"Total Category\n[ {str(len(category))} ]")
            cur.execute("select * from product")
            product=cur.fetchall()
            self.lbl_product.config(text=f"Total Product\n[ {str(len(product))} ]")
            bill=len(os.listdir('bill'))
            self.lbl_sales.config(text=f"Total Sales\n[ {str(bill)} ]")
            time_=time.strftime("%I:%M:%S")
            date_=time.strftime("%d/%m/%Y")
            self.lbl_clock.config(text=f"Hi {self.admin_name}, Welcome to Super Mart \t\tDate: {str(date_)}\t\t Time: {str(time_)}")
            self.lbl_clock.after(200,self.update_content)
            
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to {str(ex)}")

    def logout(self):
        op=messagebox.askyesno("Confirm","Are you sure to logout?")
        if op==True:
            messagebox.showinfo("Logout Successful",f"\nThanks {self.admin_name} for using our service")
            self.root.destroy()
            os.system("python login.py")
        

if __name__=="__main__":
    root=Tk()
    admin_name=sys.argv[1]
    obj=IMS(root,admin_name)
    root.mainloop()