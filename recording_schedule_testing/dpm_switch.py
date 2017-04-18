#! /usr/bin/env python3
import re, sys, time, subprocess
from datetime import datetime

# Set Up Start and End Time
start_time = datetime.now().replace(hour=int(sys.argv[1][0:2]), minute=int(sys.argv[1][2:4]), second=0, microsecond=0)
start_time_timestamp = start_time.timestamp()
end_time = datetime.now().replace(hour=int(sys.argv[2][0:2]), minute=int(sys.argv[2][2:4]), second=0, microsecond=0)
end_time_timestamp = end_time.timestamp()

# Turn On or Off Monitor In a Routine 
while end_time_timestamp != start_time_timestamp:
	get_now_timestamp = datetime.now().timestamp()
	if start_time_timestamp > get_now_timestamp:
		time.sleep(start_time_timestamp - get_now_timestamp)
	elif start_time_timestamp <= get_now_timestamp:
		xset_q = subprocess.Popen('xset q', stdout=subprocess.PIPE, shell=True)
		xset_q_output = xset_q.stdout.read().decode('utf-8')
		p = re.compile(r'Monitor is On')
		monitor_status = p.search(xset_q_output)
		if monitor_status:
			subprocess.Popen('xset dpms force off', shell=True)
			print('Monitor Off: ', datetime.now().strftime('%Y.%m.%d %H:%M:%S.%f'))
		else:
			subprocess.Popen('xset dpms force on', shell=True)
			print('Monitor On: ', datetime.now().strftime('%Y.%m.%d %H:%M:%S.%f'))
		start_time_timestamp += 600
