# usage: python 27.GffRename.py gff mapping.list
# This script is for renaming the first column of bed file,
# and transforms it to GFF file used in MCScanX.

import sys
input_file = sys.argv[1]
map_file = sys.argv[2]
output_file = sys.argv[1] + "." + sys.argv[2] + ".rename"

map_dict = {}
with open(map_file) as f_in:
	for line in f_in:
		elements = line.strip("\n").split("\t")
		map_dict[elements[0]] = elements[1]

with open(input_file) as f_in, open(output_file,"w") as f_out:
	for line in f_in:
		elements = line.strip("\n").split("\t")
		chr_id = elements[0]
		if chr_id in map_dict:
			new_list = [map_dict[chr_id], elements[3], elements[1], elements[2]]
			new_line = "\t".join(new_list) + "\n"
			f_out.write(new_line)
			
