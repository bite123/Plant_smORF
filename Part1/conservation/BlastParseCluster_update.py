# usage: python3 BlastParseCluster_update.py Merged.Blast.txt.filtered.txt
# UPDATED FROM BlastParseCluster.py
# for each species in each cluster, only retain one protein with the highest similarity sum
# The similarity sum is the sum of similarities between target protein and other species,
# if there are more than one hit, only the highest similarity is counted

######ORIGINAL NOTE######
# to parse all-to-all species blast results (previously filtered by BlastResultFilter.py)
# For our research, species are labeled from 0 to 14
# the input file is a combination of all BlastM_N.txt.filtered.txt, in which M and N are among all species
# generate two files:
# Clusters.tsv: smORF list (OrthoFinder ID) in each cluster (row) and each species (column)
# Clusters.GeneCount.tsv: number of smORFs in each cluster (row) and each species (column), 
# the last column indicates how many species the cluster is covering. 
######ORIGINAL NOTE######


import sys

input_file = sys.argv[1]
orf_file = "Clusters.tsv"
count_file = "Clusters.GeneCount.tsv"

# to get a sum of the highest similarity score in each species (except its own species) for smORF
with open(input_file) as f_in:
	score_dict = {}
	for line in f_in:
		elements = line.strip().split("\t")
		orf_a = elements[0]
		orf_b = elements[1]
		if orf_a == orf_b:
			continue
		spe_a = orf_a.split("_")[0]
		spe_b = orf_b.split("_")[0]
		score = float(elements[2])
		if orf_a not in score_dict:
			score_dict[orf_a] = {}
		if orf_b not in score_dict:
			score_dict[orf_b] = {}
		if spe_a != spe_b:
			if spe_b not in score_dict[orf_a] or score_dict[orf_a][spe_b] < score:
				score_dict[orf_a][spe_b] = score
			if spe_a not in score_dict[orf_b] or score_dict[orf_b][spe_a] < score:
				score_dict[orf_b][spe_a] = score
	sum_dict = {}
	for k,v in score_dict.items():
		score_sum = 0
		for score in v.values():
			score_sum += score
		sum_dict[k] = score_sum

# to generate clusters, and smORFs pairs similar with each other are included in the same cluster  
with open(input_file) as f_in:
	i = 0
	clust_dict = {}
	orf_dict = {}
	for line in f_in:
		elements = line.strip().split("\t")
		orf_a = elements[0]
		orf_b = elements[1]
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

# to process the clusters. For each species in a cluster, only the smORF with the largest score sum is reserved
new_clust_dict = {}
for cl_id, cl_orf_list in clust_dict.items():
	new_clust_dict[cl_id] = []
	tmp_dict = {}
	for orf in cl_orf_list:
		spe = orf.split("_")[0]
		if spe in tmp_dict:
			tmp_dict[spe].append(orf)
		else:
			tmp_dict[spe] = [orf]
	for spe in tmp_dict:
		max_orf = max(tmp_dict[spe], key = sum_dict.get)
		new_clust_dict[cl_id].append(max_orf)

sp_list = []
for i in range(15):
	sp_list.append(str(i))

with open(orf_file,"w") as f_orf, open(count_file,"w") as f_count:
	for key in sorted(new_clust_dict.keys()):
		value = new_clust_dict[key]
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


