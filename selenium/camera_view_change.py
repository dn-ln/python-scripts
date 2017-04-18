#! /usr/bin/env python3
import os, time, argparse
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import StaleElementReferenceException
import pymongo

class Camera_View_Change():
	def __init__(self):
		self.aqua_url = os.environ['AQUA_URL_RC']
		self.email = os.environ['CUMA_STAGING']
		self.pwd = os.environ['CUMA_STAGING_PWD']

	def argument(self):
		parser = argparse.ArgumentParser(description='Change camera views by dragging them.')
		parser.add_argument('-b', '--browser', required=True)
		self.args = vars(parser.parse_args())

	#def get_camera_name(self):

	def setup(self):
		if self.args['browser'].lower() == 'chrome':
			self.driver = webdriver.Chrome()
		elif self.args['browser'].lower() == 'firefox':
			self.driver = webdriver.Firefox()
		self.action = ActionChains(self.driver)

	def login(self):
		self.driver.get(self.aqua_url)
		self.driver.maximize_window()
		email_input = self.driver.find_element_by_name('email')
		pwd_input = self.driver.find_element_by_name('password')
		email_input.clear()
		email_input.send_keys(self.email)
		pwd_input.clear()
		pwd_input.send_keys(self.pwd)
		pwd_input.submit()

	def drag_in_camera(self):
		WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//form[@ng-submit="update()"]/span[text()="taipei"]')))
		taipei_camera_list = self.driver.find_element_by_xpath('//form[@ng-submit="update()"]/span[text()="taipei"]')
		taipei_camera_list.click()
		WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//ul[@ng-model="location.cameras"]/li[@ng-repeat="item in location.cameras track by item._id"][3]')))
		cam_0880 = self.driver.find_element_by_xpath('//ul[@ng-model="location.cameras"]/li[@ng-repeat="item in location.cameras track by item._id"][3]')

		self.action.click_and_hold(on_element=cam_0880).perform()
		time.sleep(0.1)
		self.action.move_by_offset(-100, -100).perform()
		self.action.move_by_offset(-100, -100).perform()
		self.action.move_by_offset(-100, 0).perform()
		self.action.release().perform()

	def drag_out_camera(self):
		time.sleep(10)
		WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//li[@ng-dblclick="viewportEnlarge(item)"][1]')))
		cam_0880_stream = self.driver.find_element_by_xpath('//li[@ng-dblclick="viewportEnlarge(item)"][1]')
		try:
			self.action.click_and_hold(on_element=cam_0880_stream).perform()
		except StaleElementReferenceException:
			WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//li[@ng-dblclick="viewportEnlarge(item)"][1]')))
			cam_0880_stream = self.driver.find_element_by_xpath('//li[@ng-dblclick="viewportEnlarge(item)"][1]')
			self.action.click_and_hold(on_element=cam_0880_stream).perform()
		time.sleep(5)
		self.action.move_by_offset(100, 100).perform()
		print('action2')
		time.sleep(5)
		self.action.move_by_offset(100, 100).perform()
		print('action3')
		time.sleep(5)
		self.action.move_by_offset(100, 0).perform()
		print('action4')
		time.sleep(5)

if __name__ == '__main__':
	launcher = Camera_View_Change()
	launcher.argument()
	launcher.setup()
	launcher.login()
	launcher.drag_in_camera()
	launcher.drag_out_camera()