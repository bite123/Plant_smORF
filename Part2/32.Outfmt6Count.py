# usage: python 32.Outfmt6Count.py outfmt6 [class_file]
# This script counts the number of the subjects,
# if there is a class file, then the subjects will be transferred to class first.
# Headline is added in the output file for the following merge process.

import sys
input_file = sys.argv[1]
output_file = input_file + ".count"

anno = 0
if len(sys.argv) == 3:
	anno = 1
	anno_file = sys.argv[2]
	anno_dict = {}
	with open(anno_file) as f_in:
		for line in f_in:
			elements = line.strip().split("\t")
			anno_dict[elements[0].lower()] = elements[1]
			# .lower(): in case some IDs like "Dca20462.1" turns into "DCA20462" in blastDB. dunno why.

count_dict = {}
with open(input_file) as f_in:
	for line in f_in:
		elements = line.strip().split("\t")
		subj = elements[1]
		if anno:
			if subj.lower() in anno_dict:
				gene = anno_dict[subj.lower()]
			# in case some IDs like "KZV54549.1" turns into "KZV54549" in blastDB. dunno why.
			else:
				new_subj = subj + ".1"
				gene = anno_dict[new_subj.lower()] 
		else:
			gene = subj
		if gene in count_dict:
			count_dict[gene] += 1
		else:
			count_dict[gene] = 1

with open(output_file, "w") as f_out:
	for key,value in count_dict.items():
		new_line = key + "\t" + str(value) + "\n"
		f_out.write(new_line)

