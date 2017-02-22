#! /usr/bin/env python3
import re, os, sys, time, subprocess
from datetime import datetime, timedelta
import pexpect, paramiko

class Video_Params_Record:
	def __init__(self):
		self.usr = os.environ['USER']
		self.pwd =  os.environ['PASSWORD']
		self.resolution = [
		'',
		'cmd1',
		'cmd2',
		'cmd3'
		]
		self.li = [
		'',
		'cmd1',
		'cmd2',
		'cmd3'
		]

	def get_argv(self):
		self.address = sys.argv[1]
		self.schedule = sys.argv[2]
		self.interval = sys.argv[3]
		self.t_input = sys.argv[4]

	def get_time(self, which):
		time_hour, time_minute = (int(self.t_input) // 100) * 3600, (int(self.t_input) % 100) * 60
		dtime = datetime.utcnow() - timedelta(minutes=1)

		now = (time.time() % 86400) - time.timezone
		start_time = time_hour + time_minute
		executed_time_str = time.strftime('%Y-%m-%dT%H:%M:%S', time.localtime())
		file_date = [
			time.strftime('%Y%m%d', time.gmtime()),
			dtime.strftime('%H%M')
		]

		time_info = [now, start_time, executed_time_str, file_date]
		return time_info[which]

	def change_resolution(self, schedule, interval):
		self.file_dates = []

		if len(schedule) % 2 == 0 and len(schedule) / 2 == len(interval) + 1:
			print('Connecting to camera...')
			c = paramiko.SSHClient()
			c.load_system_host_keys()
			c.connect(self.address, username=self.usr, password=self.pwd, timeout=20)
			with open('get_record_log.txt', 'w') as f:
			c.exec_command('nohup the_cmd')
			print('Waiting for command to be executed.')

			n1 = 0
			n2 = 0
			start_time = self.get_time(1)
			while schedule[n1:]:
				x = int(schedule[n1:n1+2][0])
				y = int(schedule[n1:n1+2][1])
				cmd = 'PATH=$PATH:/usr/sbin; {}'.format(self.resolution[x])
				cmd2 = 'PATH=$PATH:/usr/sbin; {}'.format(self.li[y])
				if interval[n2:]:
					interval_time = int(interval[n2]) * 60
				now = self.get_time(0)

				if start_time - now >= 0:
					time.sleep(start_time - now)
					if self.resolution[x]:
						c.exec_command(cmd)
						file_date_re = self.get_time(3)
						print('Executed:', cmd[22:], self.get_time(2))
					if self.lilith[y]:
						c.exec_command(cmd2)
						file_date_li = self.get_time(3)
						print('Li executed:', cmd2[22:], self.get_time(2))
						if y == 7:
							print('Waiting li to restart...')
							time.sleep(15)
					start_time += interval_time

					if 'file_date_li' in locals(): 
						self.file_dates.append(file_date_li)
						print('Append file date from li cmd.')
					elif 'file_date_re' in locals(): 
						self.file_dates.append(file_date_re)
						print('Append file date from resolution cmd.')
				else:
					print('Time has passed.', cmd[22:])
					start_time += interval_time
				n1 += 2
				n2 += 1

			c.close()

		else:
			usage()

	def get_recording(self):
		pex = pexpect.spawn('scp {}@{}:/get_record_log.txt /home/deanlin/Videos/'.format(self.usr, self.address))
		pex.expect('password:')
		pex.sendline(self.pwd)
		pex.expect(pexpect.EOF)

		with open('/home/deanlin/Videos/get_record_log.txt', 'r') as f:
			log = f.read()
			for i in self.file_dates:
				file_name = '/mnt/sdcard/{}-{}.+?Close MP4 writer <-'.format(self.file_dates[i][0], self.file_dates[i][1])
				p = re.compile(r'({})'.format(file_name))
				if p.search(log):
					argv = (self.usr, self.address, file_name)
					pex = pexpect.spawn('scp {}@{}:{}*.mp4 ~/Videos'.format(argv))
					pex.expect('password:')
					pex.sendline(self.pwd)
					pex.expect(pexpect.EOF)

	def run(self):
		self.get_argv()
		self.change_resolution(self.schedule, self.interval)
		self.get_recording()

def usage():
	print('./scp_video.py <camera address> <schedule> <interval> <starting time>')

if __name__ == '__main__':
	launcher = Video_Params_Record()
	launcher.run()
