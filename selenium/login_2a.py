#! /usr/bin/env python3
from os import environ
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

driver = webdriver.Firefox()
driver.get('url')
assert 'keyword' in driver.title

# Login In
email = environ['USER']
password = environ['PASSWORD']
elem_email = driver.find_element_by_name('email')
elem_email.clear()
elem_email.send_keys(email)
elem_password = driver.find_element_by_name('password')
elem_password.clear()
elem_password.send_keys(password)
elem_password.submit()
driver.close()
