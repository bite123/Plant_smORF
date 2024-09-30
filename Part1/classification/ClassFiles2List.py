#!/usr/bin/env python2

# usage:python ClassFiles2List.py dir
# to generate a classfication list based on files resulted from SmorfClassify.sh

import sys
import os

work_dir = sys.argv[1]
output_file = work_dir + ".class.list"

f1 = work_dir + "/" + work_dir + ".CLASS1.bed"
f2 = work_dir + "/" + work_dir + ".CLASS2.bed"
f3 = work_dir + "/" + work_dir + ".CLASS3.bed"
f4 = work_dir + "/" + work_dir + ".CLASS4.bed"
f5 = work_dir + "/" + work_dir + ".CLASS5.bed"
f6 = work_dir + "/" + work_dir + ".CLASS6.bed"
f_list = [f1, f2, f3, f4, f5, f6]

with open(output_file,"w") as f_out:
	i = 1
	for f in f_list:
		with open(f) as f_in:
			for line in f_in:
				elements = line.strip().split("\t")
				sorf = elements[3]
				new_line = sorf + "\t" + str(i) + "\n"
				f_out.write(new_line)
		i += 1

