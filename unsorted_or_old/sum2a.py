#!/usr/bin/env python3
import sys
from csv import reader
d1 = {}
for argv in sys.argv[1:]:
  with open(argv) as f:
    csvreader = reader(f, delimiter=' ')
    for row in csvreader:
      d2 = {row[0]: int(row[1])}
      if row[0] not in d1:
        d1.update(d2)
      else:
        d1[row[0]] += int(row[1])

keys, values = list(d1.keys()), list(d1.values())
for i in range(len(keys)):
    print(keys[i], values[i])

