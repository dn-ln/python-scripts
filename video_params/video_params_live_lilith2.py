#! /usr/bin/env python3
import paramiko, pexpect, sys, os
import time

def usage():
	print('./video_params2a.py <camera address> <schedule> <interval> <starting time>')

class time_ref:
	def __init__(self):
		self.now = (time.time() % 86400) - time.timezone
		self.hour, self.min = (int(startime) // 100) * 3600, (int(time_input) % 100) * 60
		self.start = hour + minute
		self.exec = time.strftime('%Y-%m-%dT%H:%M:%S', time.localtime())
		self.file_date = [time.strftime('%Y-%m-%d', time.gmtime()), time.strftime('%H', time.gmtime()), time.strftime('%Y%m%d-%H%M', time.gmtime())]

def change_resolution():
	n1 = 0
	n2 = 0
	resolution = [
	'',
	'config_cmd Video0:width 1280 Video0:height 720',
	'config_cmd Video0:width 1920 Video0:height 1080',
	'config_cmd Video0:width 1920 Video0:height 360',
	'config_cmd Video0:width 1920 Video0:height 200',
	'config_cmd Video0:width 1920 Video0:height 180',
	'config_cmd Video0:width 1920 Video1:height 360',
	'config_cmd Video0:width 1920 Video1:height 720',
	'config_cmd Video1:width 1920 Video1:height 360'
	]
	lilith = [
	'',
	'lilith -k WSTransport',
	'lilith -s WSTransport',
	'lilith -r WSTransport',
	'lilith -k MediaRec',
	'lilith -s MediaRec; lilith -s EventMgr',
	'lilith -r MediaRec; lilith -r EventMgr',
	'lilith -r all'
	]

	if len(schedule) % 2 == 0 and len(schedule) / 2 == len(interval) + 1:
		print('Connecting to camera...')
		c = paramiko.SSHClient()
		c.load_system_host_keys()
		c.connect(address, username=usr, password=pwd, timeout=20)
		print('Connect successfully.')

		time_ref1 = time_ref() 

		while schedule[n1:]:
			x = int(schedule[n1:n1+2][0])
			y = int(schedule[n1:n1+2][1])
			cmd = 'PATH=$PATH:/usr/sbin; {}'.format(resolution[x])
			cmd2 = 'PATH=$PATH:/usr/sbin; {}'.format(lilith[y])
			if interval[n2:]:
				interval_time = int(interval[n2]) * 60
			time_ref2 = time_ref()

			if time_ref1.start - time_ref2.now >= 0:
				time.sleep(time_ref1.start - time_ref2.now)
				if resolution[x]:
					c.exec_command(cmd)
					time_ref3 = time_ref()
					print('Executed:', cmd[22:], time_ref3.start, time.time())
				if lilith[y]:
					c.exec_command(cmd2)
					time_ref4 = time_ref()
					print('Lilith executed:', cmd2[22:], time_ref4.start, time.time())
				stime_ref += interval_time
				file_date = 
				if file_date not in file_dates:
					file_dates.append(file_date)
			else:
				print('Time has passed.', cmd[22:])
				start_time += interval_time

			n1 += 2
			n2 += 1

		c.close()

	else:
		usage()
	
def get_recording():
	print('Waiting files to be generated...')
	time.sleep(80)
	print('Retrieving files...')
	for file_date in file_dates:
		pex = pexpect.spawn('scp {}@{}:/mnt/sdcard/{}/{}/{}* /home/deanlin/Videos/'.format(usr, address, file_date[0], file_date[1], file_date[2]))
		pex.expect('password:')
		pex.sendline(pwd)
		pex.expect(pexpect.EOF)
	print('Success.')

if __name__ == '__main__':
	try:
		address, schedule, interval, start_time = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]
		usr, pwd = os.environ['CAMUSERID'], os.environ['CAMPASSWORD']
		file_dates = []
		change_resolution()
		get_recording()

	except IndexError:
		usage()
