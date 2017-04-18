#! /usr/bin/env python3
import sys, re
with open(sys.argv[1]) as f:
  flines = f.readlines()
  p = re.compile(r'"month".+?(\d+).+"nocomment".+?(\d+).+"false".+?(\d+).+"confirmed".+?(\d+).+"total".+?(\d+).+"name".+?"(.+?)"')
  for line in flines:
    r = p.search(line)
    l = []
    if r:
      l.append(r.group(6))

      for i in range(1, 6):
        try:
          l.append(int(r.group(i)))
        except ValueError:
          l.append(r.group(i))

      for i in l[2:5]:
        a = i / l[5]
        l.append(round(a * 100, 2))  

      print(l)

