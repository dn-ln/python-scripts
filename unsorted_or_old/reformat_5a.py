#! /usr/bin/env python3
import sys, re
try:
  with open(sys.argv[1]) as f:
    flines = f.readlines()
    for line in flines:
      p1 = re.compile(r'\d+')
      p2 = re.compile(r'\"name\"\s:\s\"(.+)\"')
      nums = ' '.join(p1.findall(line))
      name = p2.search(line)
      if name:
        print(name.group(1), nums)
except IndexError:
  print("./reformat_5a.py <txt file>")


