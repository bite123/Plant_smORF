# usage: python 34.EggnogDescriptionSelect.py eggnog.anno XXX,YYY,ZZZ...
# This script looks for keywords in description of each protein,
# the keywords are provided as a parameter, separated by comma

import sys
input_file = sys.argv[1]
output_file = input_file + ".selected"
spe_id = input_file.split("_")[0]
keyword_list = sys.argv[2].split(",")

with open(input_file) as f_in, open(output_file, "w") as f_out:
	f_in.readline()
	for line in f_in:
		elements = line.strip().split("\t")
		description = elements[7].lower()
		label = 0
		for kw in keyword_list:
			if kw in description:
				label = 1
				break
		if label:
			new_line = spe_id + "\t" + elements[0] + "\t" + elements[1] + "\t" + elements[7] + "\n"
			f_out.write(new_line)

