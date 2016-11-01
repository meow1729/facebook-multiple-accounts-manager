from tkinter import *
from tkinter import messagebox # for displaying messagebox
from tkinter import ttk # for styling
from tkinter import Text
import sqlite3


def setup_db():
    pass

def update_group_list():
    pass

def load_group():
    pass





def quit_app():
    root.quit()

def show_about(event=None):
    messagebox.showwarning('About','This software is built by Aradhya Makkar.')


def new_id_pressed():
    messagebox.showwarning('Popup','This will be popup for filling up information on the selected group.')

root = Tk()
root.title("Facebook Multiple Accounts Manager")

root.geometry('1100x650+000+000')
#root.resizable(width=False,height=False)


# styling (button)
style = ttk.Style()
style.configure('TButton',foreground="black",font="Symbol 12 bold",padding=20)
#styling ends



# ~~~~~~~~~~~~~~~~~ MENU BAR STARTS ~~~~~~~~~~~~~~~~~~
the_menu = Menu(root)

# File menu
file_menu = Menu(the_menu,tearoff=0)
file_menu.add_command(label="About",command = show_about)
file_menu.add_separator()
file_menu.add_command(label="Quit",command=quit_app)
the_menu.add_cascade(label="File",menu=file_menu)
root.config(menu=the_menu)

#~~~~~~~~~~~~~~~~~ MENU BAR ENDS ~~~~~~~~~~~~~~~~~~
root.configure(background='#3b5998')


# the left side ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
add_id_button = ttk.Button(root,text="Add New Account",command=new_id_pressed,width=30)
add_id_button.grid(row=0,column=0)

# ........... list box ................
def trigger(event=None):
    print('triggered!')
    meow = group_list.get(group_list.curselection()[0])
    var.set('status of selected group:\n '+ meow + ' selected\n It has n ids')
group_list = Listbox(root,height=15,background="pink")
group_list.grid(row=1,column=0)
for item in ["All accounts", "two", "three", "four", "two", "three", "four", "two", "three", "four", "two", "three", "four", "two", "three", "four", "two", "three", "four", "two", "three", "four", "two", "three", "four"]:
    group_list.insert(END, item)

group_list.bind('<<ListboxSelect>>',trigger)

#group_list.delete(0, END)

# .............. list box

ttk.Button(root,text="Delete selected group").grid(row=2,column=0)
ttk.Button(root,text="Expand Selected Group").grid(row=3,column=0)
ttk.Separator(root,orient=HORIZONTAL).grid(row=4, columnspan=8, sticky="ew")
ttk.Separator(root,orient=VERTICAL).grid(column=1,row=0, rowspan=8, sticky="ns")
ttk.Separator(root,orient=VERTICAL).grid(column=2,row=0, rowspan=8, sticky="ns")
ttk.Separator(root,orient=VERTICAL).grid(column=3,row=0, rowspan=8, sticky="ns")
ttk.Separator(root,orient=VERTICAL).grid(column=4,row=0, rowspan=8, sticky="ns")

var = StringVar(root,value="")
var.set('status of selected group:\n None selected\n It has 0 ids')
Label(textvariable=var,background='light green').grid(row=5)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~




# the right side ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
label_1 = Label(text="Enter your message/post here:",height = 5,background='#3b5998',font=(("Helvetica", 16,'bold')) )
label_1.grid(row=0,column=5,columnspan=5)
box = Text(root,height=8,width=70,pady=10,padx=10,highlightbackground="black",background="light blue",font = "Helvetica 20 bold")
box.grid(row=1,column = 5,columnspan=5)
ttk.Button(root,text='Message to all friends').grid(row=2,column=5)
ttk.Button(root,text='Post to the wall').grid(row=2,column=6,ipady=10)
ttk.Button(root,text='Accept all friend requests').grid(row=2,column=7)
ttk.Button(root,text='Send friend requests to people you may know').grid(row=3,column=5)
ttk.Button(root,text='Get information about selected group').grid(row=3,column=7)

status_bar_right = Text(root, height= 8, width= 100,background='#C8C5C9')
status_bar_right.grid(row=5,column= 5,columnspan=5,padx= 5, pady= 10)
scrl = Scrollbar(root, command=status_bar_right.yview)
status_bar_right.config(yscrollcommand=scrl.set)
scrl.grid(row=5, column=8, sticky='n s')
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


root.mainloop()
