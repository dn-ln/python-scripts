#! /usr/bin/env python3
import paramiko, pexpect, sys, os
import time

def usage():
	print('./video_params2a.py <camera address> <schedule> <interval> <starting time>')

def time_ref():
	now = (time.time() % 86400) - time.timezone
	time_hour, time_minute = (int(time_input) // 100) * 3600, (int(time_input) % 100) * 60
	start_time = time_hour + time_minute
	executed_time = time.strftime('%Y-%m-%dT%H:%M:%S', time.localtime())
	file_date = [time.strftime('%Y-%m-%d', time.gmtime()), time.strftime('%H', time.gmtime()), time.strftime('%Y%m%d-%H%M', time.gmtime())]
	return [now, start_time, executed_time, file_date]

def change_resolution():
	n1 = 0
	n2 = 0
	resolution = [
	'',
	'config_cmd Video0:width 1280 Video0:height 720',
	'config_cmd Video0:width 1920 Video0:height 1080'
	]
	lilith = [
	'',
	'lilith -k WSTransport',
	'lilith -s WSTransport',
	'lilith -r WSTransport',
	'lilith -k MediaRec',
	'lilith -s MediaRec; lilith -s EventMgr',
	'lilith -r MediaRec; lilith -r EventMgr',
	'lilith -r all',
	'lilith -s MediaRec; lilith -s EventMgr; lilith -k WSTransport'
	]

	if len(schedule) % 2 == 0 and len(schedule) / 2 == len(interval) + 1:
		print('Connecting to camera...')
		c = paramiko.SSHClient()
		c.load_system_host_keys()
		c.connect(address, username=usr, password=pwd)
		print('Connect successfully.')

		start_time = time_ref()[1]

		while schedule[n1:]:
			x = int(schedule[n1:n1+2][0])
			y = int(schedule[n1:n1+2][1])
			cmd = 'PATH=$PATH:/usr/sbin; {}'.format(resolution[x])
			cmd2 = 'PATH=$PATH:/usr/sbin; {}'.format(lilith[y])
			if interval[n2:]:
				interval_time = int(interval[n2]) * 60
			now = time_ref()[0]

			if start_time - now >= 0:
				time.sleep(start_time - now)
				if resolution[x]:
					c.exec_command(cmd)
					print('Executed:', cmd[22:], time_ref()[2], time.time())
				if lilith[y]:
					c.exec_command(cmd2)
					print('Lilith executed:', cmd2[22:], time_ref()[2], time.time())
				start_time += interval_time
				file_date = time_ref()[3]
				if file_date not in file_dates:
					file_dates.append(file_date)
			else:
				if resolution[x]:
					print('Time has passed.', cmd[22:])
				if lilith[y]:
					print('Time has passed.', cmd2[22:])
				start_time += interval_time

			n1 += 2
			n2 += 1

		c.close()
		return True

	else:
		usage()
		return False
	
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
		address, schedule, interval, time_input = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]
		usr, pwd = os.environ['CAMUSERID'], os.environ['CAMPASSWORD']
		file_dates = []
		change_result = change_resolution()
		if change_result:
			get_recording()

	except IndexError:
		usage()
