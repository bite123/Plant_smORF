# usage: python 35.sORFMappingOG.py Orthogroups.tsv list
# This script maps the plant smORF to its orthogroup
# There are two columns in the list: 1st is ID, and 2nd is species while represented as the column order in Orthogroups.tsv
# There will be two output files: 1st is ID-OG mapping, and 2nd counts how many species within each OG

import sys
input_file = sys.argv[1]
list_file = sys.argv[2]
output_mapping = input_file + ".mapping.txt"
output_stat = input_file + ".stat.txt"

og_dict = {}
with open(input_file) as f_in:
	for line in f_in:
		elements = line.strip("\n").split("\t")
		og_id = elements[0]
		for i in range(1, 16):
			id_list = elements[i].split(",")
			if id_list != [""]:
				for orf_id in id_list:
					orf_id = orf_id.lstrip()
					og_dict[(orf_id, i)] = og_id

og_stat = {}
with open(list_file) as f_in, open(output_mapping, "w") as f_out:
	for line in f_in:
		elements = line.strip().split("\t")
		orf_id = elements[0]
		orf_spe = int(elements[1])
		if (orf_id, orf_spe) in og_dict:
			orf_og = og_dict[(orf_id, orf_spe)]
			new_line = orf_id + "\t" + orf_og + "\n"
			f_out.write(new_line)
			if orf_og in og_stat:
				og_stat[orf_og].append(orf_spe)
			else:
				og_stat[orf_og] = [orf_spe]

with open(output_stat, "w") as f_out:
	for key,value in og_stat.items():
		total_num = len(value)
		spe_number = len(set(value))
		new_line = key + "\t" + str(total_num) + "\t" + str(spe_number) + "\n"
		f_out.write(new_line) 




