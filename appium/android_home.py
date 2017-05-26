#! /usr/bin/env python3
import time
from appium import webdriver
from appium.webdriver.common.touch_action import TouchAction
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

class AndroidTestHome():

	def setup(self):
		desired_caps = {}
		desired_caps['platformName'] = 'Android'
		desired_caps['platformVersion'] = '7.1.1'
		desired_caps['deviceName'] = 'Nexus 6'
		desired_caps['appPackage'] = 'com.google.android.googlequicksearchbox'
		desired_caps['appActivity'] = 'com.google.android.launcher.GEL'
		self.driver = webdriver.Remote('http://127.0.0.1:4723/wd/hub', desired_caps)

	def notification_list(self):
		time.sleep(3)
		size = self.driver.get_window_size()
		print(size)
		self.driver.open_notifications()
		time.sleep(1)
		notification = self.driver.find_element_by_android_uiautomator('new UiSelector().text("Someone is detected in U1-01-02-0005 within Zone 1")')
		notification.click()
		time.sleep(4)
		action1 = TouchAction(self.driver)
		action1.press(x=720, y=800).move_to(x=0, y=1000).release().perform()
		time.sleep(1)
		action2 = TouchAction(self.driver)
		action2.press(x=720, y=800).move_to(x=0, y=-700).release().perform()

if __name__ == '__main__':
	launcher = AndroidTestHome()
	launcher.setup()
	launcher.notification_list()