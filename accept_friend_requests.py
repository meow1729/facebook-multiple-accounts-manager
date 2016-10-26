from selenium import webdriver
import time

driver = webdriver.PhantomJS()
driver.get('http://facebook.com')


emailElem = driver.find_element_by_id('email')
emailElem.send_keys('aradhyamakkar97@gmail.com')
passElem = driver.find_element_by_id('pass')
passElem.send_keys('wrongpassword')
passElem.submit()


driver.get_screenshot_as_file('meow.png') # to check if logged in or not

driver.get('https://www.facebook.com/friends/requests/')
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

print('friend requests : '+str(friendrequests))

butts = driver.find_elements_by_tag_name('button')

print(len(butts))

good_butts = []

for i in butts:
    if 'Confirm' in i.text:
        good_butts.append(i)

print(len(good_butts))

for i in good_butts:
    i.click()


driver.get_screenshot_as_file('meow2.png') # the final state
driver.close()
