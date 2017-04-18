#! /usr/bin/python3
import time, calendar, sys
myTime = time.strptime(sys.argv[1], "%Y-%m-%dT%H:%M:%S")
epochTime = calendar.timegm(myTime)
print(epochTime)
