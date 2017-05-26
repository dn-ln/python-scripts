#! /usr/bin/env python3
import time
from appium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

class AndroidTestRC():

	def setup(self):
		desired_caps = {}
		desired_caps['platformName'] = 'Android'
		desired_caps['platformVersion'] = '7.1.1'
		desired_caps['deviceName'] = 'Nexus 6'
		desired_caps['appPackage'] = 'com.umbocv.cphone.rc'
		desired_caps['appActivity'] = 'com.umbocv.cphone.SplashActivity'
		self.driver = webdriver.Remote('http://127.0.0.1:4723/wd/hub', desired_caps)

	def login(self):
		time.sleep(10)
		print(self.driver.current_context)
		print(self.driver.current_activity)
		# WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="@id/email"]')))
		email = self.driver.find_element_by_android_uiautomator('new UiSelector().resourceId("com.umbocv.cphone.rc:id/email")')
		email.clear()
		email.send_keys('')
		password = self.driver.find_element_by_android_uiautomator('new UiSelector().resourceId("com.umbocv.cphone.rc:id/password")')
		password.clear()
		password.send_keys('')
		login_button = self.driver.find_element_by_android_uiautomator('new UiSelector().resourceId("com.umbocv.cphone.rc:id/email_sign_in_button")')
		login_button.click()

if __name__ == '__main__':
	launcher = AndroidTestRC()
	launcher.setup()
	launcher.login()
