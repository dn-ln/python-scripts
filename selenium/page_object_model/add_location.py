#! /usr/bin/env python3
import os, sys, re, time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import ElementNotVisibleException, NoSuchElementException
from selenium.webdriver.common.keys import Keys
from base_page import Base_Page

def usage():
	print('./add_location.py <aqua url> <browser>')

class Add_Location(Base_Page):
	def sidebar(self):
		while True:
			try:
				WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//button[@ng-if="showToggleSidebar()"]')))
				elem_sidebar = self.driver.find_element_by_xpath('//button[@ng-if="showToggleSidebar()"]')
				elem_sidebar.click()
				break
			except (ElementNotVisibleException, NoSuchElementException) as e:
				continue

	def customer_list(self):
		while True:
			try:
				WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//li[@href="/s/customers"]')))
				customers_list = self.driver.find_element_by_xpath('//li[@href="/s/customers"]')
				customers_list.click()
				break
			except (ElementNotVisibleException, NoSuchElementException) as e:
				continue

	def customer_item(self):
		while True:
			try:
				WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//li[contains(@class, "customer-item")][4]')))
				customers_item = self.driver.find_element_by_xpath('//li[contains(@class, "customer-item")][4]')
				customers_item.click()
				break
			except (ElementNotVisibleException, NoSuchElementException) as e:
				continue

	def location_list(self):
		while True:
			try:
				WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//md-tab-item[4]')))
				locations_list = self.driver.find_element_by_xpath('//md-tab-item[4]')
				locations_list.click()
				break
			except (ElementNotVisibleException, NoSuchElementException) as e:
				continue

	def create_location(self):
		while True:
			try:
				WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//button[@ng-click="createLocation($event)"]')))
				create_button = self.driver.find_element_by_xpath('//button[@ng-click="createLocation($event)"]')
				create_button.click()
				time.sleep(2.5)
				break
			except (ElementNotVisibleException, NoSuchElementException) as e:
				continue

	def location_name(self, character):
		while True:
			try:
				WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//div[@aria-hidden="true"]')))
				elem_place = self.driver.find_element_by_xpath('//input[@ng-model="c.newLocation.name"]')
				elem_place.clear()
				elem_place.send_keys(character)
				break
			except (ElementNotVisibleException, NoSuchElementException) as e:
				continue

	def location_address(self):
		elem_address = self.driver.find_element_by_xpath('//input[@ng-model="c.place"]')
		elem_address.clear()
		elem_address.send_keys('neihu')
		time.sleep(2.5)
		WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//div[@ng-click="selectPrediction($index)"]')))
		elem_address.send_keys(Keys.ENTER)

	def location_create(self, character):
		elem_create = self.driver.find_element_by_xpath('//button[contains(@class, "btn-aqua-primary")]')
		elem_create.send_keys(Keys.ENTER)
		WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//span[contains(@class, "location-item-name") and contains(text(), "{}")]'.format(character))))
		time.sleep(1)
	
	def location_create2(self):
		while True:
			try:
				WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//button[@ng-click="createLocation($event)"]')))
				customers = self.driver.find_element_by_xpath('//button[@ng-click="createLocation($event)"]')
				customers.click()
				break
			except (ElementNotVisibleException, NoSuchElementException) as e:
				continue

	def run(self):
		self.get_aqua()
		self.login()
		self.sidebar()
		self.customer_list()
		self.customer_item()
		self.location_list()
		weird_characters = 'abcdefg'
		for character in weird_characters:
			self.create_location()
			self.location_name(character)
			self.location_address()
			self.location_create(character)

if __name__ == '__main__':
	launcher = Add_Location()
	launcher.run()