# usage: python 23.ClusterSequenceExtract.py Clusters.tsv <A.fa,B.fa...>
# For each cluster line, generate a fasta file, concluding all nucleotide sequences in the cluster
# Each column in Clusters.tsv is corresponding to a species FASTA, IN ORDER

import sys

cl_file = sys.argv[1]
fa_list = sys.argv[2].split(",")

cl_dict = {}
spe_map = {}
with open(cl_file) as f_in:
	for line in f_in:
		elements = line.strip("\n").split("\t")
		cl = elements[0]
		cl_dict[cl] = []
		for i in range(len(elements)-1):
			spe_id = i + 1
			sp_orf = elements[spe_id]
			orf_list = sp_orf.split(",")
			for orf in orf_list:
				if orf != "":
					spe_map[orf] = spe_id
					cl_dict[cl].append(orf)

sp_seq_dict = {}
for i in range(len(fa_list)):
	sp_seq_dict[i+1] = {}
	f = fa_list[i]
	with open(f) as f_in:
		for line in f_in:
			if line.startswith(">"):
				record = line.strip("\n").lstrip(">").split(" ")[0].split("|")[-1] # may be adjusted for specific fasta
				sp_seq_dict[i+1][record] = []
			else:
				sp_seq_dict[i+1][record].append(line)

for key,value in cl_dict.items():
	output_file = key + ".fna"
	with open(output_file,"w") as f_out:
		for orf in value:
			sp = spe_map[orf]
			seq = sp_seq_dict[sp][orf]
			head_line = ">" + orf + "\n"
			seq_line = "".join(seq)
			f_out.write(head_line + seq_line) 

