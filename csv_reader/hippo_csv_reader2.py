#! /usr/bin/env python3
import os, csv, subprocess
import time as t
from datetime import datetime, date, time, timedelta

def hippo_csv_reader():
	usr, pwd = os.environ['HELPDESK_DBUSER'], os.environ['HELPDESK_DBPASS']
	os.environ['PYTHONIOENCODING'] = 'utf-8'
	DEVNULL = open(os.devnull, 'wb')

	start_time = datetime.now()
	exec_time = datetime.combine(date(start_time.year, start_time.month, start_time.day), time(11, 00, 00))
	if exec_time.timestamp() - start_time.timestamp() < 0:
		exec_time += timedelta(days=1)

	while True:
		print('\033[92m' + 'Waiting for:', '\033[0m' + str(exec_time - start_time))
		t.sleep(exec_time.timestamp() - start_time.timestamp())

		subprocess.Popen('python2 helpdesk.py roi production --user={} --password="{}"'.format(usr, pwd), stdout=DEVNULL, shell=True, cwd='/home/umbo/OmniOwl/Portal/DBQuery').communicate()
		print('Writing to the file at: %s' % datetime.now())
		with open('/home/umbo/OmniOwl/Portal/DBQuery/hippo.csv') as f:
			reader = csv.DictReader(f)
			with open('hippoResult_%s.txt' % exec_time.strftime('%Y%m%d_%H:%M'), 'a') as f2:
				fieldnames = ["Is Online", "CamOn_withROI", "CamOff_withROI"]
				writer = csv.DictWriter(f2, fieldnames=fieldnames)
				writer.writeheader()
				total = {'Is Online': 0, 'CamOn_withROI': 0, 'CamOff_withROI': 0}
				for row in reader:
					if row['Is Online'] == "Yes":
						total['Is Online'] += 1
					elif row['Is Online'] == "Yes" and int(row['#ROI']) >= 1:
						total['CamOn_withROI'] += 1
					elif row['Is Online'] == "No" and int(row['#ROI']) >= 1:
						total['CamOff_withROI'] += 1
				writer.writerow(total)

		exec_time += timedelta(days=1)

if __name__ == '__main__':
	hippo_csv_reader()
		