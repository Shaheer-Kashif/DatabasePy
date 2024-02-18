from tkinter import *
import sqlite3
import time

root = Tk()
root.title("Database App")

def validate_input(new_text):
    if not new_text:
        return True
    try:
        int(new_text)
        return True
    except ValueError:
        return False
    
validation = root.register(validate_input)

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
    d.execute(f"SELECT oid FROM students")
    oids = d.fetchall()
    oid_integers = [int(oid[0]) for oid in oids]
    if (int(delete_ent.get()) >= oid_integers[0]) and (int(delete_ent.get()) <= oid_integers[len(oid_integers)-1]):
        d.execute("DELETE from students WHERE oid = " + delete_ent.get())
        delete_ent.delete(0,END)
    else:
        warning_label= Label(root,text="Invalid ID", width=30, anchor="center")
        warning_label.grid(row=7,column=0,columnspan=2)
    data.commit()
    data.close()
    

def submit():
    global window
    if (int(grade.get()) >= 1 and int(grade.get()) <= 10) and (len(phone_no.get()) == 11):
        data = sqlite3.connect('school.db')
        d = data.cursor()
        
        d.execute("INSERT INTO students VALUES (:firstname , :lastname , :class , :phone_no)",
                  {"firstname":firstname.get(),
                   "lastname":lastname.get(),
                   "class":grade.get(),
                   "phone_no":phone_no.get()}
        )
        success_label= Label(root,text=str(firstname.get()) +" "+str(lastname.get())+" added!", width=30, anchor="center")
        success_label.grid(row=7,column=0,columnspan=2)
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
            warning_label= Label(root,text="Invalid Class and Phone Number", width=30, anchor="center")
        elif not(len(phone_no.get()) == 11):
            warning_label= Label(root,text="Invalid Phone Number", width=30, anchor="center")
        elif not((int(grade.get()) >= 1 and int(grade.get()) <= 10)):
            warning_label= Label(root,text="Invalid Class", width=30, anchor="center")
        warning_label.grid(row=7,column=0,columnspan=2)
   
    
def show():
    global window
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
    
    gradeshow = Entry(window,width=8,font= ("Helvetica",font_size,"bold"),justify="center")
    gradeshow.insert(0,"Class")
    gradeshow.grid(row=0,column = 3)
    
    phoneno = Entry(window,width=12,font= ("Helvetica",font_size,"bold"),justify="center")
    phoneno.insert(0,"Phone No")
    phoneno.grid(row=0,column = 4)
    
    i = 1
    for record in records:
        locals()['s_no'+str(i)] = Entry(window,width=6,justify="right")
        locals()['s_no'+str(i)].insert(0,record[4])
        locals()['s_no'+str(i)].grid(row=i,column = 0)
        
        locals()['f_name'+str(i)] = Entry(window,width=14,justify="center")
        locals()['f_name'+str(i)].insert(0,record[0])
        locals()['f_name'+str(i)].grid(row=i,column = 1)
        
        locals()['l_name'+str(i)] = Entry(window,width=14,justify="center")
        locals()['l_name'+str(i)].insert(0,record[1])
        locals()['l_name'+str(i)].grid(row=i,column = 2)
        
        locals()['grade'+str(i)] = Entry(window,width=9,justify="center")
        locals()['grade'+str(i)].insert(0,record[2])
        locals()['grade'+str(i)].grid(row=i,column = 3)
        
        locals()['phoneno'+str(i)] = Entry(window,width=14,justify="center")
        locals()['phoneno'+str(i)].insert(0,"0"+str(record[3]))
        locals()['phoneno'+str(i)].grid(row=i,column = 4)

        i += 1
        
    update_btn = Button(window,text = "Update Record",command = update)
    update_btn.grid(row = i,column=2,pady = (10,5))
        
    data.commit()
    data.close()
    
def save():
    global firstname_editor, lastname_editor, grade_editor, phone_no_editor,val,editor
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
                 
        
    data.commit()
    data.close()
    window.destroy()
    editor.destroy()
    show()
    
def edit():
    global id_input,input_window, firstname_editor, lastname_editor, grade_editor, phone_no_editor,val,editor
    val = id_input.get()
    input_window.destroy()
    data = sqlite3.connect('school.db')
    
    d = data.cursor()
    d.execute("SELECT * FROM students WHERE oid = " + val)
    records = d.fetchall()
    
    editor = Toplevel()
    
    firstname_editor = Entry(editor,width=20)
    firstname_editor.grid(row=0, column=1)

    lastname_editor = Entry(editor,width=20)
    lastname_editor.grid(row=1, column=1)

    grade_editor = Entry(editor,width=20,validate="key", validatecommand=(validation, '%P'))
    grade_editor.grid(row=2, column=1)

    phone_no_editor = Entry(editor,width=20,validate="key", validatecommand=(validation, '%P'))
    phone_no_editor.grid(row=3, column=1)
    
    for record in records:
        firstname_editor.insert(0,record[0])
        lastname_editor.insert(0,record[1])
        grade_editor.insert(0,record[2])
        phone_no_editor.insert(0,"0"+str(record[3]))

    #Creating Label
    firstname_label = Label(editor, text= "First Name" )
    firstname_label.grid(row=0, column=0,sticky=E+W)

    lastname_label = Label(editor, text= "Last Name")
    lastname_label.grid(row=1, column=0)

    grade_label = Label(editor, text= "Class")
    grade_label.grid(row=2, column=0)

    phone_no_label = Label(editor, text= "Phone Number")
    phone_no_label.grid(row=3, column=0)
    
    save_btn = Button(editor,text = "Save Edit",command = save)
    save_btn.grid(row=4, column=0,columnspan=2,pady = 10)

    
    data.commit()
    data.close()
    
def update():
    global id_input,input_window
    input_window = Toplevel()
    prompt = Label(input_window, text = "Enter ID which you want to edit")
    prompt.pack()
    id_input = Entry(input_window,width = 15,font = ("Helvetica",18,"bold"),validate="key", validatecommand=(validation, '%P'))
    id_input.pack()
    enter = Button(input_window,text = "Edit",font = ("Helvetica",12),width=10,command = edit)
    enter.pack(pady= 10)
                   
    
#Creating Entry
firstname = Entry(root,width=20)
firstname.grid(row=0, column=1)

lastname = Entry(root,width=20)
lastname.grid(row=1, column=1)

grade = Entry(root,width=20,validate="key", validatecommand=(validation, '%P'))
grade.grid(row=2, column=1)

phone_no = Entry(root,width=20,validate="key", validatecommand=(validation, '%P'))
phone_no.grid(row=3, column=1)

delete_ent = Entry(root,width=20,validate="key", validatecommand=(validation, '%P'))
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
delete_btn.grid(row=6, column=0,columnspan=2,padx = 5,pady=5)



root.mainloop()