# usage: python 33.EggnogGoPfamCount.py eggnog
# count the numbers of go and pfam in the eggnog annotation
# update: kegg module is also counted!

import sys

input_file = sys.argv[1]
go_file = input_file + ".go"
pfam_file = input_file + ".pfam"
mod_file = input_file + ".module"

go_dict = {}
pfam_dict = {}
mod_dict = {}
with open(input_file) as f_in:
	f_in.readline() # skip the headline
	for line in f_in:
		elements = line.strip().split("\t")
		go_list = elements[9].split(",")
		pfam_list = elements[20].split(",")
		mod_list = elements[13].split(",")
		for go in go_list:
			if go in go_dict:
				go_dict[go] += 1
			else:
				go_dict[go] = 1
		for pfam in pfam_list:
			if pfam in pfam_dict:
				pfam_dict[pfam] += 1
			else:
				pfam_dict[pfam] = 1
		for mod in mod_list:
			if mod in mod_dict:
				mod_dict[mod] += 1
			else:
				mod_dict[mod] = 1			

with open(go_file, "w") as f_out:
	for k,v in go_dict.items():
		line = k + "\t" + str(v) + "\n"
		f_out.write(line)

with open(pfam_file, "w") as f_out:
	for k,v in pfam_dict.items():
		line = k + "\t" + str(v) + "\n"
		f_out.write(line)

with open(mod_file, "w") as f_out:
	for k,v in mod_dict.items():
		line = k + "\t" + str(v) + "\n"
		f_out.write(line)
