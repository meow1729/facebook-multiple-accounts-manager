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
selected_group = None # will also be none when "All Accounts" is selected

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
    global selected_accounts
    global var
    global selected_group

    if selected_group == None:

        top = Toplevel(root)
        top.title("Can't Add Account")

        msg = Label(top, text='Cannot add account.\nYou must select a group (which is not All Accounts)')
        msg.pack()

        button = ttk.Button(top, text="Okay", command=top.destroy)
        button.pack()
    else:
        top = Toplevel(root)
        top.title('Add Account')
        msg = Label(top, text='Add an account by typing correct username and password\n Account will be added to the group : '+selected_group)
        msg.grid(row=0,column=0,columnspan=2)

        Label(top,text='Username : ').grid(row=1,column=0)
        username = Entry(top)
        username.grid(row=1,column=1)

        Label(top,text='Password : ').grid(row=2,column=0)
        password = Entry(top)
        password.grid(row=2,column=1)

        def new_account():
            global selected_accounts
            global selected_group
            global var
            u = username.get()
            p = password.get()

            if (u or p) == '':
                topp = Toplevel(top)
                topp.title('Error')
                msg = Label(topp, text='Cant add account\n You must add both username and password')
                msg.pack()
                ttk.Button(topp,text="Okay",command=topp.destroy).pack()
            else:
                top.destroy()
                topp = Toplevel()
                topp.title('Success')
                msg = Label(topp, text='    Congo,the account with email '+u+' is added to the group '+selected_group+'   ')
                msg.pack()

                #  adding account to the database(file basically) and the global variable
                new_content =''
                f = open('db.txt','r')
                ant = 0
                to_match = 'GROUP'+selected_group+'\n'
                for i in f:
                    if i == to_match:
                        ant = 1
                        new_content+=i
                        continue
                    if ant == 0:
                        new_content+=i
                    if ant == 1:
                        ant = 0
                        if len(i) >1:
                            new_content+= i.replace('\n',' ')+u+' '+p+'\n'
                        else:
                            new_content+=i.replace('\n','')+u+' '+p+'\n'
                f.close()
                f = open('db.txt','w')
                f.write(new_content)
                f.close()

                selected_accounts = []
                selected_group = None




                # updating the group waala status bar ( changing var variable)
                var.set('status of selected group:\n None selected\n It has 0 ids')

                ttk.Button(topp,text="Okay",command=topp.destroy).pack()

        ttk.Button(top,text="Submit",command=new_account).grid(row=3,columnspan=2)







def expand_selected_group():
    top = Toplevel(root)
    

def add_new_group():
    global list_of_groups
    global group_list

    # popup asking for new groups name.
    top = Toplevel(root)
    top.title("Add New Group")
    Label(top,text='').grid(row=0)
    msg = Label(top, text='Enter the name of the group you want to add : ')
    msg.grid(row=1)
    group_name = Entry(top)
    group_name.grid(row=2)


    def add_group():
        global list_of_groups
        global group_list
        g = group_name.get()
        # file updated.
        f = open('db.txt','r')
        old = f.read()
        f.close()
        print(old)
        new = old+ 'GROUP'+g+'\n\n'

        f = open('db.txt','w')
        f.write(new)
        f.close()

        f= open('db.txt','r')
        list_of_groups = []
        for line in f:
            if line[:5]=='GROUP':
                list_of_groups.append(line[5:-1])
        f.close()

        # listbox updated.
        group_list.delete(0, END)
        group_list.insert(END, 'All Accounts')
        for item in list_of_groups:
            group_list.insert(END, item)

        top.destroy()
        global selected_group,selected_accounts,var

        selected_accounts = []
        selected_group = None
        var.set('status of selected group:\n None selected\n It has 0 ids')










    ttk.Button(top,text='Add Group',command=add_group).grid(row=3)
    Label(top,text='').grid(row=4)






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
    global selected_group
    meow = group_list.get(group_list.curselection()[0])
    if meow != 'All Accounts':
        selected_group = meow
        selected_accounts = get_accounts(meow)
        if len(get_accounts(meow)) == 1:
            var.set('status of selected group:\n '+ meow + ' selected\n It has '+str(len(selected_accounts))+' id')
        else:
            var.set('status of selected group:\n '+ meow + ' selected\n It has '+str(len(selected_accounts))+' ids')
    else:
        selected_group = None
        selected_accounts=[]
        for i in list_of_groups:
            selected_accounts+=get_accounts(i)
        var.set('status of selected group:\n '+ meow + ' selected\n It has '+str(len(selected_accounts))+' ids')
    #print(selected_accounts)
    #print()
    #print(selected_group)




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
