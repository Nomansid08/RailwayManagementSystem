import time
import datetime as dt
import pyodbc
from tkinter import *
from tkinter.ttk import Combobox
from PIL import Image, ImageTk
from functools import partial
from random import randint

logged = False
global rowss

def pnr(n):

    Label(r4, text="You have successfully booked ticket", font=("Helvetica", 16)).place(x=900, y=300)
    l = []
    r = randint(1000000, 9999999)
    while (r in l):
        r = randint(1000000, 9999999)
    l.append(r)
    connection = pyodbc.connect( r'Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=C:\Users\Asus\Documents\TrainUserDEtails.accdb;')
    cursor = connection.cursor()
    cursor.execute("""SELECT * from `Train_details` WHERE From=? AND To=? AND `Journey Date`=? AND Availability>0""",(entry1.get(), entry2.get(), entry_d.get()))

    record = cursor.fetchall()
    c = 0
    y=0
    for row in record:
        c = c+1
        if(c == n):
            y = row[6]
    y = y-1
    cursor.execute("UPDATE `Train_details` SET `Availability`=? WHERE `ID`=?", y, n)
    cursor.execute("INSERT INTO Trains ([Full name], [Age], [Gender], [Address], [Aadhar], [Pnr no])  VALUES(?,?,?,?,?,?)",
                (e1.get(), e4.get(), e3.get(), e2.get(), e5.get(), l[len(l)-1]))
    cursor.close()
    connection.commit()
    Label(r4, text="Your PNR no. is {0}".format(l[len(l) - 1]), fg="red", font=("Helvetica", 16)).place(x=900, y=350)


def pay(n):
    Label(r4, text="Please Pay to continue", font=("Helvetica", 16)).place(x=900, y=100)
    Button(r4, text="Pay Now", command=partial(pnr,n)).place(x=900, y=200)

def passenger(n):
    global r4
    if (logged == False):
        login()
    r4 = Toplevel(r3)
    r4.geometry("2000x1000")
    Label(r4, text="Passenger Details",font=("Helvetica",16)).place(x=100, y=100)
    Label(r4, text="Name").place(x=200, y=200)
    global e1
    e1 = Entry(r4)
    e1.place(x=300, y=200, height=30, width=300)
    Label(r4, text="Address").place(x=200, y=300)
    global e2
    e2 = Entry(r4)
    e2.place(x=300, y=300, height=30, width=300)
    Label(r4, text="Gender").place(x=200, y=400)
    global e3
    e3 = Entry(r4)
    e3.place(x=300, y=400, height=30, width=300)
    Label(r4, text="Age").place(x=200, y=500)
    global e4
    e4 = Entry(r4)
    e4.place(x=300, y=500, height=30, width=300)
    Label(r4, text="Aadhar no").place(x=200, y=600)
    global e5
    e5 = Entry(r4)
    e5.place(x=300, y=600, height=30, width=300)
    Button(r4, text="Submit", activebackground="blue", activeforeground="white", background="blue", height=2, width=30, command= partial(pay,n)).place(x=300, y=700)







def onFrameConfigure(canvas):
    canvas.configure(scrollregion=canvas.bbox("all"))


def insert():
    connection = pyodbc.connect(r'Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=C:\Users\Asus\Documents\TrainUserDEtails.accdb;')
    cur = connection.cursor()

    cur.execute("SELECT * from login WHERE Username = ?",(username.get()))
    if(cur.fetchone() is not None):
        Label(r2, text="Username already exists", fg="red").place(x=200, y=80)
        username.delete(0, "end")
        username.insert(0, "Username*")
        username.config(fg="grey")
    else:
        cur.execute("INSERT into login ([Username],[Password]) VALUES(?,?)", (username.get(), password.get()))
        cur.execute("INSERT INTO sign_up ([Full name], [Address], [Phone No], [Username], [Password])  VALUES(?,?,?,?,?)",(name.get(), address.get(), phno.get(), username.get(), password.get()))
        Label(r2, text="You have been successfully registered", font=("Helvetica", 16), fg="yellow").place(x=200, y=350)
        Button(r2, text="Login Here", height=2, width=20 , command=login).place(x=200, y=400)
        Button(r2, text="Home", height=2, width=20 , command=r2.destroy).place(x=400, y=400)
    cur.close()
    connection.commit()


def click_login():
    connection = pyodbc.connect(r'Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=C:\Users\Asus\Documents\TrainUserDEtails.accdb;')
    cur = connection.cursor()
    cur.execute("""SELECT * from `login` WHERE `Username` = ? AND `Password` = ?""", (username.get(), password.get()))
    if cur.fetchone() is not None:
        Label(root, text="Welcome %s"%(username.get()), font=("Helvetica", 16)).place(x=400, y=30)
        r1.destroy()
        logged = True
    else:
        Label(r1, text="Invalid Username or Password", fg="red").place(x=200, y=80)
        username.delete(0, "end")
        password.delete(0, "end")
        username.insert(0, "Username*")
        username.config(fg="grey")
        password.insert(0, "password*")
        password.config(fg="grey")
    cur.close()
    connection.commit()



def bookNow(n):
    rowss = n
    c = 0
    connection = pyodbc.connect(r'Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=C:\Users\Asus\Documents\TrainUserDEtails.accdb;')
    cur = connection.cursor()
    cur.execute("""SELECT * from `Train_details` WHERE From=? AND To=? AND `Journey Date`=? """, (entry1.get(), entry2.get(), entry_d.get()))
    record = cur.fetchall()

    for row in record:
        c = c+1
        if(c == n):
            ry = 200*c
            Label(frame, text="Fare:{}".format(row[2]), font=("Helvetica", 12)).place(x=880, y=ry+50)
            Label(frame, text="Availability:{}".format(row[6]), font=("Helvetica", 12)).place(x=880, y=ry+80)
            Button(frame, text="Book Now", height=1, width=20, fg="black", command=partial(passenger, n)).place(x=880, y=ry+120)








def clickFin_tr():
    global r3
    r3 = Toplevel(root)
    r3.geometry("1200x700")
    r3.title("Found Trains")
    global canvas
    global frame
    canvas = Canvas(r3, borderwidth=0, background="#ffffff")
    frame = Frame(canvas, background="#ffffff", height=4056, width=1200)
    vsb = Scrollbar(r3, orient="vertical", command=canvas.yview)
    canvas.configure(yscrollcommand=vsb.set)

    vsb.pack(side="right", fill="y")
    canvas.pack(side="left", fill="both", expand=True)
    canvas.create_window((0, 0), window=frame, anchor="nw")

    frame.bind("<Configure>", onFrameConfigure(canvas))
    Label(frame, text="Train Name & no.", font=("Helvetica", 12)).place(x=300, y=100)
    Label(frame, text="Departs", font=("Helvetica", 12)).place(x=500, y=100)
    Label(frame, text="Arrives", font=("Helvetica", 12)).place(x=620, y=100)
    Label(frame, text="Class", font=("Helvetica", 12)).place(x=720, y=100)
    Label(frame, text="Availability and Fare", font=("Helvetica", 12)).place(x=880, y=100)
    fin_tr()


def fin_tr():
    rx = 300
    ry = 200
    global i
    i = 1
    connection = pyodbc.connect(r'Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=C:\Users\Asus\Documents\TrainUserDEtails.accdb;')
    cur = connection.cursor()
    cur.execute("""SELECT * from `Train_details`
                       WHERE From=? AND To=? AND `Journey Date`=? AND Availability>0""" ,(entry1.get(), entry2.get(), entry_d.get()))
    record = cur.fetchall()
    no_trains = len(record)

    if record is not None:
        Label(frame, text="{} trains found".format(no_trains), fg="blue").place(x=300, y=160)
        for row in record:

            Label(frame, text="{}".format(row[1]), fg="#335AFF").place(x=rx, y=ry)
            Label(frame, text="{0} -> {1}".format(entry1.get(), entry2.get())).place(x=rx, y=ry+20)
            Label(frame, text="{}".format(row[5])).place(x=rx+200, y=ry)
            Label(frame, text="{}".format(row[9])).place(x=rx+320, y=ry)
            Label(frame, text="{}".format(row[3])).place(x=rx+420, y=ry)
            '''cla = Combobox(frame)
            cla["values"] = ["Sleeper Class(SL)", "AC First Class(1A)", "AC 2 Tier(2A)", "AC 3 Tier(3A)"]
            if(classes.get() != "All Classes"):
                if(classes.get() == "AC First Class(1A)"):
                    cla.current(1)
                if(classes.get() == "AC 2 Tier(2A)"):
                    cla.current(2)
                if (classes.get() == "AC 3 Tier(3A)"):
                    cla.current(3)
            else:
                cla.current(0)
            cla.place(x=rx+420, y=ry)'''
            Button(frame, text="Check Availability and Fare", activebackground="#335AFF", background="#335AFF", width=30, height=2, command=partial(bookNow, i)).place(x=rx+580, y=ry)
            ry = ry+200
            i = i+1
    else:
        Label(r3, text="No trains Found.", fg="red").place(x=200, y=80)
    cur.close()
    connection.commit()


def login():
    global r1
    r1 = Toplevel(root)
    r1.title("Login")
    r1.geometry("700x400")
    Label(r1, text="Login", font=("Helvetica", 16)).place(x=250, y=30)

    global username                                                       # login username
    username = Entry(r1)
    username.insert(0, "Username*")
    username.bind("<FocusIn>", username_click)
    username.bind("<FocusOut>", username_out)
    username.config(fg="grey")
    username.place(x=200, y=100, height=30, width=300)

    global password                                                        # login password
    password = Entry(r1)
    password.insert(0, "Password*")
    password.bind("<FocusIn>", password_click)
    password.bind("<FocusOut>", password_out)
    password.config(fg="grey")
    password.place(x=200, y=150, height=30, width=300)

    Button(r1, text="LOG IN", activebackground="blue", activeforeground="white", bg="blue", fg="white", command=click_login).place(x=200, y=200, width=300, height=30)
    Label(r1, text="Don't have an account").place(x=200, y=300)
    Button(r1, text="Register", activebackground="blue", activeforeground="white", bg="blue", fg="white", command=register).place(x=200, y=330, width=300, height=30)

def register():
    global r2
    r2 = Toplevel(root)
    r2.title("REGISTER")
    r2.geometry("700x700")
    Label(r2, text="Register", font=("Helvetica",16)).place(x=250, y=30)

    global name                                                       # name of user
    name = Entry(r2)
    name.insert(0, "Name")
    name.bind("<FocusIn>", name_click)
    name.bind("<FocusOut>", name_out)
    name.config(fg="grey")
    name.place(x=200, y=100, height=30, width=300)

    global address                                                          # login password
    address = Entry(r2)
    address.insert(0, "Address*")
    address.bind("<FocusIn>", address_click)
    address.bind("<FocusOut>", address_out)
    address.config(fg="grey")
    address.place(x=200, y=150, height=30, width=300)

    global phno                                                                 # phone number of user
    phno = Entry(r2)
    phno.insert(0, "Phone no.")
    phno.bind("<FocusIn>", phno_click)
    phno.bind("<FocusOut>", phno_out)
    phno.config(fg="grey")
    phno.place(x=200, y=200, height=30, width=300)

    global username
    username = Entry(r2)
    username.insert(0, "Username*")
    username.bind("<FocusIn>", username_click)
    username.bind("<FocusOut>", username_out)
    username.config(fg="grey")
    username.place(x=200, y=250, height=30, width=300)

    global password
    password = Entry(r2)
    password.insert(0, "Password*")
    password.bind("<FocusIn>", password_click)
    password.bind("<FocusOut>", password_out)
    password.config(fg="grey")
    password.place(x=200, y=300, height=30, width=300)

    Button(r2, text="Register", activebackground="blue", activeforeground="white", bg="blue", fg="white", command=insert).place(x=200, y=350, width=300, height=30)


def address_click(event):
    if address.cget("fg") == "grey":
        address.delete(0, "end")
        address.insert(0, "")
        address.config(fg="black")


def phno_click(event):
    if phno.cget("fg") == "grey":
        phno.delete(0, "end")
        phno.insert(0, "")
        phno.config(fg="black")


def username_click(event):
    if username.cget("fg") == "grey":
        username.delete(0, "end")
        username.insert(0, "")
        username.config(fg="black")


def password_click(event):
    if password.cget("fg") == "grey":
        password.delete(0, "end")
        password.insert(0, "")
        password.config(fg="black")


def name_click(event):
    if name.cget("fg") == "grey":
        name.delete(0, "end")
        name.insert(0, "")
        name.config(fg="black")


def from_click(event):
    if entry1.cget("fg") == "grey":
        entry1.delete(0, "end")
        entry1.insert(0, "")
        entry1.config(fg="black")


def to_click(event):
    if entry2.cget("fg") == "grey":
        entry2.delete(0, "end")
        entry2.insert(0, "")
        entry2.config(fg="black")


def entryd_click(event):
    if entry_d.cget("fg") == "grey":
        entry_d.delete(0, "end")
        entry_d.insert(0, "")
        entry_d.config(fg="black")

# username


def username_out(event):
    if username.get() == "":
        username.insert(0, "Username*")
        username.config(fg="grey")


# password


def password_out(event):
    if password.get() == "":
        password.insert(0, "Password*")
        password.config(fg="grey")


# name

def name_out(event):
    if name.get() == "":
        name.insert(0, "Name*")
        name.config(fg="grey")

# address


def address_out(event):
    if address.get() == "":
        address.insert(0, "Address*")
        address.config(fg="grey")

# phno


def phno_out(event):
    if phno.get() == "":
        phno.insert(0, "Phone no.*")
        phno.config(fg="grey")


# from


def entry1_out(event):
    if entry1.get() == "":
        entry1.insert(0, "From*")
        entry1.config(fg="grey")


# to

def entry2_out(event):
    if entry2.get() == "":
        entry2.insert(0, "To*")
        entry2.config(fg="grey")

# datee


def entry_d_out(event):
    if entry_d.get() == "":
        entry_d.insert(0, "DD-MM-YY*")
        entry_d.config(fg="grey")


def update_timeText():

    current = time.strftime("[%H:%M:%S]")
    timeText.configure(text=current)
    # Call the update_timeText() function after 1 second
    root.after(1000, update_timeText)


global root
root = Tk()
root.title("RAILWAY RESERVATION PORTAL")
root.geometry("1024x700")

c = Canvas(root, width=1024, height=700).place(x=0, y=0)
f1 = Frame(root, width=1024, height=200).place(x=0, y=0)

timeText = Label(root, fg="green")
timeText.place(x=510, y=40)

update_timeText()

Label(root, text=f"{dt.datetime.now():%d-%b-%Y    %a}", fg="green").place(x=400, y=40)

logo_img = ImageTk.PhotoImage(Image.open("logo_train.jpg"))
lbl_logo = Label(root, image=logo_img).place(x=0, y=0)

log = Button(root, text="Login", height=2, width=20, fg="red", command=login).place(y=60, x=400)

reg = Button(root, text="Register", height=2, width=20, command=register).place(y=60, x=600)

train_img = ImageTk.PhotoImage(Image.open("train2.jpg"))
lbl_train = Label(root, image=train_img).place(x=0, y=100)

f2 = Frame(root, width=400, height=500).place(x=100, y=110)
# Book Your Ticket
lab = Label(root, text="Book Your Ticket", font=("Helvetica", 16)).place(x=250, y=110)

icon_img = ImageTk.PhotoImage(Image.open("rail_icon.png"))
Label(root, image=icon_img).place(x=320, y=150)

# Source entry
global entry1
entry1 = Entry(root)
entry1.insert(0, "From*")
entry1.bind("<FocusIn>", from_click)
entry1.bind("<FocusOut>", entry1_out)
entry1.config(fg="grey")
entry1.place(x=150, y=250, height=30, width=300)

# Destination entry
global entry2
entry2 = Entry(root)
entry2.insert(0, "To*")
entry2.bind("<FocusIn>", to_click)
entry2.bind("<FocusOut>", entry2_out)
entry2.config(fg="grey")
entry2.place(x=150, y=300, height=30, width=300)

# Date entry
global entry_d
entry_d = Entry(root)
entry_d.insert(0, "DD-MM-YY")
entry_d.bind("<FocusIn>", entryd_click)
entry_d.bind("<FocusOut>", entry_d_out)
entry_d.config(fg="grey")
entry_d.place(x=150, y=350, height=30, width=300)

# Classes entry
classes = Combobox(root)
classes["values"] = ("All Classes", "AC First Class(1A)", "AC 2 Tier(2A)", "AC 3 Tier(3A)", "Sleeper Class(SL)")
classes.current(0)
classes.place(x=150, y=410, height=30, width=300)

# find trains
find_ = Button(text="Find trains", activebackground="blue", activeforeground="white", fg="white", bg="blue", command=clickFin_tr).place( x=150, y=460, height=30, width=300)

root.mainloop()
