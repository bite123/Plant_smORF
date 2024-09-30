# usage: python3 ClusterSequenceExtract.py Cluster.list
# For each cluster in the list, generate a fasta file, concluding all nucleotide sequences in the cluster
# This script need:
# 1) all 15 SpeciesN.fna to provide sequences
# 2) Clusters.tsv to provide smORFs in cluster
# 3) SequenceIDs.txt, mapping OrthoFinder ID to smORF ID

import sys

list_file = sys.argv[1]
cl_file = "Clusters.tsv"
id_file = "SequenceIDs.txt"

cl_list = []
with open(list_file) as f_in:
	for line in f_in:
		cl_list.append(line.strip())

cl_dict = {}
with open(cl_file) as f_in:
	for line in f_in:
		elements = line.strip().split("\t")
		cl = elements[0]
		cl_dict[cl] = []
		for sp_orf in elements[1:]:
			orf_list = sp_orf.split(",")
			for orf in orf_list:
				if orf != "":
					cl_dict[cl].append(orf)

id_dict = {}
with open(id_file) as f_in:
	for line in f_in:
		elements = line.strip().split(" ")
		id_a = elements[0].strip(":")
		id_b = elements[1]
		id_dict[id_a] = id_b

sp_seq_dict = {}
for i in range(15):
	sp_seq_dict[i] = {}
	f = "Species" + str(i) + ".fna"
	with open(f) as f_in:
		for line in f_in:
			if line.startswith(">"):
				record = line.strip().lstrip(">")
				sp_seq_dict[i][record] = []
			else:
				sp_seq_dict[i][record].append(line)

def cluster_to_fasta(cluster):
	orf_list = cl_dict[cluster]
	output_file = cluster + ".fna"
	with open(output_file,"w") as f_out:
		for orf in orf_list:
			sp = int(orf.split("_")[0])
			new_id = id_dict[orf]
			seq = sp_seq_dict[sp][new_id]
			head_line = ">" + orf + "|" + new_id + "\n"
			seq_line = "".join(seq)
			f_out.write(head_line + seq_line) 

for cl in cl_list:
	cluster_to_fasta(cl)


