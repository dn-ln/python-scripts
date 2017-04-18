#! /usr/bin/env python3
import os, re, sys, json
import urllib.request, urllib.parse

class Set_Password():
	def __init__(self):
		self.auth_server_rc = os.environ['AQUA_URL_RC']
		self.auth_server_stag = os.environ['AQUA_URL_STAGING']
		self.api_server_rc = os.environ['API_SERVER_RC']
		self.api_server_stag = os.environ['API_SERVER_STAGING']
		self.ma_pwd_curr = os.environ['CURRENT_MASTER_PASS']
		self.ma_pwd_new = os.environ['NEW_MASTER_PASS']
		self.input = open(sys.argv[1]).read().splitlines()
		self.server = sys.argv[2]

	def read_input(self):
		self.list = []
		for account in self.input:
			item = account.split()
			if len(item) == 3:
				self.list.append(item)
			else:
				print('Password contains space characters.')

	def get_token(self):
		for item in list(self.list):
			if item[1] != item[2] or self.ma_pwd_new:
				email = item[0]
				oldPassword = item[1] + self.ma_pwd_curr
				data = json.dumps({"email": email, "password": oldPassword}).encode('ascii')
				if self.server == 'rc':
					req = urllib.request.Request('{}/auth/local'.format(self.auth_server_rc), data=data, method='POST')
				elif self.server == 'staging':
					req = urllib.request.Request('{}/auth/local'.format(self.auth_server_stag), data=data, method='POST')
				req.add_header('User-Agent', 'Mozilla/5.0')
				req.add_header('Content-Type', 'application/json')
				try:
					res_raw = urllib.request.urlopen(req)
					res = res_raw.read().decode('utf-8')
					res_json = json.loads(res)
					item.append(res_json['token'])
				except urllib.error.HTTPError as e:
					message = e.read().decode('utf-8')
					message_json = json.loads(message)
					print('{}: {}'.format(item[0], message_json['message']))
					self.list.remove(item)
			else:
				print('{}: The new password is the same as the old one.'.format(item[0]))
				self.list.remove(item)

	def get_id(self):
		if self.list:
			for item in self.list:
				if self.server == 'rc':
					req = urllib.request.Request('{}/users/me'.format(self.api_server_rc))
				elif self.server == 'staging':
					req = urllib.request.Request('{}/users/me'.format(self.api_server_stag))
				req.add_header('User-Agent', 'Mozilla/5.0')
				req.add_header('Content-Type', 'application/json')
				req.add_header('Authorization', 'Bearer {}'.format(item[3]))
				res_raw = urllib.request.urlopen(req)
				res = res_raw.read().decode('utf-8')
				res_json = json.loads(res)
				item.append(res_json['_id'])

	def change_password(self):
		if self.list:
			for item in self.list:
				if self.ma_pwd_new:
					data = json.dumps({"oldPassword": item[1] + self.ma_pwd_curr, "newPassword": item[2] + self.ma_pwd_new}).encode('ascii')
					with open('/home/deanlin/.bashrc', 'r') as file:
						f = file.read()
						f = re.sub(r'CURRENT_MASTER_PASS=".+?"', r'CURRENT_MASTER_PASS="{}"'.format(self.ma_pwd_new), f)
						f = re.sub(r'NEW_MASTER_PASS=".+?"', r'NEW_MASTER_PASS=""', f)
					with open('/home/deanlin/.bashrc', 'w') as file:
						file.write(f)
				else:
					data = json.dumps({"oldPassword": item[1] + self.ma_pwd_curr, "newPassword": item[2] + self.ma_pwd_curr}).encode('ascii')
				if self.server == 'rc':
					req = urllib.request.Request('{}/users/{}/password'.format(self.api_server_rc, item[4]), data=data, method='PUT')
				elif self.server == 'staging':
					req = urllib.request.Request('{}/users/{}/password'.format(self.api_server_stag, item[4]), data=data, method='PUT')
				req.add_header('User-Agent', 'Mozilla/5.0')
				req.add_header('Content-Type', 'application/json')
				req.add_header('Authorization', 'Bearer {}'.format(item[3]))
				try:
					res_raw = urllib.request.urlopen(req)
					res = res_raw.read().decode('utf-8')
					print('{}: Password is changed successfully.'.format(item[0]))
				except urllib.error.HTTPError as e:
					message = e.read().decode('utf-8')
					message_json = json.loads(message)
					print('{}: {}'.format(item[0], message_json['msg']))
			print('Please restart your shell session to update master password.')

	def run(self):
		self.read_input()
		self.get_token()
		if self.list:
			self.get_id()
			self.change_password()

if __name__ == '__main__':
	launcher = Set_Password()
	launcher.run()

