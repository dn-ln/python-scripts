#! /usr/bin/env python3
import os, time, argparse, subprocess
from datetime import datetime

class Wifi_Change():
	def __init__(self):
		self.wifi_ssid = ['RUMBO25', 'RUMBO3', 'Umbo_router_3']
		self.wifi_pwd = [os.environ['WIFI_PWD'], os.environ['ZTE_PWD']]

	def argument(self):
		parser = argparse.ArgumentParser(description='Change your Wi-Fi.')
		parser.add_argument('-t', '--time', nargs='*', help='Enter your start time and interval.')
		parser.add_argument('-s', '--sequence', help='Enter your Wi-Fi sequence.')
		self.args = vars(parser.parse_args()) 	

	def nmcli_connect(self, i):
		ssid = self.wifi_ssid[i]
		if 'RUMBO' in ssid:
			pwd = self.wifi_pwd[0]
		else:
			pwd = self.wifi_pwd[1]
		subprocess.Popen('nmcli d wifi connect {} password {} iface wlan0'.format(ssid, pwd), stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT, shell=True)	

	def start_traffic(self):
		if len(self.args['time']) == 1:
			interval = int(self.args['time'][0])
			sequence = self.args['sequence']
			start_time = datetime.now().timestamp()
			for i in sequence[:-1]:
				self.nmcli_connect(int(i))
				print('Executed at: ', datetime.now())
				now = datetime.now().timestamp()
				time.sleep(start_time + interval - now)
				start_time += interval
			self.nmcli_connect(int(sequence[-1]))
			print('Last executed at: ', datetime.now())	

		elif len(self.args['time']) == 2:
			interval = int(self.args['time'][0])
			sequence = self.args['sequence']
			hour, minute = int(self.args['time'][1][0:2]), int(self.args['time'][1][2:4])
			start_time = datetime.now().replace(hour=hour, minute=minute, second=0).timestamp()
			for i in sequence:
				now = datetime.now().timestamp()
				if start_time >= now:
					time.sleep(start_time - now)
					self.nmcli_connect(int(i))
					print('Executed at: ', datetime.now())
					start_time += interval
				else:
					print('The time has passed.')
					start_time += interval
			
if __name__ == '__main__':
	lanucher = Wifi_Change()
	lanucher.argument()
	lanucher.start_traffic()