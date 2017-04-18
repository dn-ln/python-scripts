#! /usr/bin/env python3
import re, os, sys, json, threading
import pycurl, pymongo
from io import BytesIO
from urllib.parse import urlencode

class Multi_Pycurl(threading.Thread):
	def __init__(self, mode, camera_name):
		threading.Thread.__init__(self)
		self.mode = mode
		self.camera_name = camera_name
		self.account = [
			{"email": os.environ['CUMA_STAGING'], "password": os.environ['CUMA_STAGING_PWD']}
		]

		#	Add More Accounts
		#
		#	{"email": os.environ['CURM_STAGING'], "password": os.environ['CURM_STAGING_PWD']},
		#	{"email": os.environ['CUPU_STAGING'], "password": os.environ['CUPU_STAGING_PWD']},
		#	{"email": os.environ['CURU_STAGING'], "password": os.environ['CURU_STAGING_PWD']},
		#	{"email": os.environ['SIMA_STAGING'], "password": os.environ['SIMA_STAGING_PWD']},
		#	{"email": os.environ['SIRM_STAGING'], "password": os.environ['SIRM_STAGING_PWD']},
		#	{"email": os.environ['SISE_STAGING'], "password": os.environ['SISE_STAGING_PWD']},
		#	{"email": os.environ['UMBOUSER'], "password": os.environ['UMBOPWD']} 

		self.ua = 'Mozilla/5.0 (platform; rv:geckoversion) Gecko/geckotrail Firefox/firefoxversion'
		self.aqua = sys.argv[2]
		if self.mode == 'all':
			self.all_bandwidth, self.all_fps, self.all_resolution = list(range(0, 3001, 100)), list(range(0, 51, 5)), list(range(0, 1801, 180))
		elif self.mode == 'certain':
			self.bandwidth, self.fps, self.resolution = sys.argv[3], sys.argv[4], sys.argv[5]

	###	Get jumboId and customerId which are needed for config.
	def get_camera_info(self):
		if self.aqua.lower() == 'rc':
			mc = pymongo.MongoClient('mongodb://mongo-rc.umbocv-inc.com')
		elif self.aqua.lower() == 'staging':
			mc = pymongo.MongoClient('mongodb://mongo.umbocv-inc.com')
		db = mc['hippo-staging']
		cameras_collection = db['cameras']
		cameras_properties = db['cameraproperties']
		self.jumboId = cameras_collection.find_one({"name": {"$regex": "{}".format(self.camera_name)}})['jumboId']
		self.serial = cameras_collection.find_one({"name": {"$regex": "{}".format(self.camera_name)}})['serial']
		camera_customerId = cameras_collection.find_one({"name": {"$regex": "{}".format(self.camera_name)}})['customerId']
		self.customerId = str(camera_customerId)
		print('[serial: {}]'.format(self.serial))

	def get_token(self, email, password):
		print("Account:", email)
		c = pycurl.Curl()
		post_data = {
			"email": email,
			"password": password
		}
		postfields = json.dumps(post_data)
		headers = [
			"Content-Type: application/json",
			"Accept: application/json"
		]
		if self.aqua.lower() == 'rc':
			c.setopt(pycurl.URL, 'https://aqua-rc.umbocv-inc.com/auth/local')
		elif self.aqua.lower() == 'staging':
			c.setopt(pycurl.URL, 'https://aqua.umbocv-inc.com/auth/local')
		output = BytesIO()
		c.setopt(pycurl.POSTFIELDS, postfields)
		c.setopt(pycurl.HTTPHEADER, headers)
		c.setopt(pycurl.USERAGENT, self.ua)
		c.setopt(pycurl.WRITEDATA, output)
		c.perform()
		c.close()
		output_decode = output.getvalue().decode('iso-8859-1')
		p = re.compile(r'"token":"(.+?)"')
		self.token = p.search(output_decode).group(1)


	#	Mode 'all' takes certain range of properties and set them all. 
	#	Mode 'certain' takes sys.argv and set specific properties.
	#
	def set_properties(self):
		if self.mode == 'all':
			for bandwidth in self.all_bandwidth:
				for fps in self.all_fps:
					for resolution in self.all_resolution:
						c = pycurl.Curl()
						post_data = {
							"jumboId": self.jumboId,
							"config": {
								"bandwidth": int(bandwidth),
								"fps": int(fps),
								"resolution": int(resolution)
							} 
						}
						postfields = json.dumps(post_data)
						headers = [
							"Content-Type: application/json",
							"Accept: application/json",
							"Authorization: Bearer {}".format(self.token)
						]
						if self.aqua.lower() == 'rc':
							c.setopt(pycurl.URL, 'https://aqua-rc.umbocv-inc.com/api/cameras/{}/properties'.format(self.customerId))
						elif self.aqua.lower() == 'staging':
							c.setopt(pycurl.URL, 'https://aqua.umbocv-inc.com/api/cameras/{}/properties'.format(self.customerId))
						output = BytesIO()
						c.setopt(pycurl.CUSTOMREQUEST, 'PUT')
						c.setopt(pycurl.POSTFIELDS, postfields)
						c.setopt(pycurl.HTTPHEADER, headers)
						c.setopt(pycurl.USERAGENT, self.ua)
						c.setopt(pycurl.WRITEDATA, output)
						c.perform()
						c.close()
						output_decode = output.getvalue().decode('iso-8859-1')
						if output_decode:
							print(bandwidth, fps, resolution)
							print('{}\n\n\n'.format(output_decode))
						else:
							print(bandwidth, fps, resolution)
							print('{}: properties are set successfully.\n\n\n'.format(self.camera_name))

		elif self.mode == 'certain':
			c = pycurl.Curl()
			post_data = {
				"jumboId": self.jumboId,
				"config": {
					"bandwidth": int(self.bandwidth),
					"fps": int(self.fps),
					"resolution": int(self.resolution)
				} 
			}
			postfields = json.dumps(post_data)
			headers = [
				'Content-Type: application/json',
				'Accept: application/json',
				'Authorization: Bearer {}'.format(self.token)
			]
			if self.aqua.lower() == 'rc':
				c.setopt(pycurl.URL, 'https://aqua-rc.umbocv-inc.com/api/cameras/{}/properties'.format(self.customerId))
			elif self.aqua.lower() == 'staging':
				c.setopt(pycurl.URL, 'https://aqua.umbocv-inc.com/api/cameras/{}/properties'.format(self.customerId))
			output = BytesIO()
			#c.setopt(pycurl.VERBOSE, True) /// If you want verbose HTTP response
			c.setopt(pycurl.CUSTOMREQUEST, 'PUT')
			c.setopt(pycurl.POSTFIELDS, postfields)
			c.setopt(pycurl.HTTPHEADER, headers)
			c.setopt(pycurl.USERAGENT, self.ua)
			c.setopt(pycurl.WRITEDATA, output)
			c.perform()
			c.close()
			output_decode = output.getvalue().decode('iso-8859-1')
			if output_decode:
				print('{}\n\n\n'.format(output_decode))
			else:
				print('{}: properties are set successfully.\n\n\n'.format(self.camera_name))

	def run(self):
		self.get_camera_info()
		for account in self.account:
			self.get_token(**account)
			self.set_properties()

def make_thread():
	mode = sys.argv[1]
	if mode == 'all':
		camera_names = sys.argv[3:]
	elif mode == 'certain':
		camera_names = sys.argv[6:]
	thread_list = []
	for camera_name in camera_names:
		thread_list.append(Multi_Pycurl(mode, camera_name))
	print(thread_list)
	for thread in thread_list:
		thread.start()
		thread.join()

if __name__ == '__main__':
	make_thread()


