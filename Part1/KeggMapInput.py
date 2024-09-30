#!/usr/bin/env python2
# usage: python KeggMapInput.py XXX.txt
# to fit kegg mapping reconstruct tool, transfer "A    B1,B2,B3" into three lines as "A    B1" etc.

import os
import sys

input_file = sys.argv[1]
output_file = "revised." + input_file

with open(input_file) as f_in, open(output_file,"w") as f_out:
	for line in f_in:
		gene = line.strip().split("\t")[0]
		kolist = line.strip().split("\t")[1].split(",")
		for i in kolist:
			new_line = gene + "\t" + i + "\n"
			f_out.write(new_line)
