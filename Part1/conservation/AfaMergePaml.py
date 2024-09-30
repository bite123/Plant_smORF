# usage: python3 AfaMergePaml.py dir
# Input file: multi-sequence align files, processed by muscle and trimal
# This script merges all MSA files (afa, etc.), and generate two output files:
# 1) a sequence merged MSA files, for tree building
# 2) a file for PAML processing
# About sequence ID for the merged file:
# Since the ID in the MSA file come from OrthoFinders and my script, like "0_178148|Chr5#23548510#+#31"
# the species ID "0" will be extracted and used

import os
import sys

input_dir = sys.argv[1]
output_afa =  sys.argv[1] + ".afa"
output_paml = sys.argv[1] + ".paml"

file_list = os.listdir(input_dir)
path_list = []
for file in file_list:
	path = input_dir + "/" + file
	path_list.append(path)

sequence_dict = {}
for i in range(15):
	sequence_dict[i] = []
length_list = []

def afa_parse(afa_file):
	with open(afa_file) as f_in:
		seq_dict = {}
		for line in f_in:
			if line.startswith(">"):
				seq_id = line.lstrip(">").split("_")[0]
				seq_dict[seq_id] = []
			else:
				seq_dict[seq_id].append(line.strip())
		new_dict = {}
		for k,v in seq_dict.items():
			new_v = "".join(v)
			new_dict[int(k)] = new_v
		seq_length = len(new_dict[0])
		return [new_dict, seq_length]

for path in path_list:
	[p_dict, p_length] = afa_parse(path)
	length_list.append(p_length)
	for k,v in p_dict.items():
		sequence_dict[k].append(v)

with open(output_afa,"w") as f_out:
	for i in range(15):
		head_line = ">" + str(i) + "\n"
		seq_line = "".join(sequence_dict[i]) + "\n"
		f_out.write(head_line + seq_line)

with open(output_paml,"w") as f_out:
	total_len = str(sum(length_list))
	num = str(len(length_list))
	length_list = [str(i) for i in length_list]
	a_line = "15\t" + total_len + "\tG\n"
	b_line =  "G\t" + num + "\t" + "\t".join(length_list) + "\n"
	f_out.write(a_line + b_line)
	for i in range(15):
		head_line = str(i) + "\n"
		seq_line = "".join(sequence_dict[i]) + "\n"
		f_out.write(head_line + seq_line)	
