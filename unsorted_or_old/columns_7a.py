#! /usr/bin/env python3
from csv import reader

with open('column.txt') as f:
  rows = csv.reader(f, delimiter=' ')
  for row in rows:
    print(row[4])

