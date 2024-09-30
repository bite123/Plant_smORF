# usage: python3 BlastParseCluster.py Merged.Blast.txt.filtered.txt
# to parse all-to-all species blast results (previously filtered by BlastResultFilter.py)
# For our research, species are labeled from 0 to 14
# the input file is a combination of all BlastM_N.txt.filtered.txt, in which M and N are among all species
# generate two files:
# Clusters.tsv: smORF list (OrthoFinder ID) in each cluster (row) and each species (column)
# Clusters.GeneCount.tsv: number of smORFs in each cluster (row) and each species (column). The last column indicates how many species the cluster is covering. 

import sys

input_file = sys.argv[1]
orf_file = "Clusters.tsv"
count_file = "Clusters.GeneCount.tsv"

with open(input_file) as f_in:
	i = 0
	clust_dict = {}
	orf_dict = {}
	for line in f_in:
		elements = line.strip().split("\t")
		orf_a = elements[0]
		orf_b = elements[1]
		if orf_a == orf_b:
			continue
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

sp_list = []
for i in range(15):
	sp_list.append(str(i))

with open(orf_file,"w") as f_orf, open(count_file,"w") as f_count:
	for key in sorted(clust_dict.keys()):
		value = clust_dict[key]
		clust_name = "Cluster" + str(key).rjust(num_len, "0")
		orf_line_list = [clust_name]
		count_line_list = [clust_name]

		dict_for_line = {}
		for sp in sp_list:
			dict_for_line[sp] = []
		for orf in value:
			sp = orf.split("_")[0]
			dict_for_line[sp].append(orf)

		for k in sp_list:
			v = dict_for_line[k]
			orf_line_list.append(",".join(v))
			count_line_list.append(str(len(v)))

		orf_line = "\t".join(orf_line_list) + "\n"
		f_orf.write(orf_line)

		total_c = 15
		for c in count_line_list:
			if c == "0":
				total_c -= 1
		count_line_list.append(str(total_c))
		count_line = "\t".join(count_line_list) + "\n"
		f_count.write(count_line)


