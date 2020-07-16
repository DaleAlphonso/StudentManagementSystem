from tkinter import *
from tkinter import messagebox
from tkinter import scrolledtext
import re
import cx_Oracle
import matplotlib.pyplot as plt
import numpy as ny
import socket
import bs4
import requests
con=None
try:
	con=cx_Oracle.connect("system/abc123")
	print("connected")
	print(con.version)
	
except cx_Oracle.DatabaseError as e:
	print("issue",e)
finally:
	if con is None:
		con.close()
		print("disconnected")

class InvalidRollNumException(Exception):
	def __intit__(self,msg):
		self.msg=msg
	
#ADD_BUTTON
def f1():
	root.withdraw()
	adst.deiconify()

#VIEW_BUTTON
def f2():
	vwst.deiconify()
	root.withdraw()
	con=None
	cursor = None
	try:
			con=cx_Oracle.connect("system/abc123")
			cursor=con.cursor()
			sql="select ROLLNO,NAME,MARKS from studentdata"
			cursor.execute(sql)
			data=cursor.fetchall()
			msg=""
			for d in data:
				msg=msg+" r : "+str(d[0])+"| n : "+str(d[1])+"| m : "+str(d[2])+"\n"
			stViewData.insert(INSERT,msg)
					
	except cx_Oracle.DatabaseError as e:
			messagebox.showerror("Error ",e)
			con.rollback()
	finally:
			if cursor is not None:
				cursor.close()
			if con is not None:
				con.close()
				
#UPDATE_BUTTON
def f3():
	upst.deiconify()
	root.withdraw()
	
#DELETE_BUTTON
def f4():
	dtst.deiconify()
	root.withdraw()
#Creating method for putting data into database
def f5():
	con=None
	try:
			con=cx_Oracle.connect("system/abc123")
			rno=entAddrno.get()
			tr_rno = rno.strip()
			name=entAddname.get()
			#tr_name = rno.strip()
			marks=entAddmarks.get()
			tr_marks = marks.strip()
			rnopattern = re.match('^[0-9]+$',tr_rno)
			name_pattern = re.match('^[A-Z a-z]+$',name)
			markspattern = re.match('^[0-9]+$',tr_marks)

			if len(rno) == 0:
				messagebox.showwarning("No Input","Please Enter the Roll Number")

			elif len(name) == 0:
				messagebox.showwarning("No Input","Please Enter the name")

			elif len(marks) == 0:
				messagebox.showwarning("No Input","Please Enter the marks")


			elif (tr_rno.isalpha() or not rnopattern or int(tr_rno) < 1 ):
				messagebox.showerror("Bad Input","Invalid roll number")
				entAddrno.delete(0,END)
				entAddrno.focus()
			elif ((len(name) < 2) or not name_pattern ):
				messagebox.showerror("Bad Input","Invalid Name")
				entAddname.delete(0,END)
				entAddname.focus()
			elif(tr_marks.isalpha() or not markspattern or int(tr_marks) < 0 or int(tr_marks) >100 ):
				messagebox.showerror("Invalid Marks","Invalid marks entered |Note* range(0-100)")
				entAddmarks.delete(0,END)
				entAddmarks.focus()
			else:
				r = int(tr_rno)
				n = name.strip()
				m = int(tr_marks)
				args=(r,n,m)
				cursor=con.cursor()
				
				sql="insert into studentdata values('%d','%s','%d')"
				cursor.execute(sql % args)
				
				con.commit()
				messagebox.showinfo("Data Added Succesfully",str(cursor.rowcount)+" rows inserted")
				entAddrno.delete(0,END)
				entAddrno.focus()
				entAddname.delete(0,END)
				entAddname.focus()
				entAddmarks.delete(0,END)
				entAddmarks.focus()
	
	except cx_Oracle.DatabaseError :
			#error = "ORA-00001: unique constraint (SYSTEM.SYS_C008017) violated"
			messagebox.showerror("Error ","Student already exists")
			entAddrno.delete(0,END)
			entAddname.delete(0,END)
			entAddmarks.delete(0,END)

			con.rollback()
	
	finally:
			if con is not None:
				con.close()
			
						
	
def f6():
	root.deiconify()
	adst.withdraw()
	rno=entAddrno.get()
	name=entAddname.get()
	marks=entAddmarks.get()
	entAddrno.delete(0,END)
	entAddrno.focus()
	entAddname.delete(0,END)
	entAddname.focus()
	entAddmarks.delete(0,END)
	entAddmarks.focus()
	
def f7():
	root.deiconify()
	vwst.withdraw()
	con=None
	try:
			con=cx_Oracle.connect("system/abc123")
	except cx_Oracle.DatabaseError as e:
		messagebox.showerror("Error ",e)
		con.rollback()
	
	finally:
		if con is not None:
			con.close()
			stViewData.delete("1.0",END)
	
	
def f8():

	con=None
	try:
			con=cx_Oracle.connect("system/abc123")
			rno=entUprno.get()
			tr_rno = rno.strip()
			name=entUpname.get()
			marks=entUpmarks.get()
			tr_marks = marks.strip()
			rnopattern = re.match('^[0-9]+$',tr_rno)
			name_pattern = re.match('^[A-Z a-z]+$',name)
			markspattern = re.match('^[0-9]+$',tr_marks)
			if len(rno) == 0:
				messagebox.showwarning("No Input","Please Enter the Roll Number")

			elif len(name) == 0:
				messagebox.showwarning("No Input","Please Enter the name")

			elif len(marks) == 0:
				messagebox.showwarning("No Input","Please Enter the marks")
			elif (tr_rno.isalpha() or not rnopattern or int(tr_rno) < 1 ):
				messagebox.showerror("Bad Input","Invalid roll number")
				entUprno.delete(0,END)
				entUprno.focus()

			elif ((len(name) < 2) or not name_pattern ):
				messagebox.showerror("Bad Input","Invalid Name")
				entUpname.delete(0,END)
				entUpname.focus()
			elif (tr_marks.isalpha() or not markspattern or int(tr_marks) < 0 or int(tr_marks) >100 ):
				messagebox.showerror("Invalid Marks","Invalid marks entered | Note* range(0-100)")
				entUpmarks.delete(0,END)
				entUpmarks.focus()
			else:
				r = int(tr_rno)
				n = name.strip()
				m = int(tr_marks)
				args=(n,m,r)
				cursor=con.cursor()
				sql="update studentdata set NAME='%s',MARKS='%d' where ROLLNO='%d'"
				cursor.execute(sql % args)
				con.commit()
				if cursor.rowcount == 0:
					messagebox.showerror("Invalid Rno","Roll Number does not exists")
					entUprno.delete(0,END)
				else:
					messagebox.showinfo("Data Updated Succesfully",str(cursor.rowcount)+" row updated")
					entUprno.delete(0,END)
					entUprno.focus()
					entUpname.delete(0,END)
					entUpname.focus()
					entUpmarks.delete(0,END)
					entUpmarks.focus()
	
	except cx_Oracle.DatabaseError as e:
			messagebox.showerror("Error ",e)
			con.rollback()
	finally:
			if con is not None:
				con.close()
			
			
			

		
def f9():
	root.deiconify()
	upst.withdraw()
def f10():
	root.withdraw()
	dtst.deiconify()
	con=None
	try:
			con=cx_Oracle.connect("system/abc123")
			rno=entDtrno.get()
			tr_rno = rno.strip()
			rnopattern = re.match('^[0-9]+$',tr_rno)
			cursor=con.cursor()

			if len(rno) == 0:
				messagebox.showinfo("No Input","Please Enter the Roll Number")
				

			elif (tr_rno.isalpha() or not rnopattern or int(tr_rno) < 1):
				messagebox.showerror("Invalid Rno","Invalid roll number entered")
				entDtrno.delete(0,END)
				entDtrno.focus()

			else:
				r = int(tr_rno)
				sql="Delete from studentdata where ROLLNO= %d"
				args=(r)
				cursor.execute(sql % args)
				con.commit()
				if cursor.rowcount == 0:
					messagebox.showerror("Invalid Rno","Invalid roll number entered")
				else:
					messagebox.showinfo("Data deleted Succesfully",str(cursor.rowcount)+" record deleted")
				entDtrno.delete(0,END)
				entDtrno.focus()
		
	except cx_Oracle.DatabaseError as e:
			messagebox.showerror("Error ",e)
			con.rollback()
	
	finally:
			if con is not None:
				con.close()
			entDtrno.delete(0,END)
							
		
				
	
def f11():
	root.deiconify()
	dtst.withdraw()
	
def maxmarks(Name,Marks, N): 
	top3_marks=[] 
	top3_names=[]
	for i in range(0, N):  
		max1 = 0
		name=""  
		for j in range(len(Marks)):      
			if Marks[j] > max1: 
				max1 = Marks[j]; 
				name=  Name[j]
		Marks.remove(max1);
		top3_marks.append(max1) 
		Name.remove(name)
		top3_names.append(name)
          
	print(top3_marks)
	print(top3_names)
	x=ny.arange(len(top3_names))
	plt.title("Top 3 students")
	plt.bar(x,top3_marks,width=0.30,label='Marks')
	plt.xticks(x,top3_names)
	plt.xlabel("Names")
	plt.ylabel("Marks")
	plt.legend()
	plt.grid()
	plt.show()
	plt.close()	
			
	
def fetchdata():
	con=None
	try:
			con=cx_Oracle.connect("system/abc123")
			cursor=con.cursor()
			sql="select NAME,MARKS from studentdata"
			cursor.execute(sql)
			data=cursor.fetchall()
			Name=[]
			Marks=[]
			N = 0
			for d in data:
				Name.append(str(d[0]))
				Marks.append(int(d[1]))

				if( len(Name) <= 3):
					N =+ len(Name)
			
			if N > 0:
				maxmarks(Name,Marks,N)
			else:
				messagebox.showinfo("Graph","No Student data recorded")
			
			print(Name)
			print(Marks)
			
	except cx_Oracle.DatabaseError as e:
			messagebox.showerror("Error ",e)
			con.rollback()
	finally:
			if cursor is not None:
				cursor.close()
			if con is not None:
				con.close()


	
root = Tk()
root.geometry("890x600+350+50")
root.title("S M S")

quo=StringVar()
var = StringVar()
btnAdd = Button(root,text="Add",font=("arial",18,'bold'),width=10,command=f1)
btnView = Button(root,text="View",font=("arial",18,'bold'),width=10,command=f2)
btnUpdate = Button(root,text="Update",font=("arial",18,'bold'),width=10,command=f3)
btnDelete = Button(root,text="Delete",font=("arial",18,'bold'),width=10,command=f4)
btnGraph = Button(root,text="Graph",font=("arial",18,'bold'),width=10,command=fetchdata)
lblStatus=Label(root,textvariable=var,font=("arial",18,'bold'),borderwidth = 3,width = 30,relief="ridge")
lblquote=Label(root,textvariable=quo,font=("arial",18,'bold'),borderwidth=3,width=68,height=30,relief="ridge")
'''To calculate Mumbai's temperature '''
try:
	socket.create_connection (("www.google.com",80))
	print(" u r connected ")
	city="Mumbai"
	a1="http://api.openweathermap.org/data/2.5/weather?units=metric"
	a2="&q=" + city
	a3="&appid=c6e315d09197cec231495138183954bd"
	api_address= a1+ a2 +a3
	res1=requests.get(api_address)
	print(res1)
	data=res1.json()
	#print(data)
	main=data[ 'main' ]
	#print(main)
	temp=main[ 'temp' ]	
	print("temp =",temp)
	var.set("Mumbai			"+str(temp)+" °C")
except OSError as e :
	print("Check network ",e)
'''To displate the quote of the day '''

res=requests.get("https://www.brainyquote.com/quotes_of_the_day.html")
print(res)
soup=bs4.BeautifulSoup(res.text,'lxml')
quote=soup.find('img',{"class":"p-qotd"})
print(quote)
msg=quote['alt']
print(msg)
list1=msg.split(" ",6)#split the string with first 6 space 
writer=msg.split("-")#split the writer and insert in list
poped_ele=list1.pop()
quoter=writer.pop()#pop the quoter from the list
list2=[]
list2.insert(0,poped_ele)
sline=' '.join(list2)
sslist=sline.split("-")
second_line=sslist.pop(0)
first_line=' '.join(list1)#string
quo.set(first_line+"\n"+second_line+"\n"+"-"+quoter) 

btnAdd.pack(pady=10)
btnView.pack(pady=10)
btnUpdate.pack(pady=10)
btnDelete.pack(pady=10)
btnGraph.pack(pady=10)
lblStatus.pack(pady=10)
lblquote.pack(pady=10)



adst = Toplevel(root)
adst.title(" Add Student ")
adst.geometry("500x600+350+50")
adst.withdraw()


lblAddRno = Label(adst,text="Enter roll no",font=("arial",18,'bold'))
entAddrno = Entry(adst,bd=10,font=("arial",18,'bold'))
lblAddName = Label(adst,text="Enter Name",font=("arial",18,'bold'))
entAddname = Entry(adst,bd=10,font=("arial",18,'bold'))
lblAddMarks = Label(adst,text="Enter Marks",font=("arial",18,'bold'))
entAddmarks = Entry(adst,bd=10,font=("arial",18,'bold'))
btnAddSave = Button(adst,text="Save",font=("arial",18,'bold'),width=10,command=f5)
btnAddBack = Button(adst,text="Back",font=("arial",18,'bold'),width=10,command=f6)


lblAddRno.pack(pady=10)
entAddrno.pack(pady=10)
lblAddName.pack(pady=10)
entAddname.pack(pady=10)
lblAddMarks.pack(pady=10)
entAddmarks.pack(pady=10)
btnAddSave.pack(pady=10)
btnAddBack.pack(pady=10)


vwst = Toplevel(root)
vwst.title(" View Student ")
vwst.geometry("500x600+350+50")
vwst.withdraw()

stViewData= scrolledtext.ScrolledText(vwst,width=50,height=20)
btnViewBack=Button(vwst,text="Back",font=("arial",18,'bold'),command=f7)
stViewData.pack(pady=10)
btnViewBack.pack(pady=10)

upst = Toplevel(root)
upst.title(" Update Student ")
upst.geometry("500x600+350+50")
upst.withdraw()

lblUpRno = Label(upst,text="Enter roll no",font=("arial",18,'bold'))
entUprno = Entry(upst,bd=10,font=("arial",18,'bold'))
lblUpName = Label(upst,text="Enter Name",font=("arial",18,'bold'))
entUpname = Entry(upst,bd=10,font=("arial",18,'bold'))
lblUpMarks = Label(upst,text="Enter Marks",font=("arial",18,'bold'))
entUpmarks = Entry(upst,bd=10,font=("arial",18,'bold'))
btnUpSave = Button(upst,text="Save",font=("arial",18,'bold'),width=10,command=f8)
btnUpBack = Button(upst,text="Back",font=("arial",18,'bold'),width=10,command=f9)

lblUpRno.pack(pady=10)
entUprno.pack(pady=10)
lblUpName.pack(pady=10)
entUpname.pack(pady=10)
lblUpMarks.pack(pady=10)
entUpmarks.pack(pady=10)
btnUpSave.pack(pady=10)
btnUpBack.pack(pady=10)

dtst = Toplevel(root)
dtst.title(" Delete Student ")
dtst.geometry("500x600+350+50")
dtst.withdraw()

lblDtRno = Label(dtst,text="Enter roll no",font=("arial",18,'bold'))
entDtrno = Entry(dtst,bd=10,font=("arial",18,'bold'))
btnDtSave = Button(dtst,text="Save",font=("arial",18,'bold'),width=10,command=f10)
btnDtBack = Button(dtst,text="Back",font=("arial",18,'bold'),width=10,command=f11)

lblDtRno.pack(pady=10)
entDtrno.pack(pady=10)
btnDtSave.pack(pady=10)
btnDtBack.pack(pady=10)

root.mainloop()