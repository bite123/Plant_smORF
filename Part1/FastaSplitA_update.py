#!/usr/bin/env python3

# usage: python3 FastaSplitA_update.py XXX.fasta N [K]
# to split fasta into small ones with N records
# if K defined, only beginning K records will be split. This is for genomes with numerous small contigs

import re
import os
import sys
import math

input_file = sys.argv[1]
record_num = int(sys.argv[2])

retain_num = 0
if len(sys.argv) >= 4:
	retain_num = int(sys.argv[3])

n = ""
m = []

with open(input_file) as f_in:
	while True:
		line = f_in.readline()
		if line.startswith(">"):
			m.append(n)
			n = line
		elif line == "":
			m.append(n)
			break
		else:
			n += line
del(m[0]) # remove the first null element

# the below paragraph merge small contigs except beginning K ones

if retain_num:
	removed_num = retain_num + 1
	merged_list = [m[retain_num]]
	for i in range(removed_num,len(m)):
		merged_list.append(m[i])
	m[retain_num] = ''.join(merged_list)
	m = m[:retain_num + 1]

''' THOUSANDS TIMES CONSUMING THAN THE ABOVE CODES! BECAUSE m[retain_num] += m[i] STRING EDITING IS SLOWWWWWWWWWWWWWWWWWW!! REMEMBER THIS TRICK!!!
if retain_num:
	removed_num = retain_num + 1
	for i in range(removed_num,len(m)):
		m[retain_num] += m[i]
m = m[:retain_num + 1]
'''


file_num = int(math.ceil(float(len(m))/record_num)) # avoid mistake in python2! in python3, math.ceil(len(m)/record_num) will be ok
for i in range(file_num):
	i_str = str(i+1).zfill(2) # to transform 1 to "01". suspect that file_num no more than 99
	output_file = input_file.rsplit(".",1)[0] + "." + i_str + "." + input_file.rsplit(".",1)[1]
	with open(output_file,"w") as f_out:
		for j in range(record_num*i, min(record_num*(i+1),len(m))):
			f_out.write(m[j])



