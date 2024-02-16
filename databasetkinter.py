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

def delete():
    data = sqlite3.connect('school.db')
    d = data.cursor()
    
    d.execute("DELETE from students WHERE oid = " + delete_ent.get())
    delete_ent.delete(0,END)
    
    data.commit()
    data.close()
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
        success_label.grid(row=7,column=0,columnspan=2)
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
        warning_label.grid(row=7,column=0,columnspan=2)

def show():
    data = sqlite3.connect('school.db')
    d = data.cursor()
    
    d.execute("SELECT * , oid FROM students")
    records = d.fetchall()
    
    window = Toplevel()
    
    font_size = 10
    s_no = Entry(window,width=5,font= ("Helvetica",font_size,"bold"),justify="center")
    s_no.insert(0,"S.No")
    s_no.grid(row=0,column = 0)
    
    first_name = Entry(window,width=12,font= ("Helvetica",font_size,"bold"),justify="center")
    first_name.insert(0,"First Name")
    first_name.grid(row=0,column = 1)
    
    last_name = Entry(window,width=12,font= ("Helvetica",font_size,"bold"),justify="center")
    last_name.insert(0,"Last Name")
    last_name.grid(row=0,column = 2)
    
    gradeshow = Entry(window,width=6,font= ("Helvetica",font_size,"bold"),justify="center")
    gradeshow.insert(0,"Class")
    gradeshow.grid(row=0,column = 3)
    
    phoneno = Entry(window,width=12,font= ("Helvetica",font_size,"bold"),justify="center")
    phoneno.insert(0,"Phone No")
    phoneno.grid(row=0,column = 4)
    
    i = 1
    for record in records:
        locals()['s_no'+str(i)] = Entry(window,width=5)
        locals()['s_no'+str(i)].insert(0,record[4])
        locals()['s_no'+str(i)].grid(row=i,column = 0)
        
        locals()['f_name'+str(i)] = Entry(window,width=12)
        locals()['f_name'+str(i)].insert(0,record[0])
        locals()['f_name'+str(i)].grid(row=i,column = 1)
        
        locals()['l_name'+str(i)] = Entry(window,width=12)
        locals()['l_name'+str(i)].insert(0,record[1])
        locals()['l_name'+str(i)].grid(row=i,column = 2)
        
        locals()['grade'+str(i)] = Entry(window,width=6)
        locals()['grade'+str(i)].insert(0,record[2])
        locals()['grade'+str(i)].grid(row=i,column = 3)
        
        locals()['phoneno'+str(i)] = Entry(window,width=12)
        locals()['phoneno'+str(i)].insert(0,"0"+str(record[3]))
        locals()['phoneno'+str(i)].grid(row=i,column = 4)
        
        
        i += 1
        
    
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

delete_ent = Entry(root,width=20)
delete_ent.grid(row=5, column=1)

#Creating Label
firstname_label = Label(root, text= "First Name" )
firstname_label.grid(row=0, column=0,sticky=E+W)

lastname_label = Label(root, text= "Last Name")
lastname_label.grid(row=1, column=0)

grade_label = Label(root, text= "Class")
grade_label.grid(row=2, column=0)

phone_no_label = Label(root, text= "Phone Number")
phone_no_label.grid(row=3, column=0)

delete_label = Label(root, text= "Delete ID")
delete_label.grid(row=5, column=0)

submit_btn = Button(root, text = "Submit",command=submit,padx=20,width=10)
submit_btn.grid(row=4,column=0,pady=15)
show_btn = Button(root, text = "Show Records",command=show,padx=20)
show_btn.grid(row=4,column=1,pady=5)
delete_btn = Button(root, text = "Delete",command=delete,padx=20,width=28)
delete_btn.grid(row=6, column=0,columnspan=2)



root.mainloop()