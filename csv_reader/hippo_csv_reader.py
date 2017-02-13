#! /usr/bin/env python3
import csv, sys

csvfile = sys.argv[1]
with open(csvfile) as f:
	reader = csv.DictReader(f)
	with open('hippoResult.txt', 'a') as f2:
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

		