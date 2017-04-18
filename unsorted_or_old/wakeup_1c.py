#!/usr/bin/env python3
import sys, time, calendar
inputlines = open(sys.argv[1]).read().splitlines()
for line in inputlines:
  inputtime = time.strptime(line, "%Y.%m.%d:%H:%M:%S")
  epochtime = calendar.timegm(inputtime)
  curtime = int(time.time())

  while True:
    if curtime > epochtime:
      print("The time", line, "has already passed.")
      break
    elif curtime < epochtime:
      curtime = int(time.time())
    else:
      print("The time", line, "has just occured.")
      break
          
    
      
       
