# This scirpt selects OGs exists in given species from Orthogroups.GeneCount.tsv.
# Beware that there are 17 columns in Orthogroups.GeneCount.tsv, including OG, 15 species, and Total
# usage: python 01.GeneCountSelection.py <column number list, separated by comma> s|u(default:s)
# s: OG exists in given species
# u: OG exists in given species and absents in others
# column number:
'''
0: Ath_sORF.v1.faa
1: Bna_sORF.v1.faa
2: Bol_sORF.v1.faa
3: Cqu_sORF.v1.faa
4: Csa_sORF.v1.faa
5: Gma_sORF.v1.faa
6: Gra_sORF.v1.faa
7: Hvu_sORF.v1.faa
8: Mtr_sORF.v1.faa
9: Osa_sORF.v1.faa
10: Sin_sORF.v1.faa
11: Sit_sORF.v1.faa
12: Sly_sORF.v1.faa
13: Tae_sORF.v1.faa
14: Zma_sORF.v1.faa
'''

import sys

input_file = "Orthogroups.GeneCount.tsv"

spe_list = sys.argv[1].split(",")
num_list = [int(x) for x in spe_list]

if len(sys.argv) == 3 and sys.argv[2] == "u":
	output_type = "u"
	output_file = input_file + ".uni_selected"
else:
	output_type = "s"
	output_file = input_file + ".selected"


with open(input_file) as f_in, open(output_file,"w") as f_out:
	head_line = f_in.readline()
	f_out.write(head_line)
	for line in f_in:
		elements = line.strip().split("\t")
		count_list = []
		other_count = 0
		for i in range(len(elements)-2): # Exclude the first OG column and the last Total count
			if i in num_list:
				count_list.append(elements[i+1])
			else:
				other_count += int(elements[i+1])
		if output_type == "s":
			if "0" not in count_list:
				f_out.write(line)
		if output_type == "u":
			if "0" not in count_list and other_count == 0:
				f_out.write(line)
