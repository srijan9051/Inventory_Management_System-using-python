from tkinter import *
from PIL import Image,ImageTk
from tkinter import ttk
from tkinter import messagebox
import sqlite3

class productClass:
    def __init__(self,root):
        self.root=root
        self.root.geometry("1100x500+220+130")
        self.root.title("Super Mart Inventory | Product")
        self.root.config(bg="white")
        self.root.focus_force()
        #===========variables============#
        self.var_searchby=StringVar()
        self.var_searchtxt=StringVar()
        self.var_pid=StringVar()
        self.var_cat=StringVar()
        self.var_sup=StringVar()
        self.cat_list=[]
        self.sup_list=[]
        self.fetch_cat_sup()
        self.var_name=StringVar()
        self.var_price=StringVar()
        self.var_qty=StringVar()
        self.var_status=StringVar()

        product_Frame=Frame(self.root,bd=2,relief=RIDGE,bg="white")
        product_Frame.place(x=10,y=10,width=450,height=480)

        #============title=============#
        title=Label(product_Frame,text="Manage Product Details",font=("goudy old style",18),bg="#0f4d7d",fg="white").pack(side=TOP,fill=X)
        #===========Label==============#
        lbl_category=Label(product_Frame,text="Category",font=("goudy old style",18),bg="white").place(x=30,y=60)
        lbl_supplier=Label(product_Frame,text="Supplier",font=("goudy old style",18),bg="white").place(x=30,y=110)
        lbl_product=Label(product_Frame,text="Name",font=("goudy old style",18),bg="white").place(x=30,y=160)
        lbl_price=Label(product_Frame,text="Price",font=("goudy old style",18),bg="white").place(x=30,y=210)
        lbl_qty=Label(product_Frame,text="Quantity",font=("goudy old style",18),bg="white").place(x=30,y=260)
        lbl_status=Label(product_Frame,text="Status",font=("goudy old style",18),bg="white").place(x=30,y=310)

        #=======combo==========#
        cmb_cat=ttk.Combobox(product_Frame,textvariable=self.var_cat,values=self.cat_list,state='readonly',justify=CENTER,font=("goudy old style",15))
        cmb_cat.place(x=150,y=60,width=200)
        cmb_cat.current(0)

        #=======combo==========#
        cmb_sup=ttk.Combobox(product_Frame,textvariable=self.var_sup,values=self.sup_list,state='readonly',justify=CENTER,font=("goudy old style",15))
        cmb_sup.place(x=150,y=110,width=200)
        cmb_sup.current(0)

        txt_name=Entry(product_Frame,textvariable=self.var_name,font=("goudy old style",15),bg="lightyellow").place(x=150,y=160,width=200)
        txt_price=Entry(product_Frame,textvariable=self.var_price,font=("goudy old style",15),bg="lightyellow").place(x=150,y=210,width=200)
        txt_qty=Entry(product_Frame,textvariable=self.var_qty,font=("goudy old style",15),bg="lightyellow").place(x=150,y=260,width=200)

        #=======combo==========#
        cmb_status=ttk.Combobox(product_Frame,textvariable=self.var_status,values=("Select","Active","Inactive"),state='readonly',justify=CENTER,font=("goudy old style",15))
        cmb_status.place(x=150,y=310,width=200)
        cmb_status.current(0)


        #===============Button============#
        btn_add=Button(product_Frame,text="Save",font=("goudy old style",15),bg="#2196f3",fg="white",cursor="hand2",command=self.add).place(x=10,y=400,width=100,height=40)
        btn_update=Button(product_Frame,text="Update",command=self.update,font=("goudy old style",15),bg="#4caf50",fg="white",cursor="hand2").place(x=120,y=400,width=100,height=40)
        btn_delete=Button(product_Frame,text="Delete",command=self.delete,font=("goudy old style",15),bg="#f44336",fg="white",cursor="hand2").place(x=230,y=400,width=100,height=40)
        btn_clear=Button(product_Frame,text="Clear",command=self.clear,font=("goudy old style",15),bg="#607d8b",fg="white",cursor="hand2").place(x=340,y=400,width=100,height=40)

         #===========search===========#
        searchFrame=LabelFrame(self.root,text="Search Product",font=("goudy old style",12,"bold"),bd=2,relief=RIDGE,bg="white")
        searchFrame.place(x=480,y=10,width=600,height=80)

        #============options=========#
        cmb_search=ttk.Combobox(searchFrame,textvariable=self.var_searchby,values=("Select","Category","Supplier","Name"),state='readonly',justify=CENTER,font=("goudy old style",15))
        cmb_search.place(x=10,y=10,width=180)
        cmb_search.current(0)

        txt_search=Entry(searchFrame,textvariable=self.var_searchtxt,font=("goudy old style",15),bg="lightyellow").place(x=200,y=10)
        btn_search=Button(searchFrame,text="Search",command=self.search,font=("goudy old style",15),bg="#4caf50",fg="white",cursor="hand2").place(x=410,y=9,width=150,height=30)


        #===========Product Details=========
        p_frame=Frame(self.root,bd=3,relief=RIDGE)
        p_frame.place(x=480,y=100,width=600,height=390)

        scrolly=Scrollbar(p_frame,orient=VERTICAL)
        scrollx=Scrollbar(p_frame,orient=HORIZONTAL)

        self.ProductTable=ttk.Treeview(p_frame,columns=("pid","category","supplier","name","price","qty","status"),yscrollcommand=scrolly.set,xscrollcommand=scrollx.set)
        scrollx.pack(side=BOTTOM,fill=X)
        scrolly.pack(side=RIGHT,fill=Y)
        scrollx.config(command=self.ProductTable.xview)
        scrolly.config(command=self.ProductTable.yview)
        self.ProductTable.heading("pid",text="Product Id")
        self.ProductTable.heading("category",text="Category")
        self.ProductTable.heading("supplier",text="Supplier")
        self.ProductTable.heading("name",text="Name")
        self.ProductTable.heading("price",text="Price")
        self.ProductTable.heading("qty",text="Quantity")
        self.ProductTable.heading("status",text="Status")
        self.ProductTable["show"]="headings"
        self.ProductTable.column("pid",width=75)
        self.ProductTable.column("category",width=100)
        self.ProductTable.column("supplier",width=100)
        self.ProductTable.column("name",width=100)
        self.ProductTable.column("price",width=100)
        self.ProductTable.column("qty",width=100)
        self.ProductTable.column("status",width=100)
        self.ProductTable.pack(fill=BOTH,expand=1)
        self.ProductTable.bind("<ButtonRelease-1>",self.get_data)
        self.show()
        self.fetch_cat_sup()

    def fetch_cat_sup(self):
        con=sqlite3.connect(database='ims.db')
        cur=con.cursor()
        try:
            cur.execute("select name from category")
            cat=cur.fetchall()
            self.cat_list.append("Empty")
            if len(cat)>0:
                del self.cat_list[:]
                self.cat_list.append("Select")
                for i in cat:
                    self.cat_list.append(i[0])
            cur.execute("select name from supplier")
            sup=cur.fetchall()
            self.sup_list.append("Empty")
            if len(sup)>0:
                del self.sup_list[:]
                self.sup_list.append("Select")
                for i in sup:
                    self.sup_list.append(i[0])

        except Exception as ex:
            messagebox.showerror("Error",f"Error due is : {str(ex)}",parent=self.root)



    def add(self):
        con=sqlite3.connect(database='ims.db')
        cur=con.cursor()
        try:
            if self.var_cat.get()=="Select" or self.var_cat.get()=="Empty" or self.var_sup.get()=="Select" or self.var_sup.get()=="Empty" or self.var_name=="" or self.var_status.get()=="Select":
                messagebox.showerror("Error","All fields are required",parent=self.root)
            else:
                cur.execute("Select * from product where name=?",(self.var_name.get(),))
                row=cur.fetchone()
                if row!=None:
                    messagebox.showerror("Error","This product is present",parent=self.root)
                else:
                    cur.execute("Insert into product (category,supplier,name,price,qty,status) values(?,?,?,?,?,?)",(
                                        self.var_cat.get(),
                                        self.var_sup.get(),
                                        self.var_name.get(),
                                        self.var_price.get(),
                                        self.var_qty.get(),
                                        self.var_status.get(),
                    ))
                    con.commit()
                    messagebox.showinfo("Success","Product added Successfully",parent=self.root)
                    self.show()
                    self.clear()
        except Exception as ex:
            messagebox.showerror("Error",f"Error due is : {str(ex)}",parent=self.root)


    def show(self):
        con=sqlite3.connect(database='ims.db')
        cur=con.cursor()
        try:
            cur.execute("select * from product")
            rows=cur.fetchall()
            self.ProductTable.delete(*self.ProductTable.get_children())
            for row in rows:
                self.ProductTable.insert('',END,values=row)

        except Exception as ex:
            messagebox.showerror("Error",f"Error due is : {str(ex)}",parent=self.root)


    def get_data(self,ev):
        f=self.ProductTable.focus()
        content=(self.ProductTable.item(f))
        row=content['values']
        self.var_pid.set(row[0])
        self.var_cat.set(row[1])
        self.var_sup.set(row[2])
        self.var_name.set(row[3])
        self.var_price.set(row[4])
        self.var_qty.set(row[5])
        self.var_status.set(row[6])
        

    def update(self):
        con=sqlite3.connect(database='ims.db')
        cur=con.cursor()
        try:
            if self.var_name.get()=="":
                messagebox.showerror("Error","Please select product from the list",parent=self.root)
            else:
                cur.execute("Select * from product where pid=?",(self.var_pid.get(),))
                row=cur.fetchone()
                if row==None:
                    messagebox.showerror("Error","Invalid Name",parent=self.root)
                else:
                    cur.execute("update product set category=?,supplier=?,name=?,price=?,qty=?,status=? where pid=?",(
                                        
                                        self.var_cat.get(),
                                        self.var_sup.get(),
                                        self.var_name.get(),
                                        self.var_price.get(),
                                        self.var_qty.get(),
                                        self.var_status.get(),
                                        self.var_pid.get(),
                    ))
                    con.commit()
                    messagebox.showinfo("Success","Product Updated Successfully",parent=self.root)
                    self.show()
                    self.clear()
        except Exception as ex:
            messagebox.showerror("Error",f"Error due is : {str(ex)}",parent=self.root)


    def delete(self):
        con=sqlite3.connect(database='ims.db')
        cur=con.cursor()
        try:
            if self.var_name.get()=="":
                messagebox.showerror("Error","Please select a product from the list",parent=self.root)
            else:
                cur.execute("Select * from product where name=?",(self.var_name.get(),))
                row=cur.fetchone()
                if row==None:
                    messagebox.showerror("Error","Invalid Product Name",parent=self.root)
                else:
                    op=messagebox.askyesno("Confirm","Do you really want to delete?",parent=self.root)
                    if op==True:
                        cur.execute("delete from product where name=?",(self.var_name.get(),))
                        con.commit()
                        messagebox.showinfo("Delete","Data deleted successfully",parent=self.root)
                        self.show()
                        self.clear()

        except Exception as ex:
            messagebox.showerror("Error",f"Error due is : {str(ex)}",parent=self.root)


    def clear(self):
        self.var_searchby.set("Select")
        self.var_searchtxt.set("")
        self.var_cat.set("Select")
        self.var_sup.set("Select")
        self.var_name.set("")
        self.var_price.set("")
        self.var_qty.set("")
        self.var_status.set("Select")
        self.show()


    def search(self):
        con=sqlite3.connect(database='ims.db')
        cur=con.cursor()
        try:
            if self.var_searchby.get()=="Select":
                messagebox.showerror("Error","Select search by option",parent=self.root)
            elif self.var_searchtxt.get()=="":
                messagebox.showerror("Error","Search area should not be empty",parent=self.root)
            elif self.var_searchby.get()=="Category":
                cur.execute("select * from product where category "+" LIKE '%"+self.var_searchtxt.get()+"%'")
                rows=cur.fetchall()
                if len(rows)!=0:
                    self.ProductTable.delete(*self.ProductTable.get_children())
                    for row in rows:
                        self.ProductTable.insert('',END,values=row)
                else:
                    messagebox.showerror("Error","No record found",parent=self.root)
            else:
                cur.execute("select * from product where "+self.var_searchby.get()+" LIKE '%"+self.var_searchtxt.get()+"%'")
                rows=cur.fetchall()
                if len(rows)!=0:
                    self.ProductTable.delete(*self.ProductTable.get_children())
                    for row in rows:
                        self.ProductTable.insert('',END,values=row)
                else:
                    messagebox.showerror("Error","No record found",parent=self.root)


        except Exception as ex:
            messagebox.showerror("Error",f"Error due is : {str(ex)}",parent=self.root)
        


if __name__=="__main__":
    root=Tk()
    obj=productClass(root)
    root.mainloop()