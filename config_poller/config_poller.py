#! /usr/bin/env python3
import os, sys, time, subprocess
from datetime import datetime
import paramiko
from paramiko.ssh_exception import SSHException, NoValidConnectionsError, BadHostKeyException

class Config_Poller():
	def __init__(self):
		self.address = sys.argv[1]
		self.usr = os.environ['CAMUSERID']
		self.pwd = os.environ['CAMPASSWORD']
		self.config_path = os.environ['CONFIG_INI']

	def new_ssh_client(self):
		c = paramiko.SSHClient()
		print('Camera connecting...')
		try:
			print('Load system host keys...')
			c.load_system_host_keys()
			c.connect(self.address, username=self.usr, password=self.pwd)
			print('Camera connected.')
			return c
		except SSHException:
			try:
				print('Add missing host key...')
				c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
				c.connect(self.address, username=self.usr, password=self.pwd,)
				print('Camera connected.')
				return c
			except BadHostKeyException:
				print('Delete unmatched host key and generate a new key...')
				subprocess.Popen('ssh-keygen -R {}'.format(self.address), shell=True)
				c.connect(self.address, username=self.usr, password=self.pwd)
				print('Camera connected.')
				return c
		except NoValidConnectionsError:
			print('Camera is offline.')
			return 0	

	def watch_config(self):
		end_time = datetime.now().timestamp() + 30
		c = self.new_ssh_client()
		if c:
			stdin, stdout, stderr = c.exec_command('cat {}'.format(self.config_path))
			config_file = stdout.readlines()
			print('Watching config file...')
			while True:
				now = datetime.now().timestamp()
				now_str = datetime.fromtimestamp(now)
				time.sleep(end_time - now)
				stdin, stdout, stderr = c.exec_command('cat {}'.format(self.config_path))
				config_file_updated = stdout.readlines()
				if config_file != config_file_updated:
					for i in range(len(config_file_updated)):
						if config_file_updated[i] != config_file[i]:
							print(datetime.now(), '{} => {}'.format(config_file[i].rstrip(), config_file_updated[i].rstrip()))
				else:
					print(datetime.now(), 'No change in config file.')
				config_file = config_file_updated
				end_time += 30

if __name__ == '__main__':
	launcher = Config_Poller()
	launcher.watch_config()

			
