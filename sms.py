from tkinter import *
import time
import ttkthemes
import pymysql
from tkinter import ttk,messagebox
from tkinter import Text, Tk,filedialog
from tkcalendar import Calendar
from tkcalendar import DateEntry
import datetime
import pandas

root=ttkthemes.ThemedTk()
root.get_themes()
root.set_theme('radiance')
root.geometry('1440x900+0+0')
root.title('Student Management System')
s = ttk.Style()
s.configure('my.TButton', font=('Helvetica', 16,'bold'))

def clock():
    global date 
    date=time.strftime('%d/%m/%Y')
    currenttime=time.strftime('%H:%M:%S')
    datetimelabel.config(text=f'  Date:{date}\nTime:{currenttime}')
    datetimelabel.after(1000,clock)
    
def search_student():
    def search_data():
        #query='select s.ID,s.Name,a.Phone,s.class,s.section,s.sex from Student s INNER JOIN Address a ON s.ID=a.ID WHERE s.ID=%s or s.name=%s or s.Class=%s or s.Section=%s or s.sex=%s or a.phone=%s'
        query='SELECT s.ID,s.Name,a.Phone,s.class,s.section,s.sex FROM Student s INNER JOIN Address a ON s.ID = a.ID INNER JOIN Parents p ON s.ID = p.ID INNER JOIN Siblings sb ON s.ID = sb.ID WHERE s.ID=%s or s.name=%s or a.phone=%s or s.class=%s or s.section=%s or s.sex=%s;'
        cur.execute(query,(Idsearchentry.get(),namesearchentry.get(),phonesearchentry.get(),classsearchentry.get(),sectionsearchentry.get(),gendersearchentry.get()))
        fetched_data2=cur.fetchall()
        studenttable.delete(*studenttable.get_children())
        for data in fetched_data2:
          studenttable.insert('',END,values=data)





    search_window=Toplevel()
    search_window.grab_set()
    search_window.geometry('300x330+0+0')
    search_window.title("Search Student")

    Idsearchlabel=Label(search_window,text=' ID :',font=('roman',17,'bold'))
    Idsearchlabel.grid(row=0,column=0,padx=5,pady=5)
    Idsearchentry=Entry(search_window,width=15,bd=3)
    Idsearchentry.grid(row=0,column=1,padx=5,pady=5)

    namesearchlabel=Label(search_window,text=' Name :',font=('roman',17,'bold'))
    namesearchlabel.grid(row=1,column=0,padx=5,pady=5)
    namesearchentry=Entry(search_window,width=15,bd=3)
    namesearchentry.grid(row=1,column=1,padx=5,pady=5)

    phonesearchlabel=Label(search_window,text=' Phone :',font=('roman',18,'bold'))
    phonesearchlabel.grid(row=2,column=0,padx=5,pady=5)
    phonesearchentry=Entry(search_window,width=15,bd=3)
    phonesearchentry.grid(row=2,column=1,padx=5,pady=5)

    classsearchlabel=Label(search_window,text=' Class :',font=('roman',18,'bold'))
    classsearchlabel.grid(row=3,column=0,padx=5,pady=5)
    classsearchentry=Entry(search_window,width=15,bd=3)
    classsearchentry.grid(row=3,column=1,padx=5,pady=5)

    sectionsearchlabel=Label(search_window,text=' Section :',font=('roman',18,'bold'))
    sectionsearchlabel.grid(row=4,column=0,padx=5,pady=5)
    sectionsearchentry=Entry(search_window,width=15,bd=3)
    sectionsearchentry.grid(row=4,column=1,padx=5,pady=5)

    gendersearchlabel=Label(search_window,text=' Gender :',font=('roman',18,'bold'))
    gendersearchlabel.grid(row=5,column=0,padx=5,pady=5)
    gendersearchentry=Entry(search_window,width=15,bd=3)
    gendersearchentry.grid(row=5,column=1,padx=5,pady=5)

    searchbutton=ttk.Button(search_window,text=' Search Student ', command=search_data)
    searchbutton.grid(row=7,columnspan=2,padx=5,pady=5)

def delete_student():
    indexing=studenttable.focus()
    print(indexing)
    content=studenttable.item(indexing)
    print(content)
    content_id=content['values'][0]
    query='delete from student where ID=%s'
    cur.execute(query,content_id)
    con.commit()
    messagebox.showinfo('Deleted',f' The ID number {content_id} is deleted successfully')
    query='Select s.ID,s.Name,a.phone,s.class,s.section,s.sex,s.dob,a.address1 FROM Student s INNER JOIN Address a ON s.ID=a.ID;'
    cur.execute(query)
    fetched_data=cur.fetchall()
    #print(fetched_data)
    studenttable.delete(*studenttable.get_children())
    for data in fetched_data:
         studenttable.insert('',END,values=data)

def display_student():
    query='Select s.ID,s.Name,a.phone,s.class,s.section,s.sex,s.dob,a.address1 FROM Student s INNER JOIN Address a ON s.ID=a.ID;'
    cur.execute(query)
    fetched_data=cur.fetchall()
    #print(fetched_data)
    studenttable.delete(*studenttable.get_children())
    for data in fetched_data:
         studenttable.insert('',END,values=data)

def export_data():
    display_student()
    url=filedialog.asksaveasfilename(defaultextension='.csv')
    print(url)
    indexing = studenttable.get_children()
    print("Number of items:", len(indexing))
    newlist=[]
    for index in indexing:
        content=studenttable.item(index)
        datalist=content['values']
        newlist.append(datalist)
        print(newlist)

    table=pandas.DataFrame(newlist,columns=['Student ID','Name','Phone','Class','Section','Gender','D.O.B','Address'])
    table.to_csv(url,index=False)  
    messagebox.showinfo('Success','Data saved Successfully')

def exit():
    result=messagebox.askyesno('Confirm','Do you want to exit?')
    if result:
        root.destroy()
    else:
        pass


def update_student():
    
    root3=Toplevel()  
    root3.grab_set() 
    root3.geometry('1000x570+0+0')
    root3.title('Update Student Details')
    root3.grab_current()

    basicdetailframe=Frame(root3)
    basicdetailframe.place(x=10,y=15,width=930,height=240)

    S_idlabel=Label(basicdetailframe,text='Student ID :')
    S_idlabel.grid(row=0,column=0)
    S_identry=Entry(basicdetailframe,width=10)
    S_identry.grid(row=0,column=1)

    Reg_nolabel=Label(basicdetailframe,text='Reg No :')
    Reg_nolabel.grid(row=0,column=2)
    Reg_noentry=Entry(basicdetailframe,width=10)
    Reg_noentry.grid(row=0,column=3)

    variable1 = StringVar(basicdetailframe)
    variable1.set("Select")
    Categorylabel=Label(basicdetailframe,text='Category :')
    Categorylabel.grid(row=1,column=0)
    categoryoption= OptionMenu(basicdetailframe, variable1,"Select","General","SC","ST","OBC" )
    categoryoption.grid(row=1,column=1)

    Regdatelabel=Label(basicdetailframe,text='Reg date :')
    Regdatelabel.grid(row=1,column=2)
    regcalender = DateEntry(basicdetailframe, width=12,  
    background='darkblue', foreground='white', borderwidth=2,locale='en_US',date_pattern="dd/mm/yyyy")
    regcalender.set_date(date)
    regcalender.grid(row=1,column=3)


    Religionlabel=Label(basicdetailframe,text='Religion :')
    Religionlabel.grid(row=0,column=4)
    variable2 = StringVar(basicdetailframe)
    variable2.set("Select")
    religionoption= OptionMenu(basicdetailframe, variable2,"Select","Hindu","Sikh","Christan","Jain","Muslim")
    religionoption.grid(row=0,column=5)

    studentnamelabel=Label(basicdetailframe,text='Student Name :')
    studentnamelabel.grid(row=2,column=0)
    studentnamenentry=Entry(basicdetailframe,width=25)
    studentnamenentry.grid(row=2,column=1,columnspan=2)

    Sexlabel=Label(basicdetailframe,text="  Sex :")
    Sexlabel.grid(row=1,column=4)
    variable3 = StringVar(basicdetailframe)
    variable3.set("Select")
    sexoption= OptionMenu(basicdetailframe, variable3,"Select","Male","Female","Transgender","Others")
    sexoption.grid(row=1,column=5)

    Mothertonguelabel=Label(basicdetailframe,text="Mother Tongue:")
    Mothertonguelabel.grid(row=2,column=4)
    mothertongueentry=Entry(basicdetailframe,width=10)
    mothertongueentry.grid(row=2,column=5)

    DOBlabel=Label(basicdetailframe,text='Date of Birth :')
    DOBlabel.grid(row=3,column=0)
    DOBcalender = DateEntry(basicdetailframe,width=12,  
    background='darkblue', foreground='white', borderwidth=2,locale='en_US',date_pattern="dd/mm/yyyy")
    DOBcalender.set_date(date)
    DOBcalender.grid(row=3,column=1)

    birthprooflabel=Label(basicdetailframe,text='Birth Proof :')
    birthprooflabel.grid(row=3,column=2)
    birthproofentry=Entry(basicdetailframe,width=20)
    birthproofentry.grid(row=3,column=3,columnspan=2)

    Sponsorlabel=Label(basicdetailframe,text='Sponsor (if any) :')
    Sponsorlabel.grid(row=4,column=0)
    sponsorentry=Entry(basicdetailframe,width=25)
    sponsorentry.grid(row=4,column=1,columnspan=2)

    Aadharlabel=Label(basicdetailframe,text=' Aadhar Number:')
    Aadharlabel.grid(row=4,column=4)
    aadharentry=Entry(basicdetailframe,width=10)
    aadharentry.grid(row=4,column=5)

    classlabel=Label(basicdetailframe,text=" Class :")
    classlabel.grid(row=5,column=0)
    variable4 = StringVar(basicdetailframe)
    variable4.set("Select")
    classoption= OptionMenu(basicdetailframe, variable4,"Select","LKG","UKG","1st","2nd","3rd","4th","5th","6th","7th","8th","9th","10th","11th","12th")
    classoption.grid(row=5,column=1)

    sectionlabel=Label(basicdetailframe,text=" Section :")
    sectionlabel.grid(row=5,column=2)
    variable5 = StringVar(basicdetailframe)
    variable5.set("Select")
    sectionoption= OptionMenu(basicdetailframe, variable5,"Select","A","B","C","D","E","F")
    sectionoption.grid(row=5,column=3)

    rollnolabel=Label(basicdetailframe,text=" Roll No :")
    rollnolabel.grid(row=5,column=4)
    rollnoentry=Entry(basicdetailframe,width=10)
    rollnoentry.grid(row=5,column=5)

    fathernamelabel=Label(basicdetailframe,text="Father's Name :")
    fathernamelabel.grid(row=6,column=0)
    fathernamenentry=Entry(basicdetailframe,width=25)
    fathernamenentry.grid(row=6,column=1,columnspan=2)
    fatheroccupationlabel=Label(basicdetailframe,text=" Occupation :")
    fatheroccupationlabel.grid(row=6,column=3)
    fatheroccupationentry=Entry(basicdetailframe,width=25)
    fatheroccupationentry.grid(row=6,column=4,columnspan=2)

    mothernamelabel=Label(basicdetailframe,text="Mother's Name :")
    mothernamelabel.grid(row=7,column=0)
    mothernamenentry=Entry(basicdetailframe,width=25)
    mothernamenentry.grid(row=7,column=1,columnspan=2)
    motheroccupationlabel=Label(basicdetailframe,text=" Occupation :")
    motheroccupationlabel.grid(row=7,column=3)
    motheroccupationentry=Entry(basicdetailframe,width=25)
    motheroccupationentry.grid(row=7,column=4,columnspan=2)


    addressframe=Frame(root3,bg="royalblue")
    addressframe.place(x=10,y=250,width=930,height=23)
    residancelabel=Label(addressframe,text='Residance Address',font=('times new roman',16,'bold'),fg='white',bg='royalblue')
    residancelabel.grid(row=0,column=0,padx=15)

    addressdetailsframe=Frame(root3)
    addressdetailsframe.place(x=10,y=275,width=930,height=130)

    address1label=Label(addressdetailsframe,text=' Address 1 :')
    address1label.grid(row=0,column=0)
    address1entry=Entry(addressdetailsframe,width=55)
    address1entry.grid(row=0,column=1,columnspan=5)

    address2label=Label(addressdetailsframe,text=' Address 2 :')
    address2label.grid(row=1,column=0)
    address2entry=Entry(addressdetailsframe,width=55)
    address2entry.grid(row=1,column=1,columnspan=5)

    villagelabel=Label(addressdetailsframe,text=' City/Village :')
    villagelabel.grid(row=2,column=0,pady=3)
    villageentry=Entry(addressdetailsframe,width=15)
    villageentry.grid(row=2,column=1,pady=3)

    districtlabel=Label(addressdetailsframe,text=' District :')
    districtlabel.grid(row=2,column=2,pady=3)
    districtentry=Entry(addressdetailsframe,width=15)
    districtentry.grid(row=2,column=3,pady=3)

    statelabel=Label(addressdetailsframe,text=' State :')
    statelabel.grid(row=2,column=4,pady=3)
    stateentry=Entry(addressdetailsframe,width=15)
    stateentry.grid(row=2,column=5,pady=3)

    pincodelabel=Label(addressdetailsframe,text=' Pincode :')
    pincodelabel.grid(row=2,column=6,pady=3)
    pincodeentry=Entry(addressdetailsframe,width=15)
    pincodeentry.grid(row=2,column=7,pady=3)

    phonelabel=Label(addressdetailsframe,text=' Phone :')
    phonelabel.grid(row=3,column=0,pady=3)
    phoneentry=Entry(addressdetailsframe,width=15)
    phoneentry.grid(row=3,column=1,pady=3)

    Mobilelabel=Label(addressdetailsframe,text=' Mobile :')
    Mobilelabel.grid(row=3,column=2,pady=3)
    mobileentry=Entry(addressdetailsframe,width=15)
    mobileentry.grid(row=3,column=3,pady=3)

    emaillabel=Label(addressdetailsframe,text=' Email :')
    emaillabel.grid(row=3,column=4,pady=3)
    emailentry=Entry(addressdetailsframe,width=15)
    emailentry.grid(row=3,column=5,pady=3)

    siblingdetailframe=Frame(root3,highlightbackground='gray64',highlightthickness='2')
    siblingdetailframe.place(x=10,y=410,width=450,height=118)

    siblinglabel=Label(siblingdetailframe,text=' Siblings Details :',font=('roman',14,'bold'))
    siblinglabel.grid(row=0,column=0)

    siblingidlabel=Label(siblingdetailframe,text=" Sibling's ID :" )
    siblingidlabel.grid(row=1,column=0)
    siblingidentry=Entry(siblingdetailframe,width=10)
    siblingidentry.grid(row=1,column=1)

    siblingnamelabel=Label(siblingdetailframe,text=" Sibling's Name :" )
    siblingnamelabel.grid(row=2,column=0)
    siblingnameentry=Entry(siblingdetailframe,width=25)
    siblingnameentry.grid(row=2,column=1,columnspan=2)

    remarkslabel=Label(siblingdetailframe,text=" Remarks (if any) :" )
    remarkslabel.grid(row=3,column=0)

    remarksentry=Entry(siblingdetailframe,width=25)
    remarksentry.grid(row=3,column=1,columnspan=2)
    
    savebutton=ttk.Button(root3,text='Update')
    savebutton.place(x=800,y=500)    

    indexing=studenttable.focus
    print(indexing)
    content=studenttable.item(indexing)
    #print(content)
    listdata=content['values']
    print(listdata)
    S_identry.insert(0,listdata[0])
    Reg_noentry.insert(0,listdata[1])
    variable1.set(0,listdata[2])
    variable2.set[0,listdata[3]]
    variable3.set[0,listdata[5]]
    studentnamenentry.insert[0,listdata[6]]
    mothertongueentry.insert[0,listdata[7]]
    birthproofentry.insert[0,listdata[9]]
    sponsorentry.insert[0,listdata[10]]
    aadharentry.insert[0,listdata[11]]
    variable4.set[0,listdata[12]]
    variable5.set[0,listdata[13]]
    rollnoentry.insert[0,listdata[14]]
    fathernamenentry.insert[0,listdata[15]]
    fatheroccupationentry.insert[0,listdata[16]]
    mothernamenentry.insert[0,listdata[17]]
    motheroccupationentry.insert[0,listdata[18]]
    address1entry.insert[0,listdata[20]]
    address2entry.insert[0,listdata[21]]
    villageentry.insert[0,listdata[22]]
    districtentry.insert[0,listdata[23]]
    stateentry.insert[0,listdata[24]]
    pincodeentry.insert[0,listdata[25]]
    phoneentry.insert[0,listdata[26]]
    mobileentry.insert[0,listdata[27]]
    emailentry.insert[0,listdata[28]]
    siblingidentry.insert[0,listdata[29]]
    siblingnameentry.insert[0,listdata[30]]
    remarksentry.insert[0,listdata[31]]

def addstudent():
    def add_data():
            if  S_identry.get()=='' or Reg_noentry.get()=='' or studentnamenentry.get()=='' or aadharentry.get()=='':
                messagebox.showerror('Error','ID, Reg No., Name, Aadhar No. is necessary')
            
            
            else:
                try:
                    query='insert into Student(ID,regno,religion,category,regdate,sex,name,mothertongue,dob,birthproof,sponsor,aadharno,class,section,rollno) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
                    cur.execute(query,(S_identry.get(),Reg_noentry.get(),variable2.get(),variable1.get(),regcalender.get_date(),variable3.get(),studentnamenentry.get(),mothertongueentry.get(),DOBcalender.get_date(),birthproofentry.get(),sponsorentry.get(),aadharentry.get(),variable4.get(),variable5.get(),rollnoentry.get()))
                    query='insert into Parents(ID,fathername,fatheroccupation,mothername,motheroccupation) values(%s,%s,%s,%s,%s)'
                    cur.execute(query,(S_identry.get(),fathernamenentry.get(),fatheroccupationentry.get(),mothernamenentry.get(),motheroccupationentry.get()))
                    query='insert into Address(ID,Address1,Address2,City,District,State,pincode,phone,mobile,email) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
                    cur.execute(query,(S_identry.get(),address1entry.get(),address2entry.get(),villageentry.get(),districtentry.get(),stateentry.get(),pincodeentry.get(),phoneentry.get(),mobileentry.get(),emailentry.get()))
                    query='insert into Siblings(ID,SiblingID,Siblingname,remarks) values(%s,%s,%s,%s)'
                    cur.execute(query,(S_identry.get(),siblingidentry.get(),siblingnameentry.get(),remarksentry.get()))
                    con.commit()
                    result=messagebox.askyesno('Confirm','Data added successfully. Do you want to clear the form?')
                    if result:
                        S_identry.delete(0,END)
                        Reg_noentry.delete(0,END)
                        variable1.set("Default value")
                        variable2.set("Default value")
                        regcalender.set_date(date)
                        variable3.set("Default value")
                        studentnamenentry.delete(0,END)
                        mothertongueentry.delete(0,END)
                        DOBcalender.set_date(date)
                        birthproofentry.delete(0,END)
                        sponsorentry.delete(0,END)
                        aadharentry.delete(0,END)
                        variable4.set("Default value")
                        variable5.set("Default value")
                        rollnoentry.delete(0,END)
                        fathernamenentry.delete(0,END)
                        fatheroccupationentry.delete(0,END)
                        mothernamenentry.delete(0,END)
                        motheroccupationentry.delete(0,END)
                        address1entry.delete(0,END)
                        address2entry.delete(0,END)
                        villageentry.delete(0,END)
                        districtentry.delete(0,END)
                        stateentry.delete(0,END)
                        pincodeentry.delete(0,END)
                        phoneentry.delete(0,END)
                        mobileentry.delete(0,END)
                        siblingidentry.delete(0,END)
                        siblingnameentry.delete(0,END)
                        remarksentry.delete(0,END)
                        emailentry.delete(0,END)

                    else:
                        pass
                except:
                    messagebox.showerror('Error','ID already exists. Cannot be repeated.')
                    return
                
                query = 'Select s.ID,s.Name,a.phone,s.class,s.section,s.sex,s.dob,a.address1 FROM Student s INNER JOIN Address a ON s.ID=a.ID;'
                cur.execute(query)
                fetched_data=cur.fetchall()
                    #print(fetched_data)
                studenttable.delete(*studenttable.get_children())
                for data in fetched_data:
                    studenttable.insert('',END,values=data)



    root2=Toplevel()  
    root2.grab_set() 
    root2.geometry('1000x570+0+0')
    root2.title('Student Registration')
    root2.grab_current()

    basicdetailframe=Frame(root2)
    basicdetailframe.place(x=10,y=15,width=930,height=240)

    S_idlabel=Label(basicdetailframe,text='Student ID :')
    S_idlabel.grid(row=0,column=0)
    S_identry=Entry(basicdetailframe,width=10)
    S_identry.grid(row=0,column=1)

    Reg_nolabel=Label(basicdetailframe,text='Reg No :')
    Reg_nolabel.grid(row=0,column=2)
    Reg_noentry=Entry(basicdetailframe,width=10)
    Reg_noentry.grid(row=0,column=3)

    variable1 = StringVar(basicdetailframe)
    variable1.set("Select")
    Categorylabel=Label(basicdetailframe,text='Category :')
    Categorylabel.grid(row=1,column=0)
    categoryoption= OptionMenu(basicdetailframe, variable1,"Select","General","SC","ST","OBC" )
    categoryoption.grid(row=1,column=1)

    Regdatelabel=Label(basicdetailframe,text='Reg date :')
    Regdatelabel.grid(row=1,column=2)
    regcalender = DateEntry(basicdetailframe, width=12,  
    background='darkblue', foreground='white', borderwidth=2,locale='en_US',date_pattern="dd/mm/yyyy")
    regcalender.set_date(date)
    regcalender.grid(row=1,column=3)


    Religionlabel=Label(basicdetailframe,text='Religion :')
    Religionlabel.grid(row=0,column=4)
    variable2 = StringVar(basicdetailframe)
    variable2.set("Select")
    religionoption= OptionMenu(basicdetailframe, variable2,"Select","Hindu","Sikh","Christan","Jain","Muslim")
    religionoption.grid(row=0,column=5)

    studentnamelabel=Label(basicdetailframe,text='Student Name :')
    studentnamelabel.grid(row=2,column=0)
    studentnamenentry=Entry(basicdetailframe,width=25)
    studentnamenentry.grid(row=2,column=1,columnspan=2)

    Sexlabel=Label(basicdetailframe,text="  Sex :")
    Sexlabel.grid(row=1,column=4)
    global variable3
    variable3 = StringVar(basicdetailframe)
    variable3.set("Select")
    sexoption= OptionMenu(basicdetailframe, variable3,"Select","Male","Female","Transgender","Others")
    sexoption.grid(row=1,column=5)

    Mothertonguelabel=Label(basicdetailframe,text="Mother Tongue:")
    Mothertonguelabel.grid(row=2,column=4)
    mothertongueentry=Entry(basicdetailframe,width=10)
    mothertongueentry.grid(row=2,column=5)

    DOBlabel=Label(basicdetailframe,text='Date of Birth :')
    DOBlabel.grid(row=3,column=0)
    DOBcalender = DateEntry(basicdetailframe,width=12,  
    background='darkblue', foreground='white', borderwidth=2,locale='en_US',date_pattern="dd/mm/yyyy")
    DOBcalender.set_date(date)
    DOBcalender.grid(row=3,column=1)

    birthprooflabel=Label(basicdetailframe,text='Birth Proof :')
    birthprooflabel.grid(row=3,column=2)
    birthproofentry=Entry(basicdetailframe,width=20)
    birthproofentry.grid(row=3,column=3,columnspan=2)

    Sponsorlabel=Label(basicdetailframe,text='Sponsor (if any) :')
    Sponsorlabel.grid(row=4,column=0)
    sponsorentry=Entry(basicdetailframe,width=25)
    sponsorentry.grid(row=4,column=1,columnspan=2)

    Aadharlabel=Label(basicdetailframe,text=' Aadhar Number:')
    Aadharlabel.grid(row=4,column=4)
    aadharentry=Entry(basicdetailframe,width=10)
    aadharentry.grid(row=4,column=5)

    classlabel=Label(basicdetailframe,text=" Class :")
    classlabel.grid(row=5,column=0)
    global variable4
    variable4 = StringVar(basicdetailframe)
    variable4.set("Select")
    classoption= OptionMenu(basicdetailframe, variable4,"Select","LKG","UKG","1st","2nd","3rd","4th","5th","6th","7th","8th","9th","10th","11th","12th")
    classoption.grid(row=5,column=1)

    sectionlabel=Label(basicdetailframe,text=" Section :")
    sectionlabel.grid(row=5,column=2)
    global variable5
    variable5 = StringVar(basicdetailframe)
    variable5.set("Select")
    sectionoption= OptionMenu(basicdetailframe, variable5,"Select","A","B","C","D","E","F")
    sectionoption.grid(row=5,column=3)

    rollnolabel=Label(basicdetailframe,text=" Roll No :")
    rollnolabel.grid(row=5,column=4)
    rollnoentry=Entry(basicdetailframe,width=10)
    rollnoentry.grid(row=5,column=5)

    fathernamelabel=Label(basicdetailframe,text="Father's Name :")
    fathernamelabel.grid(row=6,column=0)
    fathernamenentry=Entry(basicdetailframe,width=25)
    fathernamenentry.grid(row=6,column=1,columnspan=2)
    fatheroccupationlabel=Label(basicdetailframe,text=" Occupation :")
    fatheroccupationlabel.grid(row=6,column=3)
    fatheroccupationentry=Entry(basicdetailframe,width=25)
    fatheroccupationentry.grid(row=6,column=4,columnspan=2)

    mothernamelabel=Label(basicdetailframe,text="Mother's Name :")
    mothernamelabel.grid(row=7,column=0)
    mothernamenentry=Entry(basicdetailframe,width=25)
    mothernamenentry.grid(row=7,column=1,columnspan=2)
    motheroccupationlabel=Label(basicdetailframe,text=" Occupation :")
    motheroccupationlabel.grid(row=7,column=3)
    motheroccupationentry=Entry(basicdetailframe,width=25)
    motheroccupationentry.grid(row=7,column=4,columnspan=2)


    addressframe=Frame(root2,bg="royalblue")
    addressframe.place(x=10,y=250,width=930,height=23)
    residancelabel=Label(addressframe,text='Residance Address',font=('times new roman',16,'bold'),fg='white',bg='royalblue')
    residancelabel.grid(row=0,column=0,padx=15)

    addressdetailsframe=Frame(root2)
    addressdetailsframe.place(x=10,y=275,width=930,height=130)

    address1label=Label(addressdetailsframe,text=' Address 1 :')
    address1label.grid(row=0,column=0)
    address1entry=Entry(addressdetailsframe,width=55)
    address1entry.grid(row=0,column=1,columnspan=5)

    address2label=Label(addressdetailsframe,text=' Address 2 :')
    address2label.grid(row=1,column=0)
    address2entry=Entry(addressdetailsframe,width=55)
    address2entry.grid(row=1,column=1,columnspan=5)

    villagelabel=Label(addressdetailsframe,text=' City/Village :')
    villagelabel.grid(row=2,column=0,pady=3)
    villageentry=Entry(addressdetailsframe,width=15)
    villageentry.grid(row=2,column=1,pady=3)

    districtlabel=Label(addressdetailsframe,text=' District :')
    districtlabel.grid(row=2,column=2,pady=3)
    districtentry=Entry(addressdetailsframe,width=15)
    districtentry.grid(row=2,column=3,pady=3)

    statelabel=Label(addressdetailsframe,text=' State :')
    statelabel.grid(row=2,column=4,pady=3)
    stateentry=Entry(addressdetailsframe,width=15)
    stateentry.grid(row=2,column=5,pady=3)

    pincodelabel=Label(addressdetailsframe,text=' Pincode :')
    pincodelabel.grid(row=2,column=6,pady=3)
    pincodeentry=Entry(addressdetailsframe,width=15)
    pincodeentry.grid(row=2,column=7,pady=3)

    phonelabel=Label(addressdetailsframe,text=' Phone :')
    phonelabel.grid(row=3,column=0,pady=3)
    phoneentry=Entry(addressdetailsframe,width=15)
    phoneentry.grid(row=3,column=1,pady=3)

    Mobilelabel=Label(addressdetailsframe,text=' Mobile :')
    Mobilelabel.grid(row=3,column=2,pady=3)
    mobileentry=Entry(addressdetailsframe,width=15)
    mobileentry.grid(row=3,column=3,pady=3)

    emaillabel=Label(addressdetailsframe,text=' Email :')
    emaillabel.grid(row=3,column=4,pady=3)
    emailentry=Entry(addressdetailsframe,width=15)
    emailentry.grid(row=3,column=5,pady=3)

    siblingdetailframe=Frame(root2,highlightbackground='gray64',highlightthickness='2')
    siblingdetailframe.place(x=10,y=410,width=450,height=118)

    siblinglabel=Label(siblingdetailframe,text=' Siblings Details :',font=('roman',14,'bold'))
    siblinglabel.grid(row=0,column=0)

    siblingidlabel=Label(siblingdetailframe,text=" Sibling's ID :" )
    siblingidlabel.grid(row=1,column=0)
    siblingidentry=Entry(siblingdetailframe,width=10)
    siblingidentry.grid(row=1,column=1)

    siblingnamelabel=Label(siblingdetailframe,text=" Sibling's Name :" )
    siblingnamelabel.grid(row=2,column=0)
    siblingnameentry=Entry(siblingdetailframe,width=25)
    siblingnameentry.grid(row=2,column=1,columnspan=2)

    remarkslabel=Label(siblingdetailframe,text=" Remarks (if any) :" )
    remarkslabel.grid(row=3,column=0)
    remarksentry=Entry(siblingdetailframe,width=25)
    remarksentry.grid(row=3,column=1,columnspan=2)
    
    savebutton=ttk.Button(root2,text='Save',command=add_data)
    savebutton.place(x=800,y=500)
    
def connectdatabase():
    def connectionestablished():
        global cur
        global con
        try:
            con=pymysql.connect(host='localhost',user='root',password='MyNewPass')
            cur=con.cursor()
        except:
            messagebox.showerror('Error','Invalid details')
            return
            
        try:
             query='create database studentsystem'
             cur.execute(query)
             query='use studentsystem'
             cur.execute(query)
             query='CREATE TABLE Student( ID varchar(10) NOT NULL PRIMARY KEY, regno varchar(10), religion varchar(10), category varchar(10),regdate date, sex varchar(8), name varchar(25) NOT NULL, mothertongue varchar(10), dob date, birthproof varchar(15),sponsor varchar(20),aadharno varchar(15),class varchar(10),section varchar(10), rollno varchar(5))'
             cur.execute(query)
             query='CREATE TABLE Parents(ID varchar(10),fathername varchar(25),fatheroccupation varchar(10), mothername varchar(25), motheroccupation varchar(10), foreign key (ID) references Student(ID) ON DELETE CASCADE)'
             cur.execute(query)
             query='Create table Address(ID varchar(10), Address1 varchar(25), Address2 varchar(25), City varchar(10), District varchar(10), State varchar(10), pincode varchar(10), phone varchar(10), mobile varchar(10), email varchar(15),foreign key (ID) references Student(ID) ON DELETE CASCADE)'
             cur.execute(query)
             query='Create table  Siblings(ID varchar(10), SiblingID varchar(10), Siblingname varchar(25), remarks varchar(25),foreign key (ID) references Student(ID) ON DELETE CASCADE) '
             cur.execute(query)
        
        except:
             query='use studentsystem'
             cur.execute(query)
        messagebox.showinfo('Success','Database connection successful')
        connectwindow.destroy()
        addstudentbutton.config(state=NORMAL)
        searchstudentbutton.config(state=NORMAL)
        deletestudentbutton.config(state=NORMAL)
        displaystudentbutton.config(state=NORMAL)
        exportstudentdatabutton.config(state=NORMAL)
        updatestudentbutton.config(state=NORMAL)






    connectwindow=Toplevel()
    connectwindow.title('Database Connection')
    connectwindow.geometry('470x250+750+250')
    connectwindow.grab_set()

    hostnamelabel=Label(connectwindow,text=" Host Name :",font=("roman",20,"bold"))
    hostnamelabel.grid(row=0,column=0,padx=10,pady=12)
    hostentry=Entry(connectwindow,font=("roman",16,"bold"),bd=3)
    hostentry.grid(row=0,column=1,padx=25,pady=12)

    usernamelabel=Label(connectwindow,text=" User Name :",font=("roman",20,"bold"),fg="red")
    usernamelabel.grid(row=1,column=0,padx=10,pady=12)
    usernameentry=Entry(connectwindow,font=("roman",16,"bold"),bd=3)
    usernameentry.grid(row=1,column=1,padx=25,pady=12)
    
    passwordlabel=Label(connectwindow,text=" Password :",font=("roman",20,"bold"),fg="red")
    passwordlabel.grid(row=2,column=0,padx=10,pady=12)
    passentry=Entry(connectwindow,font=("roman",16,"bold"),bd=3,show='*')
    passentry.grid(row=2,column=1,padx=25,pady=12)

    connectbutton=ttk.Button(connectwindow,text='CONNECT',command=connectionestablished)
    connectbutton.grid(row=4,column=1)
datetimelabel=Label(root,font=('times new roman',20,'bold'))
datetimelabel.place(x=5,y=5)
clock()

headinglabel=Label(root,text='Student Management System',font=('times new roman',38,'bold'))
headinglabel.place(x=500,y=5)

connectdatabasebutton=ttk.Button(root,text='Connect Database',command=connectdatabase)
connectdatabasebutton.place(x=1200,y=8)

leftframe=Frame(root)
leftframe.place(x=40,y=150,width=250,height=700)

logo_image=PhotoImage(file='students.png')
logo_image_label=Label(leftframe,image=logo_image)
logo_image_label.grid(row=0,column=0)

addstudentbutton=ttk.Button(leftframe,text='Add Student',width=20,style='my.TButton',command=addstudent,state=DISABLED)
addstudentbutton.grid(row=1,column=0,pady=25)
searchstudentbutton=ttk.Button(leftframe,text='Search Student',width=20,style='my.TButton',command=search_student,state=DISABLED)
searchstudentbutton.grid(row=2,column=0,pady=25)
deletestudentbutton=ttk.Button(leftframe,text='Delete Student',width=20,style='my.TButton',command=delete_student,state=DISABLED)
deletestudentbutton.grid(row=3,column=0,pady=25)
updatestudentbutton=ttk.Button(leftframe,text='Update Student',width=20,style='my.TButton',command=update_student,state=DISABLED)
updatestudentbutton.grid(row=4,column=0,pady=25)
displaystudentbutton=ttk.Button(leftframe,text='Display Students',width=20,style='my.TButton',command=display_student,state=DISABLED)
displaystudentbutton.grid(row=5,column=0,pady=25)
exportstudentdatabutton=ttk.Button(leftframe,text='Export Student Data',width=20,style='my.TButton',command=export_data,state=DISABLED)
exportstudentdatabutton.grid(row=6,column=0,pady=25)
exitbutton=ttk.Button(leftframe,text='Exit',width=15,style='my.TButton',command=exit)
exitbutton.grid(row=7,column=0,pady=20)


rightframe=Frame(root)
rightframe.place(x=380,y=150,width=1020,height=650)
#scrollbarx=Scrollbar(rightframe,orient=HORIZONTAL)
#scrollbary=Scrollbar(rightframe,orient=VERTICAL)
global studenttable
studenttable=ttk.Treeview(rightframe,columns=('ID','Name','Phone','Class','Section','Gender','D.O.B','Address'))
studenttable.pack(fill=BOTH,expand=1 )

#scrollbarx.config(studenttable.xview)
#scrollbary.config(studenttable.yview)
#yscrollcommand=scrollbary.set,xscrollcommand=scrollbarx.set,
#scrollbarx.pack(BOTTOM,fill=X)
#scrollbary.pack(RIGHT,fill=Y)


studenttable.heading('ID',text='Student ID')
studenttable.heading('Name',text='Name')
studenttable.heading('Phone',text='Phone No.')
studenttable.heading('Class',text='Class')
studenttable.heading('Section',text='Section')
studenttable.heading('Gender',text='Gender')
studenttable.heading('D.O.B',text='Date of Birth')
studenttable.heading('Address',text='Residential Address')
studenttable.config(show='headings')

studenttable.column('ID',width=100,anchor=CENTER)
studenttable.column('Name',width=260,anchor=CENTER)
studenttable.column('Phone',width=260,anchor=CENTER)
studenttable.column('Class',width=150,anchor=CENTER)
studenttable.column('Section',width=150,anchor=CENTER)
studenttable.column('Gender',width=100,anchor=CENTER)
studenttable.column('Address',width=260,anchor=CENTER)
studenttable.column('D.O.B',width=180,anchor=CENTER)
style=ttk.Style()
style.configure('Treeview',rowheight=30,font=('roman',12,'bold'))
style.configure('Treeview.Heading',font=('roman',14,'bold'))



root.mainloop()