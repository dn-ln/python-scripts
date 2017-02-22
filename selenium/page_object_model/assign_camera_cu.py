#! /usr/bin/env python3
import os, sys, time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import ElementNotVisibleException, NoSuchElementException
from base_page import Base_Page

def usage():
	print('./assign_camera_cu.py <aqua url> <browser>')

class Assign_Camera_Cu(Base_Page):
	def sidebar(self):
		while True:
			try:
				WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//button[@ng-if="showToggleSidebar()"]')))
				elem_sidebar = self.driver.find_element_by_xpath('//button[@ng-if="showToggleSidebar()"]')
				elem_sidebar.click()
				break
			except (ElementNotVisibleException, NoSuchElementException) as e:
				continue

	def cam_list(self):		
		while True:
			try:
				WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//li[@href="/s/stock"]')))
				elem_cam_list = self.driver.find_element_by_xpath('//li[@href="/s/stock"]')
				elem_cam_list.click()
				break
			except (ElementNotVisibleException, NoSuchElementException) as e:
				continue

	def customer_list(self):		
		while True:
			try:
				WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//md-select[@md-on-close="c.onSelectCustomer($event)"]')))
				elem_cu_selection = self.driver.find_element_by_xpath('//md-select[@md-on-close="c.onSelectCustomer($event)"]')
				elem_cu_selection.click()
				print('1')
				time.sleep(2)
				break
			except (ElementNotVisibleException, NoSuchElementException) as e:
				continue

	def select_customer(self):
		while True:
			try:
				WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//md-option[@ng-repeat="item in c.customers"][3]')))
				elem_cu_selection = self.driver.find_element_by_xpath('//md-option[@ng-repeat="item in c.customers"][3]')
				elem_cu_selection.click() 
				time.sleep(1)
				print('2')
				break
			except (ElementNotVisibleException, NoSuchElementException) as e:
				continue

	def location_list(self):
		while True:
			try:
				WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//md-select[@md-on-close="c.onSelectLocation($event)"]')))
				elem_lo_selection = self.driver.find_element_by_xpath('//md-select[@md-on-close="c.onSelectLocation($event)"]')
				elem_lo_selection.click()
				print('3')
				time.sleep(1)
				break
			except (ElementNotVisibleException, NoSuchElementException) as e:
				continue

	def select_location(self):
		while True:
			try:
				WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//md-option[@ng-repeat="item in c.locations"][%d]' % i)))
				elem_cu_selection = self.driver.find_element_by_xpath('//md-option[@ng-repeat="item in c.locations"][%d]' % i)
				elem_cu_selection.click()
				print('4')
				break
			except (ElementNotVisibleException, NoSuchElementException) as e:
				continue

	def add_cam_to_list(self):
		while True:
			try:
				WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//button[@ng-click="c.addToList(cam)"][1]')))
				elem_cam_item = self.driver.find_element_by_xpath('//button[@ng-click="c.addToList(cam)"][1]')
				elem_cam_item.click()
				print('5')
				break
			except (ElementNotVisibleException, NoSuchElementException) as e:
				continue
		elem_cam_name = self.driver.find_element_by_xpath('//input[@ng-model="cam.name"]')
		elem_cam_name.send_keys(I)
		time.sleep(1)	

	def add_cam_to_location(self):
		while True:
			try:
				WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//button[@ng-click="c.addToLocation($event)"]')))
				elem_cam_item = self.driver.find_element_by_xpath('//button[@ng-click="c.addToLocation($event)"]')
				elem_cam_item.click()
				print('6')
				break
			except (ElementNotVisibleException, NoSuchElementException) as e:
				continue

	def add_cam_confirm(self):
		while True:
			try:
				WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//button[@ng-click="c.addCamera()"]')))
				elem_cam_add = self.driver.find_element_by_xpath('//button[@ng-click="c.addCamera()"]')
				elem_cam_add.click()
				print('7')
				break
			except (ElementNotVisibleException, NoSuchElementException) as e:
				continue

	def back_to_list(self):
		while True:
			try:
				WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//a[@ng-click="c.backToList()"]')))
				elem_cam_add = self.driver.find_element_by_xpath('//a[@ng-click="c.backToList()"]')
				elem_cam_add.click()
				print('8')
				time.sleep(2)
				break
			except (ElementNotVisibleException, NoSuchElementException) as e:
				continue	

	def run(self):
		self.setUp()
		self.get_aqua()
		self.login()
		self.sidebar()
		self.cam_list()
		self.customer_list()
		self.select_customer()
		for i in range(1, 29):
			self.location_list()
			self.select_location()
			for I in range(3):
				self.add_cam_to_list()
				self.add_cam_to_location()
				self.add_cam_confirm()
				self.back_to_list()

if __name__ == '__main__':
	launcher = Assign_Camera_Cu()
	launcher.run()







