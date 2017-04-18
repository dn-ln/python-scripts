#! /usr/bin/env python3
import re

with open('input.txt', 'r') as f:
  f_read = f.read().rstrip()
  p = r'.(\d\d):'
  today = re.search(p, f_read).group(1)
  tomorrow = r'.' + '{0:0=2d}'.format(int(today) + 1) + ':'
  f_new = re.sub(p, tomorrow, f_read)
  print(f_new)


