from tkinter import *
from tkinter import messagebox
from tkinter import ttk

def open_msg_box():
    messagebox.showwarning(
    'Trigger warning',
    'button clicked'
    )

root = Tk()
root.title("Facebook Multiple Accounts Manager")

root.geometry('1000x500+000+000')
root.resizable(width=False,height=False)

frame = Frame(root)

style = ttk.Style()
style.configure('TButton',foreground="dark green",font="Times 20 bold italic",padding=20)


theButton = ttk.Button(frame,text="Important Button",command=open_msg_box)
theButton['state']='disabled'
theButton['state']='normal'
theButton.pack()

frame.pack()

root.mainloop()
