#! /usr/bin/env python3
import os, sys, re, time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementNotVisibleException, NoSuchElementException

def usage():
	print('./ledchanger_2b.py <aqua_url> <browser> <led_behavior>')

def ledchanger():
	aqua, browser = sys.argv[1], sys.argv[2]
	email = os.environ['MY_LOGIN']
	pwd = os.environ['MY_PASSWORD']
	p = re.compile(r'https://.+?com/(\w)')

	if browser.lower() == 'firefox':
		driver = webdriver.Firefox()
	elif browser.lower() == 'chrome':
		driver = webdriver.Chrome()

	if aqua.lower() == 'rc':
		driver.get('http://aqua-rc.umbocv-inc.com')
	elif aqua.lower() == 'staging':
		driver.get('http://aqua.umbocv-inc.com')
	elif aqua.lower() == 'production':
		driver.get('http://aqua.umbocv.com')
	assert 'Umbo CV Portal' in driver.title

	elem_email = driver.find_element_by_name('email')
	elem_email.clear()
	elem_email.send_keys(email)
	elem_pwd = driver.find_element_by_name('password')
	elem_pwd.clear()
	elem_pwd.send_keys(pwd)
	elem_pwd.submit()
	WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//button[@ng-if="showToggleSidebar()"]')))
	assert 'dashboard' in driver.current_url

	if p.search(driver.current_url).group(1) == 's':
		elem_toggle_nav = driver.find_element_by_xpath('//button[@ng-if="showToggleSidebar()"]')
		elem_toggle_nav.click()

		while True:
			try:
				WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//li[@href="/s/customers"]')))
				elem_toggle_customer = driver.find_element_by_xpath('//li[@href="/s/customers"]')
				elem_toggle_customer.click()
				break
			except ElementNotVisibleException:
				continue
			
		while True:
			try:
				WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//li[contains(@class, "customer-item")][2]')))
				elem_toggle_c_item = driver.find_element_by_xpath('//li[contains(@class, "customer-item")][2]')
				elem_toggle_c_item.click()
				break
			except ElementNotVisibleException:
				continue

		while True:
			try:
				WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//md-tab-item[6]')))
				elem_toggle_settings1 = driver.find_element_by_xpath('//md-tab-item[6]')
				elem_toggle_settings1.click()
				break
			except ElementNotVisibleException:
				continue

		while True:
			try:
				WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//li[@ui-sref=".setting"]')))
				elem_toggle_settings2 = driver.find_element_by_xpath('//li[@ui-sref=".setting"]')
				elem_toggle_settings2.click()
				break
			except ElementNotVisibleException:
				continue

		while True:
			try:
				WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//li[span[contains(text(), "craven")]]')))
				elem_toggle_settings3 = driver.find_element_by_xpath('//li[span[contains(text(), "craven")]]')
				elem_toggle_settings3.click()
				break
			except ElementNotVisibleException:
				continue

		while True:
			try:
				WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//h4[contains(text(), "craven")]')))
				elem_toggle_settings4 = driver.find_element_by_xpath('//li[contains(@class, "light-option")][2]')
				elem_toggle_settings4.click()
				break
			except ElementNotVisibleException:
				continue

		while True:
			try:
				WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//button[@ng-click="c.save()"]')))
				elem_toggle_settings4 = driver.find_element_by_xpath('//button[@ng-click="c.save()"]')
				elem_toggle_settings4.click()
				break
			except ElementNotVisibleException:
				continue

	#elif p.search(driver.current_url).group(1) == 'c':

if __name__ == '__main__':
	ledchanger()

