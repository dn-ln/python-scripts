#! /usr/bin/env python3
import os, sys, time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

# Create traffic from starting time, interval, and steps(increasing or decreasing value of exposure)
def traffic(function):
	def wrapper(self, all_steps):
		points = [self.start_time]
		all_steps = self.all_steps
		for interval in self.intervals:
			points.append(self.start_time + int(interval, 16))
			self.start_time += int(interval, 16)
		for point, steps in zip(points, all_steps): 
			now = datetime.now().timestamp() 
			if point >= now:
				time.sleep(point - now)
				function(self, steps)
			else:
				print('The time has passed:', datetime.fromtimestamp(point))
	return wrapper

# Main part
class Exposure_Toggler():

	def __init__(self):
		self.email = os.environ['DN_SI_MA_RC']
		self.pwd = os.environ['DN_SI_MA_RC_PWD']
		self.aqua_rc = os.environ['AQUA_URL_RC']
		self.aqua_staging = os.environ['AQUA_URL_STAGING']
		self.browser = sys.argv[1]
		self.server = sys.argv[2]
		self.start_time = datetime.now().replace(hour=int(sys.argv[3][0:2]), minute=int(sys.argv[3][2:4]), second=int(sys.argv[3][4:6]), microsecond=0).timestamp()
		self.intervals = list(sys.argv[4])
		self.all_steps = [sys.argv[5][i:i+2] for i in range(0, len(sys.argv[5]), 2)]

	def setup(self):
		# Choose browser
		if self.browser.lower() == 'firefox':
			self.driver = webdriver.Firefox()
		elif self.browser.lower() == 'chrome':
			self.driver = webdriver.Chrome()
		# Choose aqua server
		if self.server.lower() == 'rc':
			self.driver.get(self.aqua_rc)
		elif self.server.lower() == 'staging':
			self.driver.get(self.aqua_staging)
		# Maximize the window
		self.driver.maximize_window()

	def login(self):
		# Find email input and send account email
		input_email = self.driver.find_element_by_name('email')
		input_email.clear()
		input_email.send_keys(self.email)
		# Find password input and send password
		input_pwd = self.driver.find_element_by_name('password')
		input_pwd.clear()
		input_pwd.send_keys(self.pwd)
		# Submit to login
		input_pwd.submit()
		WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//li[@ng-repeat="customer in customers | filter: search.keyword"][1]')))

	def go_to_property_page(self):
		# Choose the customer
		slowtime_player = self.driver.find_element_by_xpath('//li[@ng-repeat="customer in customers | filter: search.keyword"][1]')
		slowtime_player.click()
		WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//md-tab-item[6]')))
		# Go to Settings page
		settings_tab = self.driver.find_element_by_xpath('//md-tab-item[6]')
		settings_tab.click()
		WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//tr[@ng-repeat="item in c.display track by $index"][7]')))
		# Hover on the camera row to make button visible
		camera_table_row = self.driver.find_element_by_xpath('//tr[@ng-repeat="item in c.display track by $index"][7]')
		actions = ActionChains(self.driver)
		actions.move_to_element(camera_table_row)
		actions.perform()
		WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.XPATH, '(//span[@ng-click="c.editProperty($event, item)"])[7]')))
		# Open the property menu
		property_button = self.driver.find_element_by_xpath('(//span[@ng-click="c.editProperty($event, item)"])[7]')
		property_button.click()
		WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//div[@class="md-dialog-container ng-scope"]')))

	def go_to_image_property(self):
		# Go to Image Properties
		image_property_button = self.driver.find_element_by_xpath('(//button[@ng-click="c.setContent(item.state)"])[2]')
		image_property_button.click()
		WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//md-radio-button[@aria-label="exposure settings manual"]')))
		# Set Exposure to manual
		manual_button = self.driver.find_element_by_xpath('//md-radio-button[@aria-label="exposure settings manual"]')
		manual_button.click()
		WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//span[@ng-click="c.step(1)"]')))			

	@traffic
	def change_exposure(self, steps):
		# Find increase and decrease button
		exposure_plus_step = self.driver.find_element_by_xpath('//span[@ng-click="c.step(1)"]')
		exposure_minus_step = self.driver.find_element_by_xpath('//span[@ng-click="c.step(-1)"]')
		# Increase or decrease exposure according to the steps
		if int(steps) >= 0: 
			for step in range(int(steps)):
				exposure_plus_step.click()
		else:
			for step in range(abs(int(steps))):
				exposure_minus_step.click()

	def run(self):
		self.setup()
		self.login()
		self.go_to_property_page()
		self.go_to_image_property()
		self.change_exposure(self.all_steps)

if __name__ == '__main__':
	launcher = Exposure_Toggler()
	launcher.run()