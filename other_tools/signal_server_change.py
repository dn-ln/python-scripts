#! /usr/bin/env python3
from pymongo import MongoClient
import re, os, sys, paramiko, subprocess

class Signal_Server_Change():
	def __init__(self):
		self.usr = os.environ['CAMUSERID']
		self.pwd = os.environ['CAMPASSWORD']
		self.server_replaced, self.server_to_replace, self.camera_names = sys.argv[1], sys.argv[2], sys.argv[3:]	

	def usage():
		print('./signal_server_change.py <camera address> <rc|staging|production> <rc|staging|production>')

	def get_cam_ip(self):
		if self.server_replaced.lower() == 'rc':
			mc = MongoClient('url') 
		elif self.server_replaced.lower() == 'staging':
			mc = MongoClient('url')	
		db = mc['hippo-staging']
		db_collection_cameras = db['cameras']
		self.ip_list = []
		for camera_name in self.camera_names:
			camera_mac_string = db_collection_cameras.find_one({"name": {"$regex": "{}".format(camera_name)}})['mac']
			camera_mac_address = ':'.join(format(s, '02x') for s in bytes.fromhex(camera_mac_string))
			arp_scan = subprocess.Popen('echo $SUDOPWD | sudo -S arp-scan --interface=eth0 -l | grep {}'.format(camera_mac_address), stdout=subprocess.PIPE, shell=True)
			arp_scan_decode = arp_scan.stdout.read().decode()
			ip_pattern = re.compile(r'192.168.2.\d+')
			ip = ip_pattern.search(arp_scan_decode).group(0)
			self.ip_list.append(ip)	

	def new_ssh_session(self, address):
		c = paramiko.SSHClient()
		c.load_system_host_keys()
		try:
			print('Connecting to the camera...')
			c.connect(address, username=self.usr, password=self.pwd)
		except paramiko.SSHException:
			print('Adding unknown host key...')
			c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
			c.connect(address, username=self.usr, password=self.pwd)
		print('Camera connected.')
		return c	

	def replace_text(self, c):
		if self.server_replaced.lower() == 'rc':
			stdin, stdout, stderr = c.exec_command('grep -q "silk-rc" "config_file_path" && echo found')
			grep_result = stdout.read().decode().rstrip()
			if grep_result == 'found':
				if self.server_to_replace.lower() == 'staging':
					c.exec_command('sed -i -- "s/silk-rc/silk-staging/g" config_file_path')
					c.exec_command('PATH=$PATH:/usr/sbin; restart_command')
					print('Change from RC to Staging.')
				elif self.server_to_replace.lower() == 'production':
					c.exec_command('sed -i -- "s/silk-rc/silk/g" config_file_path')
					c.exec_command('PATH=$PATH:/usr/sbin; restart_command'')
					print('Change from RC to Production.')
			else:
				print('It is not on RC.')
		elif self.server_replaced.lower() == 'staging':
			stdin, stdout, stderr = c.exec_command('grep -q "silk-staging" "config_file_path" && echo found')
			grep_result = stdout.read().decode().rstrip()
			if grep_result == 'found':
				if self.server_to_replace.lower() == 'rc':
					c.exec_command('sed -i -- "s/silk-staging/silk-rc/g" config_file_path')
					c.exec_command('PATH=$PATH:/usr/sbin; restart_command')
					print('Change from Staging to RC.')
				elif self.server_to_replace.lower() == 'production':
					c.exec_command('sed -i -- "s/silk-rc/silk/g" config_file_path')
					c.exec_command('PATH=$PATH:/usr/sbin; restart_command')
					print('Change from Staging to Production.')
			else:
				print('It is not on Staging.')	
		elif self.server_replaced.lower() == 'production':
			stdin, stdout, stderr = c.exec_command('grep -q "silk-production" "/etc/umbo/config.ini" && echo found')
			grep_result = stdout.read().decode().rstrip()
			if grep_result == 'found':
				if self.server_to_replace.lower() == 'rc':
					c.exec_command('sed -i -- "s/silk-staging/silk-rc/g" config_file_path')
					c.exec_command('PATH=$PATH:/usr/sbin; restart_command')
					print('Change from Production to RC.')
				elif self.server_to_replace.lower() == 'staging':
					c.exec_command('sed -i -- "s/silk-rc/silk-staging/g" config_file_path')
					c.exec_command('PATH=$PATH:/usr/sbin; restart_command')
					print('Change from Production to Staging.')
			else:
				print('It is not on Production.')
		else:
			self.usage()

	def run(self):
		try:
			self.get_cam_ip()
			for address in self.ip_list:
				client = self.new_ssh_session(address)
				self.replace_text(client)
		except IndexError:
			self.usage()

if __name__ == '__main__':
	launcher = Signal_Server_Change()
	launcher.run()


