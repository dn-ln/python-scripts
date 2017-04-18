#! /usr/bin/env python3
import os, sys, csv, time, subprocess
from datetime import datetime
import paramiko
from paramiko.ssh_exception import SSHException, NoValidConnectionsError, BadHostKeyException

class TCP_Poller():
	def __init__(self):
		self.address = sys.argv[1]
		self.interval = int(sys.argv[2])
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
				c.connect(self.address, username=self.usr, password=self.pwd)
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

	def watch_tcp(self):
		c = self.new_ssh_client()
		if c:
			print('Watching on TCP connection...')
			stdin, stdout, stderr = c.exec_command('netstat -nt')
			config_file = stdout.readlines()
			connections = []
			for row in config_file[2:]:
				connection = row.split()
				connections.append('Host: {} Foreign: {}'.format(connection[3], connection[4]))
			end_time = datetime.now().timestamp() + self.interval
			while True:
				now = datetime.now().timestamp()
				now_str = datetime.fromtimestamp(now)
				if end_time - now >= 0:
					time.sleep(end_time - now)
				else:
					time.sleep(self.interval)
				stdin, stdout, stderr = c.exec_command('netstat -nt')
				config_file_updated = stdout.readlines()
				connections_updated = []
				for row in config_file_updated[2:]:
					connection_updated = row.split()
					connections_updated.append('Host: {} Foreign: {}'.format(connection_updated[3], connection_updated[4]))
				if connections != connections_updated:
					set1, set2 = set(connections), set(connections_updated)
					if list(set1 - set2):
						print(datetime.now(), '|', 'Disconnect:\n' + '\n'.join(list(set1 - set2)))
					elif list(set2 - set1):
						print(datetime.now(), '|', 'Newly Connected:\n' + '\n'.join(list(set2 - set1)))
					connections = connections_updated
				end_time += self.interval

if __name__ == '__main__':
	launcher = TCP_Poller()
	launcher.watch_tcp()

			
