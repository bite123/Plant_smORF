#!/usr/bin/env python3
# usage: python Outfmt6FaiParse.py XXX.fai XXX.outfmt6
# to extract proteins that match 100% and with a full length in outfmt6

import sys

input_file = sys.argv[1]
output_file = input_file + ".parse_list"
blast_file = sys.argv[2]

orf_len = {}
with open(input_file) as f_in:
	for line in f_in:
		elements = line.strip().split("\t")
		orf = elements[0]
		# length = int(elements[1]) -1 NO NEED, for the stop codon has been removed in the novel analysis
		length = int(elements[1]) 
		orf_len[orf] = length

match_list = []
with open(blast_file) as f_in:
	for line in f_in:
		elements = line.strip().split("\t")
		orf = elements[0]
		pident = float(elements[2])
		length = int(elements[3])
		if pident == 100 and length == orf_len[orf]:
			if orf not in match_list:
				match_list.append(orf)

with open(output_file,"w") as f_out:
	for k in match_list:
		new_line = k + "\n"
		f_out.write(new_line)

