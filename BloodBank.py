import mysql.connector as mysql
from tkinter import *
from tkinter import messagebox
import json
import os

if not os.path.exists("config_db.json"):
	f = open("config_db.json", "w")

file1 = open("config_db.json","r") 
db_conf=file1.read()
file1.close()
dbdt=['','','']
if db_conf=="":
	print("Let's configure your database first:")
	dbdt[0]=input("Enter host/server ip: ")
	dbdt[1]=input("Database username: ")
	dbdt[2]=input("Database password: ")
	saveit=json.dumps(dbdt)
	db= mysql.connect(
  		host=dbdt[0],
  		user=dbdt[1],
  		password=dbdt[2],
			)
	cursor=db.cursor()
	qdb='''CREATE DATABASE IF NOT EXISTS `blood_donation_db`;
		'''
	cursor.execute(qdb)
	db= mysql.connect(
 	 host=dbdt[0],
 	 user=dbdt[1],
  	 password=dbdt[2],
  	 database="blood_donation_db"
	)
	cursor=db.cursor()
	qdb='''CREATE TABLE IF NOT EXISTS `blood` (
  `bloodgroup` varchar(50) DEFAULT NULL,
  `platelet` varchar(50) DEFAULT NULL,
  `rbc` varchar(50) DEFAULT NULL,
  `date` datetime DEFAULT NULL,
  `id` int(10) NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
		'''
	cursor.execute(qdb)
	qdb='''CREATE TABLE IF NOT EXISTS `donors` (
  `name` varchar(50) DEFAULT NULL,
  `age` varchar(50) DEFAULT NULL,
  `gender` varchar(50) DEFAULT NULL,
  `address` varchar(50) DEFAULT NULL,
  `contactno` varchar(50) DEFAULT NULL,
  `id` int(10) NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

		'''
	cursor.execute(qdb)
	file1 = open("config_db.json","w+")
	file1.write(saveit)
	file1.close()
else:
	dbdt=json.loads(db_conf)
db= mysql.connect(
  host=dbdt[0],
  user=dbdt[1],
  password=dbdt[2],
  database="blood_donation_db"
)
cursor=db.cursor()
def mainfn():
	root = Tk()

	root.title("BLOOD BANK")
	root.geometry("1920x1080")
	root.configure(background='white')
	l3=Label(root,text="BLOOD BANK SYSTEM",bg='white',font = "Helvetica 15 bold").place(x=450,y=40,w=300,h=40)
	l1=Label(root,text="Click to enter the details of the donor",bg='white',font="Helvetica 12").place(x=80,y=100,w=300,h=40)
	b1=Button(root,text="Donor Details",command=lambda : donordetails()).place(x=80,y=150)
	l2=Label(root,text="Click to enter the details of the blood",bg='white',font="Helvetica 12").place(x=80,y=200,w=300,h=40)
	b2=Button(root,text="Blood Details",command=lambda : blooddetails()).place(x=80,y=250)	
	l3=Label(root,text="Click to make a request for blood",bg='white',font="Helvetica 12").place(x=80,y=300,w=300,h=40)
	b3=Button(root,text="Blood Request",command=lambda : requestblood()).place(x=80,y=350)
	b2=Button(root,text="Exit",command=lambda : stop(root)).place(x=80,y=400)	
	v = StringVar()

def insertDonor(name,age,gender,address,contactno):
	insert = "INSERT INTO donors(name,age,gender,address,contactno) VALUES('"+name+"','"+age+"','"+gender+"','"+address+"',"+"'"+contactno+"')"
	try:
		cursor.execute(insert)
		db.commit()
	except:
		db.rollback()

	blooddetails()


def insertBlood(bloodgroup,platelet,rbc):
	insert= "INSERT INTO blood(bloodgroup,platelet,rbc,date) VALUES('"+bloodgroup+"',"+"'"+platelet+"',"+"'"+rbc+"',"+"CURDATE())"
		
	try:
		cursor.execute(insert)
		db.commit()
	except:
		db.rollback()
		
def retrieve(bg):
	request="select * from donors inner join blood using(id) where bloodgroup='"+bg+"'"
	
	try:
		cursor.execute(request)		
		rows=cursor.fetchall()		
		db.commit()
		print (len(rows))
		return rows
	except:
		db.rollback() 


def donordetails():
	global v
	v=""
	root=Tk()
	root.title("BLOOD BANK")
	root.geometry("1024x768")
	root.configure(background ='#FF8F8F')
	l1=Label(root,text="Name:",bg='white',font="Helvetica 12").place(x=40,y=40)
	l2=Label(root,text="Age:",bg='white',font="Helvetica 12").place(x=40,y=80)
	l3=Label(root,text="Gender:",bg='white',font="Helvetica 12").place(x=40,y=120)
	l4=Label(root,text="Address:",bg='white',font="Helvetica 12").place(x=40,y=160)
	l5=Label(root,text="Contact:",bg='white',font="Helvetica 12").place(x=40,y=200)
	e1=Entry(root)
	e1.place(x=120,y=40)
	e2=Entry(root)
	e2.place(x=120,y=80)
	e3=Entry(root)
	e3.place(x=120,y=120)
	e4=Entry(root)
	e4.place(x=120,y=160)
	e5=Entry(root)
	e5.place(x=120,y=200)
	
	b2=Button(root,text="Back",command=lambda : stop(root)).place(x=120,y=300)
	
	b1=Button(root,text="Submit",command=lambda : insertDonor(e1.get(),e2.get(),e3.get(),e4.get(),e5.get())).place(x=40,y=300)

	root.mainloop()

def newbloodin(a,b,c):
	insertBlood(a,b,c)
	messagebox.showinfo("Info", "Added Successfully")
	
def blooddetails():
	root=Tk()
	root.title("BLOOD BANK")
	root.geometry("1024x768")
	root.configure(background ='#FF8F8F')
	l1=Label(root,text="Blood Group:",font="Helvetica 12").place(x=40,y=40,w=250,h=20)
	l2=Label(root,text="PLatetelet count (in 100 thousands):",font="Helvetica 12").place(x=40,y=80,w=250,h=20)
	l3=Label(root,text="RBC count (in millions):",font="Helvetica 12").place(x=40,y=120,w=250,h=20)
	#l4=Label(root,text="Date Of Entry count:").place(x=40,y=160)
	e1=Entry(root)
	e1.place(x=350,y=40)
	e2=Entry(root)
	e2.place(x=350,y=80)
	e3=Entry(root)
	e3.place(x=350,y=120)
	b1=Button(root,text="Submit",command=lambda : newbloodin(e1.get(),e2.get(),e3.get())).place(x=40,y=160)
		
	root.mainloop()	
	
	
def grid1(bg):
	root=Tk()
	root.title("LIST OF MATCHING DONORS")
	root.geometry("750x500")
	root.configure(background='#0C43F0')
	rows=retrieve(bg)
	x=0
	for row in rows:
		l1=Label(root,text=row[0],bg="#1EDEF2",font = "Verdana 15 bold").grid(row=x,column=0,sticky='E',padx=5,pady=5,ipadx=5,ipady=5)
		l2=Label(root,text=row[1],bg="#1EDEF2",font = "Verdana 15 bold").grid(row=x,column=1,sticky='E',padx=5,pady=5,ipadx=5,ipady=5)
		l3=Label(root,text=row[2],bg="#1EDEF2",font = "Verdana 15 bold").grid(row=x,column=2,sticky='E',padx=5,pady=5,ipadx=5,ipady=5)
		l4=Label(root,text=row[3],bg="#1EDEF2",font = "Verdana 15 bold").grid(row=x,column=3,sticky='E',padx=5,pady=5,ipadx=5,ipady=5)
		l5=Label(root,text=row[4],bg="#1EDEF2",font = "Verdana 15 bold").grid(row=x,column=4,sticky='E',padx=5,pady=5,ipadx=5,ipady=5)
		l6=Label(root,text=row[5],bg="#1EDEF2",font = "Verdana 15 bold").grid(row=x,column=5,sticky='E',padx=5,pady=5,ipadx=5,ipady=5)
		l7=Label(root,text=row[6],bg="#1EDEF2",font = "Verdana 15 bold").grid(row=x,column=6,sticky='E',padx=5,pady=5,ipadx=5,ipady=5)
		l8=Label(root,text=row[7],bg="#1EDEF2",font = "Verdana 15 bold").grid(row=x,column=7,sticky='E',padx=5,pady=5,ipadx=5,ipady=5)
		l9=Label(root,text=row[8],bg="#1EDEF2",font = "Verdana 15 bold").grid(row=x,column=8,sticky='E',padx=5,pady=5,ipadx=5,ipady=5)
		l10=Label(root,text=row[9],bg="#1EDEF2",font = "Verdana 15 bold").grid(row=x,column=9,sticky='E',padx=5,pady=5,ipadx=5,ipady=5)
		x=x+1
	root.mainloop()

def requestblood():
	root=Tk()
	root.title("BLOOD BANK")
	root.geometry("1024x720")
	root.configure(background='#FF8F8F')
	l=Label(root,text="Enter the blood group").place(x=50,y=50,w=400,h=40)
	e=Entry(root)
	e.place(x=500,y=50)
	b2=Button(root,text="Back",command=lambda : stop(root)).place(x=600,y=100)
	b=Button(root,text="ENTER",command=lambda : grid1(e.get())).place(x=500,y=100)
	root.mainloop()

def stop(root):
	root.destroy()

def login():
    #getting form data
    uname=username.get()
    pwd=password.get()
    #applying empty validation
    if uname=='' or pwd=='':
        message.set("fill the empty field!!!")
    else:
      if uname=="admin" and pwd=="abc123":
       loggedin="1"
       message.set("Login success")
       mainfn()
       login_screen.destroy()
      else:
       message.set("Wrong username or password!!!")
#defining loginform function
def Loginform():
    global login_screen
    login_screen = Tk()
    #Setting title of screen
    login_screen.title("Login Form")
    #setting height and width of screen
    login_screen.geometry("300x250")
    #declaring variable
    global loggedin
    global message
    global username
    global password
    username = StringVar()
    password = StringVar()
    message=StringVar()
    #Creating layout of login form
    Label(login_screen,width="300", text="Please enter details below", bg="orange",fg="white").pack()
    #Username Label
    Label(login_screen, text="Username * ").place(x=20,y=40)
    #Username textbox
    Entry(login_screen, textvariable=username).place(x=90,y=42)
    #Password Label
    Label(login_screen, text="Password * ").place(x=20,y=80)
    #Password textbox
    Entry(login_screen, textvariable=password ,show="*").place(x=90,y=82)
    #Label for displaying login status[success/failed]
    Label(login_screen, text="",textvariable=message).place(x=95,y=100)
    #Login button
    Button(login_screen, text="Login", width=10, height=1, bg="orange",command=login).place(x=105,y=130)
    login_screen.mainloop()
#calling function Loginform

Loginform()
