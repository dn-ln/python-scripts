#! /usr/bin/env python3
import datetime, calendar
d = datetime.datetime.utcnow()
d2 = d.strftime('%Y.%m.%d:%H:%M:')
with open('input2.txt', 'w') as f:
  for i in range(60):
    s = '%.2d' % i
    d3 = d2 + s + '\n'
    f.write(d3)


