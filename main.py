from tkinter import *
from tkinter import messagebox # for displaying messagebox
from tkinter import ttk # for styling
from tkinter import Text


f = open('db.txt','a')
f.close()

f= open('db.txt','r')
list_of_groups = []
for line in f:
    if line[:5]=='GROUP':
        list_of_groups.append(line[5:-1])
f.close()

selected_accounts = [] # updates whenever a group is selected... 

def get_accounts(g):
    result = []
    with open('db.txt','r') as ff:
        to_match = 'GROUP'+g+'\n'
        semi_result=None
        antenna = 0
        for i in ff:
            if antenna == 1:
                antenna = 0
                semi_result = i[0:-1]
                break
            if i == to_match:
                antenna = 1
        if semi_result == None:
            return []
        else:
            a = semi_result.split(' ')
            tick = 0
            t = []
            for i in a:

                if tick ==0 :
                    t = []
                    t.append(i)
                    tick = 1
                else:
                    tick = 0
                    t.append(i)
                    result.append(t)
            return result

def add_new_account():
    pass

def expand_selected_group():
    pass

def add_new_group():
    pass

def message_to_all_friends():
    pass

def post_to_the_wall():
    pass

def accept_friend_requests():
    pass

def send_friend_requests():
    pass

def get_info():
    pass



def quit_app():
    root.quit()

def show_about(event=None):
    messagebox.showwarning('About','This software is built by Aradhya Makkar.')


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
add_id_button = ttk.Button(root,text="Add New Account",command=add_new_account,width=30)
add_id_button.grid(row=0,column=0)

# ........... list box ................
def trigger(event=None):
    global selected_accounts
    meow = group_list.get(group_list.curselection()[0])
    if meow != 'All Accounts':
        selected_accounts = get_accounts(meow)
        if len(get_accounts(meow)) == 1:
            var.set('status of selected group:\n '+ meow + ' selected\n It has '+str(len(get_accounts(meow)))+' id')
        else:
            var.set('status of selected group:\n '+ meow + ' selected\n It has '+str(len(get_accounts(meow)))+' ids')
    else:
        n = 0
        selected_accounts=[]
        for i in list_of_groups:
            selected_accounts+=get_accounts(i)
            n+= len(get_accounts(i))
        var.set('status of selected group:\n '+ meow + ' selected\n It has '+str(n)+' ids')
    print(selected_accounts)




group_list = Listbox(root,height=15,background="pink")
group_list.grid(row=1,column=0)
group_list.insert(END, 'All Accounts')
for item in list_of_groups:
    group_list.insert(END, item)

group_list.bind('<<ListboxSelect>>',trigger)

# .............. list box .......

ttk.Button(root,text="Expand Selected Group",command=expand_selected_group).grid(row=2,column=0)
ttk.Button(root,text="Add new group",command=add_new_group).grid(row=3,column=0)
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
ttk.Button(root,text='Message to all friends',command = message_to_all_friends).grid(row=2,column=5)
ttk.Button(root,text='Post to the wall',command= post_to_the_wall).grid(row=2,column=6,ipady=10)
ttk.Button(root,text='Accept all friend requests',command=accept_friend_requests).grid(row=2,column=7)
ttk.Button(root,text='Send friend requests to people you may know',command=send_friend_requests).grid(row=3,column=5)
ttk.Button(root,text='Get information about selected group',command=get_info).grid(row=3,column=7)

status_bar_right = Text(root, height= 8, width= 100,background='#C8C5C9')
status_bar_right.grid(row=5,column= 5,columnspan=5,padx= 5, pady= 10)
scrl = Scrollbar(root, command=status_bar_right.yview)
status_bar_right.config(yscrollcommand=scrl.set)
scrl.grid(row=5, column=8, sticky='n s')
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


root.mainloop()
