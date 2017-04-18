#! /usr/bin/env python3
import csv, ast

with open('cu_list.txt') as f:
	new_dic = []
	for line in f:
		line2 = line.rstrip()
		new_dic.append(line2)

with open('cu_list.csv', 'w') as f:
	fieldnames = ['username', 'firstName', 'lastName']
	new_csv = csv.DictWriter(f, fieldnames=fieldnames)

	new_csv.writeheader()
	for str_dic in new_dic:
		dic = ast.literal_eval(str_dic)
		new_csv.writerow(dic)