from tkinter import *
import sqlite3

root = Tk()
root.title("Database App")

'''
d.execute(""" CREATE TABLE students (
              firstname text,
			  lastname text,
              class text,
              phone_no integer
              )
          """)
'''

def submit():
    if (int(grade.get()) >= 1 and int(grade.get()) <= 10) and (len(phone_no.get()) == 11):
        data = sqlite3.connect('school.db')
        d = data.cursor()
        
        d.execute("INSERT INTO students VALUES (:firstname , :lastname , :class , :phone_no)",
                  {"firstname":firstname.get(),
                   "lastname":lastname.get(),
                   "class":grade.get(),
                   "phone_no":phone_no.get()}
        )
        success_label= Label(root,text=str(firstname.get()) +" "+str(lastname.get())+"added!")
        success_label.grid(row=5,column=0,columnspan=2)
        firstname.delete(0,END)
        lastname.delete(0,END)
        grade.delete(0,END)
        phone_no.delete(0,END)
        
        data.commit()
        data.close()
    else:
        if not((int(grade.get()) >= 1 and int(grade.get()) <= 10)) and not(len(phone_no.get()) == 11):
            warning_label= Label(root,text="Invalid Class and Phone Number")
        elif not(len(phone_no.get()) == 11):
            warning_label= Label(root,text="Invalid Phone Number")
        elif not((int(grade.get()) >= 1 and int(grade.get()) <= 10)):
            warning_label= Label(root,text="Invalid Class")
        warning_label.grid(row=5,column=0,columnspan=2)

def show():
    data = sqlite3.connect('school.db')
    d = data.cursor()
    
    d.execute("SELECT * , oid FROM students")
    records = d.fetchall()
    
    new_record = ""
    for record in records:
        new_record += str(record[0]) +" "+ str(record[1]) + " Class: " +str(record[2]) + "\n"
        
    display_label = Label(root,text = new_record)
    display_label.grid(row=5,column=0,columnspan=2)
    data.commit()
    data.close()
    
#Creating Entry
firstname = Entry(root,width=20)
firstname.grid(row=0, column=1)

lastname = Entry(root,width=20)
lastname.grid(row=1, column=1)

grade = Entry(root,width=20)
grade.grid(row=2, column=1)

phone_no = Entry(root,width=20)
phone_no.grid(row=3, column=1)

#Creating Label
firstname_label = Label(root, text= "First Name" )
firstname_label.grid(row=0, column=0,sticky=E+W)

lastname_label = Label(root, text= "Last Name")
lastname_label.grid(row=1, column=0)

grade_label = Label(root, text= "Class")
grade_label.grid(row=2, column=0)

phone_no_label = Label(root, text= "Phone Number")
phone_no_label.grid(row=3, column=0)

submit_btn = Button(root, text = "Submit",command=submit,padx=20,width=10)
submit_btn.grid(row=4,column=0,pady=10)
show_btn = Button(root, text = "Show Records",command=show,padx=20)
show_btn.grid(row=4,column=1,pady=10)

root.mainloop()