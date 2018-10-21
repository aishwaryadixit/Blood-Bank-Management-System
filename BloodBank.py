#MySQL Data base import
import MySQLdb
from Tkinter import *
from PIL import Image

db=MySQLdb.connect("localhost","root","@idx","bbms")
cursor=db.cursor()
root = Tk()
#insert image
image1=PhotoImage(file="/home/aishwarya/Downloads/bg.gif")
panel=Label(root,image=image1,bg="black").place(x=0,y=0,relwidth=1,relheight=1)
root.title("BLOOD BANK")
#dimension
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
# Function for donar entry
def insertDonor(name,age,gender,address,contactno):
	insert = "INSERT INTO donors(name,age,gender,address,contactno) VALUES('"+name+"','"+age+"','"+gender+"','"+address+"',"+"'"+contactno+"')"
	try:
		cursor.execute(insert)
		db.commit()
	except:
		db.rollback()

# function for insert blood
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
		print len(rows)
		return rows
	except:
		db.rollback() 

def sel():
   selection = "You selected the option " + v.get()
   print selection
  

def donordetails():
	#global v
	root=Toplevel()
	root.title("BLOOD BANK")
	root.geometry("1024x768")
	root.configure(background ='#FF8F8F')
	l1=Label(root,text="Name:",bg='white',font="Helvetica 12").place(x=40,y=40)
	l2=Label(root,text="Age:",bg='white',font="Helvetica 12").place(x=40,y=80)
	l3=Label(root,text="Gender:",bg='white',font="Helvetica 12").place(x=40,y=120)
	l4=Label(root,text="Address:",bg='white',font="Helvetica 12").place(x=40,y=220)
	l5=Label(root,text="Contact:",bg='white',font="Helvetica 12").place(x=40,y=260)
	e1=Entry(root)
	e1.place(x=120,y=40)
	e2=Entry(root)
	e2.place(x=120,y=80)
	r1=Radiobutton(root,text="Male",variable=v,value="Male",command=sel).place(x=120,y=120)
	r2=Radiobutton(root,text="Female",variable=v,value="Female",command=sel).place(x=120,y=150)
	r3=Radiobutton(root,text="Other",variable=v,value="Other",command=sel).place(x=120,y=180)
	#e3=Entry(root)
	#e3.place(x=100,y=120)
	e4=Entry(root)
	e4.place(x=120,y=220)
	e5=Entry(root)
	e5.place(x=120,y=260)
	
	#b2=Button(root,text="Back",command=lambda : stop(root)).place(x=120,y=300)
	
	#b1=Button(root,text="Submit",command=lambda : insertDonor(e1.get(),e2.get(),gen,e4.get(),e5.get())).place(x=40,y=300)

	root.mainloop()

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
	b2=Button(root,text="Back",command=lambda : stop(root)).place(x=200,y=160)
	b1=Button(root,text="Submit",command=lambda : insertBlood(e1.get(),e2.get(),e3.get())).place(x=40,y=160)
	
	#img = PhotoImage(file="/home/aishwarya/Downloads/b1.gif")	
	#panel = Label(root, image = img,bg="#F6B88D").place(x=200,y=200,w=400,h=400)
		
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


root.mainloop()
