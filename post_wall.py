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


p = driver.find_element_by_css_selector('.uiTextareaAutogrow')
p.send_keys('wow I am a a fucking genius')
p.submit()




driver.get_screenshot_as_file('meow2.png') # the final state
driver.close()
