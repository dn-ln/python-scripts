#! /usr/bin/env python3
import time, os, sys
starttime = time.time()
try:
  cmd = sys.argv[1]
  interval = int(sys.argv[2])
  while True:
    counttime = time.time()
    if counttime - starttime >= interval:
      os.system(cmd)
      starttime += interval

except IndexError:
  print('./fw_reboot.py <command> <interval(in second)>')
