#! /usr/bin/env python3
import os, sys, subprocess
import paramiko

class Match_Firmware():
	def __init__(self):
		self.usr = os.environ['CAMUSERID']
		self.pwd = os.environ['CAMPASSWORD']
		self.config_path = os.environ['CONFIG_INI']
		self.address_list = sys.argv[1:]	

	def ssh_to_camera(self, address):
		c = paramiko.SSHClient()
		c.load_system_host_keys()
		try:
			print('Connecting to camera...')
			c.connect(address, username=self.usr, password=self.pwd)
		except paramiko.SSHException:
			try:
				print('Add system host key.')
				c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
				c.connect(address, username=self.usr, password=self.pwd)
			except paramiko.BadHostKeyException:
				print('Fix unmatch host key.')
				subprocess.Popen('ssh-keygen -R {}'.format(self.address), shell=True)
				c.connect()
		print('Camera connected.')
		return c	

	def guava_match(self, address):
		c = self.ssh_to_camera(address)
		stdin, stdout, stderr = c.exec_command('cat {} | grep guava256'.format(self.config_path))
		guava_256 = stdout.read().decode('utf-8')
		if guava_256:
			print(address, 'guava256')
		else:
			print(address, 'guava')

	def run(self):
		for address in self.address_list:
			self.guava_match(address)

if __name__ == '__main__':
	launcher = Match_Firmware()
	launcher.run()


