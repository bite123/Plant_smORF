# usage: python BedExtract.py bed list
# to extract bed lines according to list

import sys

input_file = sys.argv[1]
list_file = sys.argv[2]
output_file = sys.argv[1] + "." + sys.argv[2] + ".extracted"

extract_list = []
with open(list_file) as f_in:
	for line in f_in:
		extract_id = line.strip()
		extract_list.append(extract_id)

db = {}

with open(input_file) as f_in:
	for line in f_in:
		elements = line.strip().split("\t")
		orf = elements[3]
		db[orf] = line

with open(output_file,"w") as f_out:
	for orf in extract_list:
		if orf in db:
			f_out.write(db[orf])

