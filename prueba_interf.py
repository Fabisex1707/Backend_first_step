from tkinter import *
from tkinter import ttk

root=Tk()
frm= ttk.Frame(root,padding=30)
frm.grid()
ttk.Label(frm,text='Hello world').grid(column=0,row=0)
peter=Button(frm,text='quit',command=root.destroy,fg="white",bg='red').grid(column=1,row=0)
ttk.Button(peter)
print(dir(peter))
ttk.Button(frm,text='queeee').grid(column=2,row=0)
root.mainloop()