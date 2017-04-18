#! /usr/bin/env python3
import sys, re
with open(sys.argv[1]) as f:
  flines = f.readlines()
  p = re.compile(r'"month".+?(\d+).+"day".+?(\d+).+"nocomment".+?(\d+).+"false".+?(\d+).+"confirmed".+?(\d+).+"total".+?(\d+).+"name".+?"(.+?)"')
  print('customer month/day total confirmed%')
  print('---------------------------------------------')
  for line in flines:
    r = p.search(line)
    l = []
    if r:
      l.append(r.group(7))

      for i in range(1, 7):
        try:
          l.append(int(r.group(i)))
        except ValueError:
          l.append(r.group(i))

      for i in l[3:6]:
        a = i / l[6]
        l.append(round(a * 100, 2))  

      #print(l)
      print('"' + r.group(7) + '"', r.group(1) + "/" + r.group(2), r.group(6), round(int(r.group(5)) / int(r.group(6)) * 100, 2))

