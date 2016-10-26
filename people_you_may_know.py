from selenium import webdriver
import time
from selenium.webdriver.common.keys import Keys

driver = webdriver.PhantomJS()
driver.get('http://facebook.com')


emailElem = driver.find_element_by_id('email')
emailElem.send_keys('fakeemail1729@gmail.com')
passElem = driver.find_element_by_id('pass')
passElem.send_keys('wrongpassword')
passElem.submit()


driver.get_screenshot_as_file('meow.png') # to check if logged in or not

driver.get('https://www.facebook.com/friends/requests/')





butts = driver.find_elements_by_tag_name('button')

print(len(butts))

good_butts = []

for i in butts:
    if 'Add Friend' in i.text:
        good_butts.append(i)

print(len(good_butts))

for i in good_butts:
    i.click()


driver.get_screenshot_as_file('meow2.png') # the final state
driver.close()
