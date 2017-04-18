#! /usr/bin/env python3
import time, os, sys
from datetime import datetime
try:
  interval = int(sys.argv[2])
  cmd = sys.argv[1]

  while True:
    t0 = time.time()
    t = interval - (t0 % interval)
    time.sleep(t)
    os.system(cmd)

except IndexError:
  print('./fw_reboot.py <command> <interval(second)>')

except ValueError:
  print('Please enter a non-float interval.')
