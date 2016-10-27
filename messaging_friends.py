from selenium import webdriver
import time
from selenium.webdriver.common.keys import Keys

driver = webdriver.PhantomJS()
driver.get('http://facebook.com')

#logging in
emailElem = driver.find_element_by_id('email')
emailElem.send_keys('aradhyamakkar97@gmail.com')
passElem = driver.find_element_by_id('pass')
passElem.send_keys('wrongpassword')
passElem.submit()
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


driver.get_screenshot_as_file('meow.png') # to check if logged in or not


# getting number of friends in variable nof as integer and printing the number of friends
driver.get('http://facebook.com/me/friends')
nof = driver.find_element_by_css_selector('._gs6')
print('friends: '+nof.text)
nof = int(nof.text)
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~




#getting list of friends url in links ~~~~~~~~~~
driver.get('https://m.facebook.com/profile.php?v=friends')
nice_hyperlinks=[]

while len(nice_hyperlinks) <= nof-5:
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(1)

    print('tick')
    print(len(nice_hyperlinks))
    nice_hyperlinks = []

    hyperlinks = driver.find_elements_by_tag_name('a')
    for i in hyperlinks:
        if i.text !='' and i.text != 'Find Friends' and i.text != 'Active Friends' and i.text != 'Public' and i.text!= 'Only Me':
            nice_hyperlinks.append(i)

print('lenght of hypelinks : '+str(len(nice_hyperlinks)))

links = []
for i in nice_hyperlinks:
    links.append(    str( i.get_attribute('href'))[0:8] +   str(i.get_attribute('href'))[10:]  )


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



# sending message to friends~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
message = 'hello,!!!' # this will be sent, get this l8r from gui ;)

for i in links:

    message_link = (i)[0:21]+'messages/'+(i)[21:]
    print(message_link)
    driver.get(message_link)

    try:
        box = driver.find_element_by_css_selector('textarea')

        box.send_keys(message)

        send_buttonsssss = driver.find_elements_by_tag_name('input')

        new = ''
        for j in send_buttonsssss:
            if j.get_attribute('value') == 'Send' or j.get_attribute('value') == 'Reply':
                new = j
                new.click()
                break
    except:
        continue













#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


driver.get_screenshot_as_file('meow2.png') # the final state
driver.close()
