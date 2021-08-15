from tkinter import *
import sqlite3
from tkinter import messagebox

root = Tk()
root.title("ToDo List")
root.geometry("470x500")

photo = PhotoImage(file = "noteIcon.png")
root.iconphoto(False, photo)

conn = sqlite3.connect("toDo.db")

c = conn.cursor()

#Create table
c.execute("""
    CREATE TABLE if not exists toDo(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
        description TEXT NOT NULL,
        completed BOOLEAN NOT NULL
    );
""")

conn.commit()

def remove(id):
    def _remove():
        c.execute("DELETE FROM toDo WHERE id = ?", (id, ))
        conn.commit()
        render_toDos()
    return _remove

#Currying
def complete(id):
    def _complete():
        toDo = c.execute("SELECT * from toDo WHERE id = ?", (id, )).fetchone()
        c.execute("UPDATE toDo SET completed = ? WHERE id = ?", (not toDo[3], id))
        conn.commit()
        render_toDos()
    return _complete

def deleteAll():
    respuesta = messagebox.askokcancel("Delete all task", "Are you sure you want to delete all tasks?") #Devuelve boolean    
    if respuesta == True:
        c.execute("DELETE FROM toDo")
        conn.commit()
        render_toDos()              
    else:
        pass

def render_toDos():
    rows = c.execute("SELECT * FROM toDo").fetchall()    

    for widget in frame.winfo_children():
        widget.destroy()

    for i in range(0, len(rows)):
        id = rows[i][0]
        completed = rows[i][3]
        description = rows[i][2]
        color = "#c7c7c7" if completed else "black"
        l = Checkbutton(frame, text=description, fg=color, width=42, anchor="w", command=complete(id))
        l.grid(row=i, column=0, sticky="w")
        btnDel = Button(frame, text = "Delete", fg="white", bg="#d13d3d", command=remove(id))
        btnDel.grid(row=i, column=1)
        l.select() if completed else l.deselect()
        
def addToDo():
    toDo = e.get()
    if toDo:
        c.execute("""
            INSERT INTO toDo (description, completed) VALUES (?, ?)
             """, (toDo, False))
        conn.commit()
        e.delete(0, END)
        render_toDos()
    else:
        pass   

l = Label(root, text="New task")
l.grid(row=0, column=0)

e = Entry(root, width=40)
e.grid(row=0, column=1)

btn = Button(root, text="Add", fg="#fff", bg="#008dff", command=addToDo)
btn.grid(row=0, column=2)

btndestroy = Button(root, text="DELETE ALL", fg="#fff", bg="red", command=deleteAll)
btndestroy.grid(row=0, column=3)

frame = LabelFrame(root, text="My tasks", padx=5, pady=5)
frame.grid(row=1, column=0, columnspan=3, sticky="nswe", padx=5)

e.focus()
root.bind("<Return>", lambda x:addToDo())

render_toDos()

root.mainloop()