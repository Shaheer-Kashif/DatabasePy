from tkinter import *
import sqlite3
from tkinter import messagebox
import os

root = Tk()
root.title("School Database App")
root.iconbitmap("databasetkinter.ico")
show_pass = True
update_pass = True

def validate_input(new_text):
    if not new_text:
        return True
    try:
        int(new_text)
        return True
    except ValueError:
        return False
    
validation = root.register(validate_input)
root.configure(bg = "#313131")

if os.path.exists("school.db"):
    pass
else:
    data = sqlite3.connect('school.db')
    d = data.cursor()
    d.execute(""" CREATE TABLE students (
              firstname text,
			  lastname text,
              class text,
              phone_no integer
              )
          """)
    data.commit()
    data.close()
        
def delete():
    data = sqlite3.connect('school.db')
    d = data.cursor()
    d.execute(f"SELECT oid FROM students")
    oids = d.fetchall()
    oid_integers = [int(oid[0]) for oid in oids]
    if delete_ent.get() == "":
        messagebox.showwarning("Warning","Enter an ID to Delete.")
    else:
        if (int(delete_ent.get()) >= oid_integers[0]) and (int(delete_ent.get()) <= oid_integers[len(oid_integers)-1]):
            d.execute("DELETE from students WHERE oid = " + delete_ent.get())
            delete_ent.delete(0,END)
        else:
            messagebox.showerror("Error","This ID Doesn't Exist.")
    data.commit()
    data.close()
    

def submit():
    global window
    if firstname.get() == "" or lastname.get() == "" or grade.get() == "" or phone_no.get() == "":
        messagebox.showerror("Warning","Data Fields Can't be Empty.")
    else:
        if (int(grade.get()) >= 1 and int(grade.get()) <= 10) and (len(phone_no.get()) == 11):
            data = sqlite3.connect('school.db')
            d = data.cursor()
            
            d.execute("INSERT INTO students VALUES (:firstname , :lastname , :class , :phone_no)",
                    {"firstname":firstname.get(),
                    "lastname":lastname.get(),
                    "class":grade.get(),
                    "phone_no":phone_no.get()}
            )
            messagebox.showinfo("Success!",str(firstname.get()) +" "+str(lastname.get())+" added!")
            firstname.delete(0,END)
            lastname.delete(0,END)
            grade.delete(0,END)
            phone_no.delete(0,END)
            data.commit()
            data.close()
            try:
                window.destroy()
            except NameError:
                pass
            finally:
                show()
        else:
            if not((int(grade.get()) >= 1 and int(grade.get()) <= 10)) and not(len(phone_no.get()) == 11):
                messagebox.showwarning("Error","Invalid Class and Phone Number")
            elif not(len(phone_no.get()) == 11):
                messagebox.showwarning("Error","Invalid Phone Number")
            elif not((int(grade.get()) >= 1 and int(grade.get()) <= 10)):
                messagebox.showwarning("Error","Invalid Class")
   
def show():
    global window,show_pass,update_btn
    
    if show_pass == True:
        window = Toplevel()
        show_pass = False
        window.destroy()
        
    if window.winfo_exists():
        pass
    else:
        window = Toplevel()
        data = sqlite3.connect('school.db')
        d = data.cursor()
    
        d.execute("SELECT * , oid FROM students")
        records = d.fetchall()
     
        font_size = 10
        s_no = Entry(window,width=5,font= ("Helvetica",font_size,"bold"),justify="center")
        s_no.insert(0,"S.No")
        s_no.grid(row=0,column = 0)
        s_no.configure(state="readonly")
        
        first_name = Entry(window,width=14,font= ("Helvetica",font_size,"bold"),justify="center")
        first_name.insert(0,"First Name")
        first_name.grid(row=0,column = 1)
        first_name.configure(state="readonly")
        
        last_name = Entry(window,width=14,font= ("Helvetica",font_size,"bold"),justify="center")
        last_name.insert(0,"Last Name")
        last_name.grid(row=0,column = 2)
        last_name.configure(state="readonly")
        
        gradeshow = Entry(window,width=8,font= ("Helvetica",font_size,"bold"),justify="center")
        gradeshow.insert(0,"Class")
        gradeshow.grid(row=0,column = 3)
        gradeshow.configure(state="readonly")
        
        phoneno = Entry(window,width=12,font= ("Helvetica",font_size,"bold"),justify="center")
        phoneno.insert(0,"Phone No")
        phoneno.grid(row=0,column = 4)
        phoneno.configure(state="readonly")
        
        i = 1
        for record in records:
            locals()['s_no'+str(i)] = Entry(window,width=6,justify="right")
            locals()['s_no'+str(i)].insert(0,record[4])
            locals()['s_no'+str(i)].grid(row=i,column = 0)
            locals()['s_no'+str(i)].configure(state="readonly")
            
            locals()['f_name'+str(i)] = Entry(window,width=16,justify="center")
            locals()['f_name'+str(i)].insert(0,record[0])
            locals()['f_name'+str(i)].grid(row=i,column = 1)
            locals()['f_name'+str(i)].configure(state="readonly")
            
            locals()['l_name'+str(i)] = Entry(window,width=16,justify="center")
            locals()['l_name'+str(i)].insert(0,record[1])
            locals()['l_name'+str(i)].grid(row=i,column = 2)
            locals()['l_name'+str(i)].configure(state="readonly")
            
            locals()['grade'+str(i)] = Entry(window,width=9,justify="center")
            locals()['grade'+str(i)].insert(0,record[2])
            locals()['grade'+str(i)].grid(row=i,column = 3)
            locals()['grade'+str(i)].configure(state="readonly")
            
            locals()['phoneno'+str(i)] = Entry(window,width=14,justify="center")
            if len(str(record[3])) < 11:
                locals()['phoneno'+str(i)].insert(0,"0"+str(record[3]))
            else:
                locals()['phoneno'+str(i)].insert(0,str(record[3]))
            locals()['phoneno'+str(i)].grid(row=i,column = 4)
            locals()['phoneno'+str(i)].configure(state="readonly")

            i += 1
            
        update_btn = Button(window,text = "Update Record",command = update,bg = "#0086D3",fg="white",font = ("montserrat",12,"bold"))
        update_btn.grid(row = i,column=0,columnspan=5,pady = (10,5))
            
        data.commit()
        data.close()
    
def save():
    global firstname_editor, lastname_editor, grade_editor, phone_no_editor,val,editor
    if firstname_editor.get() == "" or lastname_editor.get() == "" or grade_editor.get() == "" or phone_no_editor.get() == "":
        messagebox.showerror("Warning","Data Fields Can't be Empty.")
    else:
        if (int(grade_editor.get()) >= 1 and int(grade_editor.get()) <= 10) and (len(phone_no_editor.get()) == 11):
            data = sqlite3.connect('school.db')
            d = data.cursor()
        
            d.execute("""UPDATE students SET firstname = :first ,
                        lastname = :last,
                        class = :grade,
                        phone_no = :phone
                        WHERE oid = :oid""",
                    {"first" : firstname_editor.get(),
                    "last" : lastname_editor.get(),
                    "grade" : grade_editor.get(),
                    "phone" : phone_no_editor.get(),
                    "oid" : val}
                    )
        else:
            if not((int(grade_editor.get()) >= 1 and int(grade_editor.get()) <= 10)) and not(len(phone_no_editor.get()) == 11):
                messagebox.showwarning("Error","Invalid Class and Phone Number")
            elif not(len(phone_no_editor.get()) == 11):
                messagebox.showwarning("Error","Invalid Phone Number")
            elif not((int(grade_editor.get()) >= 1 and int(grade.get()) <= 10)):
                messagebox.showwarning("Error","Invalid Class")
            
        data.commit()
        data.close()
        window.destroy()
        editor.destroy()
        show()
    
def edit():
    global id_input,input_window, firstname_editor, lastname_editor, grade_editor, phone_no_editor,val,editor,update_btn
    val = id_input.get()
    data = sqlite3.connect('school.db')
    update_btn.configure(state=DISABLED)
    d = data.cursor()
    d.execute(f"SELECT oid FROM students")
    oids = d.fetchall()
    oid_integers = [int(oid[0]) for oid in oids]
    if id_input.get() == "":
        messagebox.showwarning("Warning","Enter an ID.")
    else:
        if (int(val) >= oid_integers[0]) and (int(val) <= oid_integers[len(oid_integers)-1]):
            input_window.destroy()
            
            d.execute("SELECT * FROM students WHERE oid = " + val)
            records = d.fetchall()
            
            editor = Toplevel()
            editor.configure(bg="#313131")
            
            firstname_editor = Entry(editor,width=20)
            firstname_editor.grid(row=0, column=1,pady=(10,0),padx=5)

            lastname_editor = Entry(editor,width=20)
            lastname_editor.grid(row=1, column=1,padx=5)

            grade_editor = Entry(editor,width=20,validate="key", validatecommand=(validation, '%P'))
            grade_editor.grid(row=2, column=1,padx=5)

            phone_no_editor = Entry(editor,width=20,validate="key", validatecommand=(validation, '%P'))
            phone_no_editor.grid(row=3, column=1,padx=5)
            
            for record in records:
                firstname_editor.insert(0,record[0])
                lastname_editor.insert(0,record[1])
                grade_editor.insert(0,record[2])
                if len(str(record[3])) < 11:
                    phone_no_editor.insert(0,"0"+str(record[3]))
                else:
                    phone_no_editor.insert(0,str(record[3]))
                    

            #Creating Label
            firstname_label = Label(editor, text= "First Name",bg = "#313131",fg="white",font=("arial",12)) 
            firstname_label.grid(row=0, column=0,padx = 10,pady=(10,0))

            lastname_label = Label(editor, text= "Last Name",bg = "#313131",fg="white",font=("arial",12))
            lastname_label.grid(row=1, column=0,padx = 10)

            grade_label = Label(editor, text= "Class",bg = "#313131",fg="white",font=("arial",12))
            grade_label.grid(row=2, column=0,padx = 10)

            phone_no_label = Label(editor, text= "Phone Number",bg = "#313131",fg="white",font=("arial",12))
            phone_no_label.grid(row=3, column=0,padx = 10)
            
            save_btn = Button(editor,text = "Save Edit",command = save,bg="#1A7C28",fg="white",borderwidth=1,font = ("montserrat",12,"bold"),width = 10)
            save_btn.grid(row=4, column=0,columnspan=2,pady = 10)
            data.commit()
            data.close()
            
        else:
            messagebox.showerror("Error","This ID Doesn't Exist")
            id_input.delete(0,END)
    
       
        
    
def update():
    global id_input,input_window,update_pass
    if update_pass == True:
        input_window = Toplevel()
        update_pass = False
        input_window.destroy()
        
    if input_window.winfo_exists():
        pass
    else:
        input_window = Toplevel()
        prompt = Label(input_window, text = "Enter ID which you want to edit")
        prompt.pack()
        id_input = Entry(input_window,width = 15,font = ("Helvetica",18,"bold"),validate="key", validatecommand=(validation, '%P'))
        id_input.pack()
        enter = Button(input_window,text = "Edit",bg = "#0086D3",fg="white",font = ("montserrat",12,"bold"),width=10,command = edit)
        enter.pack(pady= 10)
                   
    
#Creating Entry
firstname = Entry(root,width=20)
firstname.grid(row=0, column=1,pady=(5,0))

lastname = Entry(root,width=20)
lastname.grid(row=1, column=1)

grade = Entry(root,width=20,validate="key", validatecommand=(validation, '%P'))
grade.grid(row=2, column=1)

phone_no = Entry(root,width=20,validate="key", validatecommand=(validation, '%P'))
phone_no.grid(row=3, column=1)

delete_ent = Entry(root,width=20,validate="key", validatecommand=(validation, '%P'))
delete_ent.grid(row=5, column=1)

#Creating Label"
firstname_label = Label(root, text= "First Name" ,bg = "#313131",fg="white",font=("arial",12))
firstname_label.grid(row=0, column=0,pady=(5,0))

lastname_label = Label(root, text= "Last Name",bg = "#313131",fg="white",font=("arial",12))
lastname_label.grid(row=1, column=0)

grade_label = Label(root, text= "Class",bg = "#313131",fg="white",font=("arial",12))
grade_label.grid(row=2, column=0)

phone_no_label = Label(root, text= "Phone Number",bg = "#313131",fg="white",font=("arial",12))
phone_no_label.grid(row=3, column=0)

delete_label = Label(root, text= "Delete ID",bg = "#313131",fg="white",font=("arial",12))
delete_label.grid(row=5, column=0)

submit_btn = Button(root, text = "Submit",command=submit,width=10,bg="#1A7C28",fg="white",borderwidth=1,font = ("montserrat",12,"bold"))
submit_btn.grid(row=4,column=0,pady=5)
show_btn = Button(root, text = "Show Records",command=show,width=14,bg="#1A7C28",fg="white",borderwidth=1,font = ("montserrat",12,"bold"))
show_btn.grid(row=4,column=1,pady=5)
delete_btn = Button(root, text = "Delete",command=delete,padx=5,width=25,bg="#8B1A1A",fg="white",borderwidth=1,font = ("montserrat",12,"bold"))
delete_btn.grid(row=6, column=0,columnspan=2,padx = 5,pady=5)



root.mainloop()