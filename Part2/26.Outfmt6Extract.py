# usage: python 26.Outfmt6Extract.py outfmt6 list
# Extracting only the alignment wigh query and subject both in the list

import sys
input_file = sys.argv[1]
list_file = sys.argv[2]
output_file = sys.argv[1] + "." + sys.argv[2] + ".extracted"

extract_list = []
with open(list_file) as f_in:
	for line in f_in:
		extract_id = line.strip("\n")
		extract_list.append(extract_id)

with open(input_file) as f_in, open(output_file,"w") as f_out:
	for line in f_in:
		elements = line.strip("\n").split("\t")
		q_id = elements[0]
		s_id = elements[1]
		if q_id in extract_list and s_id in extract_list:
			f_out.write(line)

			