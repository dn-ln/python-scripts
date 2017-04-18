#! /usr/bin/env python3

#import datetime, calendar
from collections import OrderedDict
#tuple_today = datetime.date.today().timetuple()
#epoch_tday = calendar.timegm(tuple_today)

json_data = {
		"jumboId": "<jumboId>",
		"roiId": "<roiId>",
		"snapshot": "https://www.xxx.com/images/page_learnc_01-2.07877134.png",
		"previewVideo": "https://www.xxx.com/images/page_learnc_01-2.07877134.png",
		"beginTime": "<timestamp>",
		"objectType": "person"
	    }

order_data = OrderedDict(sorted(json_data.items()))
print(order_data)

opt = ["-i", "-X", "-d", "-H"]
req = ["POST"]
hdr = ["Authorization: Bearer <token>", "Accept: application/json"]
api = ["https://xxx.com/api/alerts/cv"]


print('curl', opt[0], opt[1], req[0], opt[2], order_data, opt[3], hdr[0], opt[3], hdr[1], api[0])
