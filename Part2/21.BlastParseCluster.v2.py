# v1 is for OrthoFinder BLAST output,
# and this v2 is general for BLAST outfmt6
# usage: python3 21.BlastParseCluster.v2.py <1_A_B.outfmt6, 2_A_C.outfmt6, 3_A_C.outfmt6 ...>
# To ensure species ID could be retrieved from file name,
# name the BLAST files like: XXXXXX_A_B.XXXXX

# ATTENTION!!!!
# Making BLAST database may change sequence ID from lcl|NC_027757.2_cds_XP_013670397.1_1 to NC_027757.2_cds_XP_013670397.1_1!
# In this script need to transform the above ID!


######################## Original Note ####################
# usage: python3 BlastParseCluster.py Merged.Blast.txt.filtered.txt
# to parse all-to-all species blast results (previously filtered by BlastResultFilter.py)
# For our research, species are labeled from 0 to 14
# the input file is a combination of all BlastM_N.txt.filtered.txt, in which M and N are among all species
# generate two files:
# Clusters.tsv: smORF list (OrthoFinder ID) in each cluster (row) and each species (column)
# Clusters.GeneCount.tsv: number of smORFs in each cluster (row) and each species (column). The last column indicates how many species the cluster is covering. 
######################## Original Note ####################

import sys

input_file_list = sys.argv[1:]
orf_file = "Clusters.tsv"
count_file = "Clusters.GeneCount.tsv"

clust_dict = {}
i = 0
orf_dict = {}
spe_map = {}
spe_list = []

for input_file in input_file_list:
	spe_a = input_file.split(".")[-2].split("_")[-2]
	spe_b = input_file.split(".")[-2].split("_")[-1]
	spe_list.append(spe_a)
	spe_list.append(spe_b)
	with open(input_file) as f_in:
		for line in f_in:
			elements = line.strip().split("\t")
			orf_a = elements[0].split("|")[-1] # See ATTENTION above.
			orf_b = elements[1]
			if orf_a == orf_b:
				continue
			spe_map[orf_a] = spe_a
			spe_map[orf_b] = spe_b
			if orf_a not in orf_dict and orf_b not in orf_dict:
				i += 1
				clust_dict[i] = [orf_a, orf_b]
				orf_dict[orf_a] = i
				orf_dict[orf_b] = i
			elif orf_a in orf_dict and orf_b in orf_dict:
				pass
			elif orf_a in orf_dict and orf_b not in orf_dict:
				orf_dict[orf_b] = orf_dict[orf_a]
				clust_dict[orf_dict[orf_b]].append(orf_b)
			elif orf_a not in orf_dict and orf_b in orf_dict:
				orf_dict[orf_a] = orf_dict[orf_b]
				clust_dict[orf_dict[orf_a]].append(orf_a)
num_len = len(str(i))
spe_list = sorted(list(set(spe_list)))


with open(orf_file,"w") as f_orf, open(count_file,"w") as f_count:
	for key in sorted(clust_dict.keys()):
		value = clust_dict[key]
		clust_name = "Cluster" + str(key).rjust(num_len, "0")
		orf_line_list = [clust_name]
		count_line_list = [clust_name]

		dict_for_line = {}
		for spe in spe_list:
			dict_for_line[spe] = []
		for orf in value:
			spe = spe_map[orf]
			dict_for_line[spe].append(orf)

		for spe in spe_list:
			v = dict_for_line[spe]
			orf_line_list.append(",".join(v))
			count_line_list.append(str(len(v)))

		orf_line = "\t".join(orf_line_list) + "\n"
		f_orf.write(orf_line)

		total_c = len(spe_list)
		for c in count_line_list:
			if c == "0":
				total_c -= 1
		count_line_list.append(str(total_c))
		count_line = "\t".join(count_line_list) + "\n"
		f_count.write(count_line)


