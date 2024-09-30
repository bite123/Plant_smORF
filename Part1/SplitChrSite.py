#!/usr/bin/env python2
# usage: python SplitChrSite.py XXX.file N
# to correct chr site according to split chr

import os
import sys
import re
import math

input_file = sys.argv[1]
output_file = "corrected." + input_file
split = int(sys.argv[2])

# when splitting, condition is set to " > N*1000000 ". if condition will be changed to >=, then:
# size = math.ceil(split*1000000/60) * 60
size = (math.floor(split*1000000/60) + 1) * 60

multi = re.search(r'\.r(\d+)\.',input_file)[1]
multi = int(multi)
multi_size = (multi - 1) * size

def correct(raw):
	raw_num = int(raw)
	cor_num = raw_num + multi_size
	return str(cor_num)

def id_correct(id):
	s = id.split("#")
	raw = s[1]
	s[1] = correct(raw)
	cor_id = "#".join(s)
	return cor_id


if input_file.endswith(".bed"):
	with open(input_file) as f_in, open(output_file,"w") as f_out:
		for line in f_in:
			elements = line.strip().split("\t")
			elements[1] = correct(elements[1])
			elements[2] = correct(elements[2])
			elements[3] = id_correct(elements[3])
			new_line = "\t".join(elements) + "\n"
			f_out.write(new_line)

if input_file.endswith(".fa"):
	with open(input_file) as f_in, open(output_file,"w") as f_out:
		for line in f_in:
			if line.startswith(">"):
				id = line.lstrip(">").strip()
				new_id = id_correct(id)
				new_line = ">" + new_id + "\n"
				f_out.write(new_line)
			else:
				f_out.write(line)


