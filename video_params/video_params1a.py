#! /usr/bin/env python3
from os import environ
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Firefox()
driver.get('http://aqua-rc.umbocv-inc.com')
assert 'Umbo CV Portal' in driver.title

email = environ['MY_LOGIN']
password = environ['MY_PASSWORD']
elem_email = driver.find_element_by_name('email')
elem_email.clear()
elem_email.send_keys(email)
elem_password = driver.find_element_by_name('password')
elem_password.clear()
elem_password.send_keys(password)
elem_password.submit()
wait = WebDriverWait(driver, 10)
element = wait.until(EC.element_to_be_clickable(By.LINK_TEXT("customer")))
elem_customer.click()
