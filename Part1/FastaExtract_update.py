#!/usr/bin/env python2

# Usage: python FastaExtract_update.py XXX.fasta XXX.list [f60|f1](default=f60)
# Print 60 words one line (default or parameter f60), or print one record into one line (parameter f1).
# Extracting fasta records EXACTLY MATCHING names on a list. 
# Updated: also output a file containg the unextracted records

import re
import os
import sys
import collections # to create ordered dict

input_file = sys.argv[1]
list_file = sys.argv[2]
output_file = sys.argv[1] + ".extracted"
unextracted_file = sys.argv[1] + ".unextracted"

f60 = True
if len(sys.argv) == 4:
	if sys.argv[3] == "f1":
		f60 = False

extract_list = []
with open(list_file) as f_in:
	for line in f_in:
		extract_id = line.strip()
		extract_list.append(extract_id)


d1 = collections.OrderedDict() # just a setting

db = {}
with open(input_file) as f_in, open(output_file, "w") as f_out, open(unextracted_file, "w") as f_un:
	for line in f_in:
		if line.startswith("#"):
			continue
		elif line.startswith(">"):
			record = line.strip().lstrip(">").split(" ")[0] #split symbol based on the target fasta file
			db[record] = []
		else:
			db[record].append(line.strip())

	for extract_id in extract_list:
		sequence = db.pop(extract_id)
		sequence = ''.join(sequence)
		anno_line = ">" + extract_id + "\n"
		f_out.write(anno_line)
		if f60:
			while sequence != "":
				seq_line = sequence[0:60] + "\n"
				sequence = sequence[60:]
				f_out.write(seq_line)
		else:
			seq_line = sequence + "\n"
			f_out.write(seq_line)

	for key,value in db.items():
		sequence = ''.join(value)
		anno_line = ">" + key + "\n"
		f_un.write(anno_line)
		if f60:
			while sequence != "":
				seq_line = sequence[0:60] + "\n"
				sequence = sequence[60:]
				f_un.write(seq_line)
		else:
			seq_line = sequence + "\n"
			f_un.write(seq_line)
