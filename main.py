from tkinter import *
from tkinter import messagebox # for displaying messagebox
from tkinter import ttk # for styling
from tkinter import Text
from selenium import webdriver
import time


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
sa = None # selected account when group is expanded. it's global for a reason.


def output_to_widget(message):
    status_bar_right.insert(INSERT, message)
    status_bar_right.see(END)

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
    global sa,var,selected_accounts
    sa = None
    global list_of_groups
    global selected_group
    global group_list
    if selected_group==None:
        top = Toplevel(root)
        top.title("Error")
        Label(top,text='').grid(row=0)
        Label(top,text='     You must select a group!     ').grid(row=1)
        Label(top,text='').grid(row=2)
        ttk.Button(top,text='Okay',command=top.destroy).grid(row=3)
        return
    top = Toplevel(root)
    top.title("Group settings - "+selected_group)
    Label(top,text='').grid(row=0)
    zoom = StringVar()
    if len(selected_accounts)!=1:
        Label(top, textvariable=zoom).grid(row=1,column=0)
        zoom.set('         The group {} has {} accounts :        '.format(selected_group,str(len(selected_accounts))))
    else:
        Label(top, textvariable=zoom).grid(row=1,column=0)
        zoom.set('         The group {} has {} account :        '.format(selected_group,str(len(selected_accounts))))
    Label(top,text='').grid(row=2)

    acc_list = Listbox(top,height=15,background="pink")
    acc_list.grid(row=3,column=0)
    for item in selected_accounts:
        acc_list.insert(END, item[0])

    Label(top,text='').grid(row=4)

    def boom(event=None):
        global sa
        sa = acc_list.get(acc_list.curselection()[0])

    acc_list.bind('<<ListboxSelect>>',boom)

    def delete_selected_account():
        global sa,var,selected_accounts
        if sa == None:
            topp = Toplevel(top)
            topp.title('Error')

            Label(topp,text='').grid(row=0)
            Label(topp,text='     You must select an account!     ').grid(row=1)
            Label(topp,text='').grid(row=2)
            ttk.Button(topp,text='Okay',command=topp.destroy).grid(row=3)
            return

        topp = Toplevel(top)
        topp.title('Confirmation')

        Label(topp,text='').grid(row=0,columnspan=2)
        Label(topp,text='     Are you sure you want to delete {} from group {} ?   '.format(sa,selected_group)).grid(row=1,columnspan=2)
        Label(topp,text='').grid(row=2,columnspan=2)
        def destroy_account():
            global sa,var,selected_accounts

            # removing the fucking popup ka popup (topp)
            topp.destroy()

            # deleting the account from the file, ( only from the selected group )
            new = ''
            f= open('db.txt','r')
            tick = 0
            for line in f:
                if line == 'GROUP'+selected_group+'\n':
                    new += line
                    tick = 1
                    continue
                if tick == 0:
                    new += line
                if tick == 1:
                    tick = 0
                    l =line.split(' ')
                    l[-1] = l[-1][:-1]

                    for_modified_line=[]
                    pick = 0
                    for i in l:
                        if i == sa:
                            pick = 1
                            continue
                        if pick == 0:
                            for_modified_line.append(i)
                        if pick == 1:
                            pick = 0
                    #print(len(for_modified_line))

                    if len(for_modified_line) > 0:

                        modified_line=''
                        for i in for_modified_line:
                            modified_line+=(i+' ')
                        modified_line= modified_line[:-1]+'\n'
                    else:
                        modified_line='\n'

                    new+=modified_line
            f.close()

            f = open('db.txt','w')
            f.write(new)
            f.close()

            # updating sa and ..
            # updating selected_accounts variable
            for item in selected_accounts:
                if item[0]==sa:
                    selected_accounts.remove(item)
                    break
            sa = None

            # updating var for updating status bar
            if len(selected_accounts) == 1:
                var.set('status of selected group:\n '+ selected_group + ' selected\n It has '+str(len(selected_accounts))+' id')
            else:
                var.set('status of selected group:\n '+ selected_group + ' selected\n It has '+str(len(selected_accounts))+' ids')

            # updating the listbox of the top popup
            acc_list.delete(0, END)
            for item in selected_accounts:
                acc_list.insert(END, item[0])

            # updating the uppar waala text of the top popup
            if len(selected_accounts)!=1:
                zoom.set('         The group {} has {} accounts :        '.format(selected_group,str(len(selected_accounts))))
            else:
                zoom.set('         The group {} has {} account :        '.format(selected_group,str(len(selected_accounts))))

        ttk.Button(topp,text="Yes",command=destroy_account).grid(row=3,column=0)
        ttk.Button(topp,text="No",command=topp.destroy).grid(row=3,column=1)






    ttk.Button(top,text='Delete Selected account from group',command=delete_selected_account).grid(row=5)

    def delete_complete_group():
        global selected_group,selected_accounts
        global list_of_groups
        global group_list
        topp = Toplevel(top)
        topp.title('Confirmation')
        Label(topp,text='').grid(row=0,columnspan=2)
        Label(topp,text='   This action will also delete all the accounts inside the group   ').grid(row=1,columnspan=2)
        Label(topp,text='   Are you sure you want to delete this group?   ').grid(row=2,columnspan=2)
        Label(topp,text='').grid(row=3)
        def destroy_group():
            global selected_group,selected_accounts
            global group_list

            # closing the fucking popups
            topp.destroy()
            top.destroy()

            # destroying the group from the file
            new =''
            f = open('db.txt','r')
            tick = 0
            for line in f:
                if line == 'GROUP'+selected_group+'\n':
                    tick = 1
                    continue
                if tick == 0:
                    new += line
                if tick == 1:
                    tick = 0

            f.close()
            f = open('db.txt','w')
            f.write(new)
            f.close()

            # updating the global variables selected_group and selected_accounts
            selected_group=None
            selected_accounts = []


            # Updating the listbox
            global list_of_groups
            f= open('db.txt','r')
            list_of_groups = []
            for line in f:
                if line[:5]=='GROUP':
                    list_of_groups.append(line[5:-1])
            f.close()

            global group_list

            group_list.delete(0, END)
            group_list.insert(END, 'All Accounts')
            for item in list_of_groups:
                group_list.insert(END, item)




            # updating the groups status bar
            global var
            var.set('status of selected group:\n None selected\n It has 0 ids')



        ttk.Button(topp,text='yes',command=destroy_group).grid(row=4,column=0)
        ttk.Button(topp,text='no',command=topp.destroy).grid(row=4,column=1)



    ttk.Button(top,text='Delete the complete Group',command=delete_complete_group).grid(row=6)



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
        #print(old)
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
    if len(selected_accounts)==0:
        messagebox.showwarning('Error',"Please select a group with finite number of accounts.")
        return

    if box.get("1.0",'end-1c') == '':
        messagebox.showwarning('Error','You need to type something in the box to send to friends. Its empty right now')
        return

    top = Toplevel(root)
    Label(top,text='').grid(row=0,columnspan=2)
    if len(selected_accounts) > 1:
        Label(top,text='    This command will send message to all friends on all {} accounts of the selected group.     \n     Are you sure you want to continue?'.format(str(len(selected_accounts)))).grid(row=1,columnspan=2)
    else:
        Label(top,text='    This command will accept friend requests on all accounts of the selected group.     \n     Are you sure you want to continue?').grid(row=1,columnspan=2)
    Label(top,text='').grid(row=2,columnspan=2)

    def message():
        top.destroy()
        output_to_widget('starting ...\n\n')
        for t in selected_accounts:
            driver = webdriver.PhantomJS()
            driver.get('http://facebook.com')

            #logging in
            emailElem = driver.find_element_by_id('email')
            emailElem.send_keys(t[0])
            passElem = driver.find_element_by_id('pass')
            passElem.send_keys(t[1])
            passElem.submit()


            # getting number of friends in variable nof as integer
            driver.get('http://facebook.com/me/friends')
            try:
                nof = driver.find_element_by_css_selector('._gs6')
                nof = int(nof.text)
            except:
                output_to_widget('Unable to login on {}, incorrect password or something.. \n'.format(t[0]))
                continue
            #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~




            #getting list of friends url in links ~~~~~~~~~~
            driver.get('https://m.facebook.com/profile.php?v=friends')
            nice_hyperlinks=[]

            while len(nice_hyperlinks) <= nof-5:
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(1)

                #print('tick')
                #print(len(nice_hyperlinks))
                nice_hyperlinks = []

                hyperlinks = driver.find_elements_by_tag_name('a')
                for i in hyperlinks:
                    if i.text !='' and i.text != 'Find Friends' and i.text != 'Active Friends' and i.text != 'Public' and i.text!= 'Only Me':
                        nice_hyperlinks.append(i)

            #print('lenght of hypelinks : '+str(len(nice_hyperlinks)))

            links = []
            for i in nice_hyperlinks:
                links.append(    str( i.get_attribute('href'))[0:8] +   str(i.get_attribute('href'))[10:]  )


            #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



            # sending message to friends~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            message =  box.get("1.0",'end-1c')

            for i in links:

                message_link = (i)[0:21]+'messages/'+(i)[21:]
                #print(message_link)
                driver.get(message_link)

                try:
                    boxx = driver.find_element_by_css_selector('textarea')

                    boxx.send_keys(message)

                    send_buttonsssss = driver.find_elements_by_tag_name('input')

                    new = ''
                    for j in send_buttonsssss:
                        if j.get_attribute('value') == 'Send' or j.get_attribute('value') == 'Reply':
                            new = j
                            new.click()
                            break
                except:
                    continue


            driver.close()
            output_to_widget('messages sent to friends with email {} \n\n'.format(t[0]))
        output_to_widget('Process complete!..\n\n')

    ttk.Button(top,text='Yes',command=message).grid(row=3,column=0)
    ttk.Button(top,text='No',command=top.destroy).grid(row=3,column=1)


def post_to_the_wall():

    if len(selected_accounts)==0:
        messagebox.showwarning('Error',"You must select a group with finite number of accounts.")
        return

    if box.get("1.0",'end-1c') == '':
        messagebox.showwarning('Error','You need to type something in the box to post on the wall. Its empty right now')
        return

    top = Toplevel(root)
    Label(top,text='').grid(row=0,columnspan=2)
    if len(selected_accounts) > 1:
        Label(top,text='    This command will post the message to the wall on all {} accounts of the selected group.     \n     Are you sure you want to continue?'.format(str(len(selected_accounts)))).grid(row=1,columnspan=2)
    else:
        Label(top,text='    This command will post the message to the wall on all accounts of the selected group.     \n     Are you sure you want to continue?').grid(row=1,columnspan=2)
    Label(top,text='').grid(row=2,columnspan=2)

    def post_wall():
        top.destroy()
        output_to_widget('Starting process....\n\n')
        for i in selected_accounts:
            driver = webdriver.PhantomJS()
            driver.get('http://facebook.com')


            emailElem = driver.find_element_by_id('email')
            emailElem.send_keys(i[0])
            passElem = driver.find_element_by_id('pass')
            passElem.send_keys(i[1])
            passElem.submit()

            driver.get('https://mbasic.facebook.com/')

            try:

                p = driver.find_element_by_css_selector('textarea')
                p.send_keys(box.get("1.0",'end-1c'))
                a= driver.find_element_by_css_selector('#mbasic_inline_feed_composer > form > table > tbody > tr > td.m > div > input')
                a.click()


                driver.close()
                output_to_widget('Posted on the wall on id with username :'+i[0]+' ...\n')
            except:
                output_to_widget('Unable to post on the wall on id with username :'+i[0]+' ...\n')
        output_to_widget('\nProcess Complete! \n')



    ttk.Button(top,text='Yes',command=post_wall).grid(row=3,column=0)
    ttk.Button(top,text='No',command=top.destroy).grid(row=3,column=1)



def accept_friend_requests():
    if len(selected_accounts)==0:
        messagebox.showwarning('Error',"Please select a group with finite number of accounts.")
        return

    top = Toplevel(root)
    Label(top,text='').grid(row=0,columnspan=2)
    if len(selected_accounts) > 1:
        Label(top,text='    This command will accept friend requests on all {} accounts of the selected group.     \n     Are you sure you want to continue?'.format(str(len(selected_accounts)))).grid(row=1,columnspan=2)
    else:
        Label(top,text='    This command will accept friend requests on all accounts of the selected group.     \n     Are you sure you want to continue?').grid(row=1,columnspan=2)
    Label(top,text='').grid(row=2,columnspan=2)

    def accept():
        top.destroy()
        output_to_widget('starting the process of accepting friend requests from all accounts ....\n')
        for t in selected_accounts:
            driver = webdriver.PhantomJS()
            driver.get('http://facebook.com')


            emailElem = driver.find_element_by_id('email')
            emailElem.send_keys(t[0])
            passElem = driver.find_element_by_id('pass')
            passElem.send_keys(t[1])
            passElem.submit()

            driver.get('https://www.facebook.com/friends/requests/')
            if driver.current_url != 'https://www.facebook.com/friends/requests/':
                output_to_widget('Unable to login on {}, incorrect password or something.. \n'.format(t[0]))
                continue
            try:
                nopf = driver.find_element_by_css_selector('#u_0_1o > h2:nth-child(1)')
                friendrequests = ''
                for i in nopf.text:
                    if i in '0123456789':
                        friendrequests+=i
            except:
                friendrequests=0
            try:
                friendrequests=int(friendrequests)
            except:
                friendrequests=0

            #print('friend requests : '+str(friendrequests))

            butts = driver.find_elements_by_tag_name('button')

            #print(len(butts))

            good_butts = []

            for i in butts:
                if 'Confirm' in i.text:
                    good_butts.append(i)

            #print(len(good_butts))

            for i in good_butts:
                i.click()


            #driver.get_screenshot_as_file('meow2.png') # the final state
            driver.close()
            output_to_widget('accepted {} pending friend requests in account with email {} ..\n'.format(str(len(good_butts)),t[0]))
        output_to_widget('\nProcess Complete! \n\n')


    ttk.Button(top,text='Yes',command=accept).grid(row=3,column=0)
    ttk.Button(top,text='No',command=top.destroy).grid(row=3,column=1)



def send_friend_requests():
    if len(selected_accounts)==0:
        messagebox.showwarning('Error',"Please select a group with finite number of accounts.")
        return
    top = Toplevel(root)
    Label(top,text='').grid(row=0,columnspan=2)
    if len(selected_accounts) > 1:
        Label(top,text='    This command will send friend requests to people you may know on all {} accounts of the selected group.     \n     Are you sure you want to continue?'.format(str(len(selected_accounts)))).grid(row=1,columnspan=2)
    else:
        Label(top,text='    This command will send friend requests to people you may know on all accounts of the selected group.     \n     Are you sure you want to continue?').grid(row=1,columnspan=2)
    Label(top,text='').grid(row=2,columnspan=2)

    def send():
        top.destroy()
        for t in selected_accounts:
            driver = webdriver.PhantomJS()
            driver.get('http://facebook.com')


            emailElem = driver.find_element_by_id('email')
            emailElem.send_keys(t[0])
            passElem = driver.find_element_by_id('pass')
            passElem.send_keys(t[1])
            passElem.submit()


            driver.get('https://www.facebook.com/friends/requests/')

            if driver.current_url != 'https://www.facebook.com/friends/requests/':
                output_to_widget('Unable to login on {}, incorrect password or something.. \n'.format(t[0]))
                continue

            butts = driver.find_elements_by_tag_name('button')

            good_butts = []

            for i in butts:
                if 'Add Friend' in i.text:
                    good_butts.append(i)


            for i in good_butts:
                i.click()

            driver.close()
            output_to_widget('sent {} friend requests to people you may know in account with email {} ..\n'.format(str(len(good_butts)),t[0]))
        output_to_widget('\nProcess Complete! \n\n')

    ttk.Button(top,text='Yes',command=send).grid(row=3,column=0)
    ttk.Button(top,text='No',command=top.destroy).grid(row=3,column=1)


def get_info():
    if len(selected_accounts)==0:
        messagebox.showwarning('Error',"Please select a group with finite number of accounts.")
        return
    top = Toplevel(root)
    Label(top,text='').grid(row=0,columnspan=2)
    if len(selected_accounts) > 1:
        Label(top,text='    This command will get information of all the {} accounts of the selected group from the internet and may take some time.     \n     Are you sure you want to continue?'.format(str(len(selected_accounts)))).grid(row=1,columnspan=2)
    else:
        Label(top,text='    This command will get information of all the accounts of the selected group from the internet and may take some time.    \n     Are you sure you want to continue?').grid(row=1,columnspan=2)
    Label(top,text='').grid(row=2,columnspan=2)

    def get():
        top.destroy()

        total_friends_request = 0
        total_friends = 0

        output_to_widget('Staring information retrieval ... \n\n')

        for t in selected_accounts:
            driver = webdriver.PhantomJS()
            driver.get('http://facebook.com')


            emailElem = driver.find_element_by_id('email')
            emailElem.send_keys(t[0])
            passElem = driver.find_element_by_id('pass')
            passElem.send_keys(t[1])
            passElem.submit()


            driver.get('http://facebook.com/me/friends')
            try:
                nof = driver.find_element_by_css_selector('._gs6')
                output_to_widget('id with email '+t[0]+' has friends = '+ str(nof.text)+'\n')
                total_friends+= int(nof.text)
            except:
                output_to_widget('Unable to login on {}, incorrect password or something.. \n\n'.format(t[0]))
                continue


            driver.get('https://www.facebook.com/friends/requests/')

            butts = driver.find_elements_by_tag_name('button')


            good_butts = []

            for i in butts:
                if 'Confirm' in i.text:
                    good_butts.append(i)
            total_friends_request += len(good_butts)
            output_to_widget('id with email '+t[0]+' has friends requests = '+str(len(good_butts))+'\n\n')

            driver.close()
        output_to_widget('all ids in the selected group {} has {} friends \n'.format(selected_group,str(total_friends)))
        output_to_widget('all ids in the selected group {} has {} friend requests \n\n'.format(selected_group,str(total_friends_request)))
        output_to_widget('process completed!!!\n\n')





    ttk.Button(top,text='Yes',command=get).grid(row=3,column=0)
    ttk.Button(top,text='No',command=top.destroy).grid(row=3,column=1)



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

        temp = []
        for i in selected_accounts:
            if i not in temp:
                temp.append(i)
        selected_accounts = temp
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
