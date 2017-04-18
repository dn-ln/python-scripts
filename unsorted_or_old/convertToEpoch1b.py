#! /usr/bin/python3
import time, calendar, sys
input_lines = open(sys.argv[1]).read().splitlines()
for input_line in input_lines:
 myTime = time.strptime(input_line, '%Y.%m.%d:%H:%M:%S')
 epochTime = calendar.timegm(myTime)
 print(input_line, epochTime)
