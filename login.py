from tkinter import *
from tkinter import messagebox
from PIL import ImageTk

root=Tk()
root.geometry('1440x900+0+0')
root.title('Admin Login')


def login():
    if usernameentry.get()=='' or passwordentry.get()=='':
         messagebox.showerror('Error','Fields cannot be empty')

    elif usernameentry.get()=='Kavish' and passwordentry.get()=='12345':
            messagebox.showinfo('Success','Login Successful')
            root.destroy()
            import sms
    else:
        messagebox.showerror('Error','Invalid Login Details')

backgroundimage=ImageTk.PhotoImage(file='bg.jpg')
bglabel=Label(root,image=backgroundimage)
bglabel.place(x=0,y=0)

loginframe=Frame(root,bg='white')
loginframe.place(x=600,y=200)

loginlogoimage=PhotoImage(file='loginlogo.png')
loginlabel=Label(loginframe, image=loginlogoimage,bg='white' )
loginlabel.grid(row=0,column=0,columnspan=2,pady=10)

usernamelabel=Label(loginframe,text='Username',font=('times new roman',22,'bold'),bg='white',fg='black')
usernamelabel.grid(row=1,column=0,pady=10,padx=15)
passwordlabel=Label(loginframe,text='Password',font=('times new roman',22,'bold'),bg='white',fg='black')
passwordlabel.grid(row=2,column=0,pady=10,padx=15)

usernameentry=Entry(loginframe,font=('times new roman',18),bg='white',fg='black',bd=4)
usernameentry.grid(row=1,column=1,pady=10)
passwordentry=Entry(loginframe,font=('times new roman',18),bg='white',fg='black',bd=4,show='*')
passwordentry.grid(row=2,column=1,pady=10)

loginbutton=Button(loginframe,text='Login',font=('times new roman',20,'bold'),width=10,command=login)
loginbutton.grid(row=3,column=1,pady=10)


root.mainloop()