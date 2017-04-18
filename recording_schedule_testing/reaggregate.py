#! /usr/bin/env python3
import re, os, sys, subprocess
import paramiko

class Reaggregate():
	def __init__(self):
		self.usr = os.environ['CAMUSERID']
		self.pwd = os.environ['CAMPASSWORD']
		self.mnt_path = os.environ['MNT_SDCARD']
		self.address = sys.argv[1]	

	def ssh_to_camera(self):
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
				print('Unmatched host key.')
				subprocess.Popen('ssh-keygen -R 192.168.2.118', shell=True)
				c.connect(address, username=self.usr, password=self.pwd)
		print('Camera connected.')
		return c	

	def aggregate(self):
		c = self.ssh_to_camera()
		datetime_range = sys.argv[2]
		stdin, stdout, stderr = c.exec_command('find {} -name 2017{}*.mp4 | xargs ls -l'.format(self.mnt_path, datetime_range))
		mp4_list = stdout.read().decode('utf-8')
		p = re.compile(r'\s(\d+?)\s\w{3}\s')
		size_list_str = p.findall(mp4_list)
		size_list = list(map(int, size_list_str))
		print('The total size is:', sum(size_list), 'bytes')

if __name__ == '__main__':
	launcher = Reaggregate()
	launcher.aggregate()