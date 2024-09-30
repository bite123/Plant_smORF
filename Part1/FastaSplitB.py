#!/usr/bin/env python2
# usage: python FastaSplitB.py XXX.fasta N
# There is ONLY ONE record in XXX.fasta
# to split XXX.fasta into small ones, each with N Mb

import os
import sys

input_file = sys.argv[1]
size = float(sys.argv[2]) * 1000000


with open(input_file) as f_in:
	line = f_in.readline()
	record_name = line.strip()
	count = 0
	s = ""
	s_list = []
	for line in f_in:
		s += line
		count += len(line.strip())
		if count > size: # will be changed into >= in the formal edition
			s_list.append(s)
			s = ""
			count = 0
	s_list.append(s) # to get the ending seq which is less than N Mb

for i in range(len(s_list)):
	i_str = str(i+1).zfill(2)	# to transform 1 to "01". suspect that file_num no more than 99
	output_file = input_file.rsplit(".",1)[0] + ".r" + i_str + ".fasta"
	name = record_name + "r" + i_str + "\n"
	with open(output_file,"w") as f_out:
		f_out.write(name)
		f_out.write(s_list[i])


