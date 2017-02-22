import os, sys, re, time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import ElementNotVisibleException, NoSuchElementException
from selenium.webdriver.common.keys import Keys

class Base_Page():
	def __init__(self):
		self.aqua = sys.argv[1]
		self.browser = sys.argv[2]
		self.email = os.environ['MY_LOGIN']
		self.pwd = os.environ['MY_PASSWORD']
		if self.browser.lower() == 'firefox':
			self.driver = webdriver.Firefox()
		elif self.browser.lower() == 'chrome':
			self.driver = webdriver.Chrome()

	def get_aqua(self):
		if self.aqua.lower() == 'rc':
			self.driver.get('url')
		elif self.aqua.lower() == 'staging':
			self.driver.get('url')
		assert 'Umbo CV Portal' in self.driver.title

	def login(self):
		elem_email = self.driver.find_element_by_name('email')
		elem_email.clear()
		elem_email.send_keys(self.email)
		elem_pwd = self.driver.find_element_by_name('password')
		elem_pwd.clear()
		elem_pwd.send_keys(self.pwd)
		elem_pwd.submit()
		WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//button[@ng-if="showToggleSidebar()"]')))
		assert 'dashboard' in self.driver.current_url