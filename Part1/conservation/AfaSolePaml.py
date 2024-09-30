# usage: python3 AfaSolePaml.py afa_file
# Input file: multi-sequence align files, processed by muscle (and trimal if needed)
# This script transforms the afa file to a file for PAML processing
# About sequence ID for the merged file:
# Since the ID in the MSA file come from OrthoFinders and my script, like "0_178148|Chr5#23548510#+#31"
# the species ID "0" will be extracted and used

import sys

input_file = sys.argv[1]
output_paml = sys.argv[1] + ".paml"

species_table = {
    "0": "Ath", "1": "Bna", "2": "Bol", "3": "Cqu",
    "4": "Csa", "5": "Gma", "6": "Gra", "7": "Hvu",
    "8": "Mtr", "9": "Osa", "10": "Sin", "11": "Sit",
    "12": "Sly", "13": "Tae", "14": "Zma"                        
}


with open(input_file) as f_in:
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
		new_k = species_table[k]
		new_dict[new_k] = new_v
	seq_num = len(new_dict)
	seq_length = len(new_dict["Ath"])

with open(output_paml,"w") as f_out:
	head_line = "\t" + str(seq_num) + "\t" + str(seq_length) + "\n"
	f_out.write(head_line)
	for k in sorted(new_dict.keys()):
		f_out.write(k + "\n" + new_dict[k] + "\n")
