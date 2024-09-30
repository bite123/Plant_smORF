# This script processes Orthogroups.GeneCount.tsv & Orthogroups_UnassignedGenes.tsv to generate statistical data
# The code could be more efficiency, generating whole information by processing file one time,
# However, it processes file multi-times, to clarify the procedure, and to facilitate possible supplements 

import itertools

input_assign = "Orthogroups.GeneCount.tsv"
input_unassign = "Orthogroups_UnassignedGenes.tsv"

# 0 label species
labels = []
with open("Orthogroups_UnassignedGenes.tsv") as f_in:
	head_line = f_in.readline()
	elements = head_line.strip("\n").split("\t")
	for i in range(1, len(elements)):
		labels.append(elements[i])
	n_spe = len(labels)
	n_list = list(range(1, n_spe+1))
	label_line = "Stat" + "\t" + "\t".join(labels) + "\n"

# 1 count unassigned genes
unassign_num = {}
for i in n_list:
	unassign_num[i] = 0
with open(input_unassign) as f_in:
	head_line = f_in.readline()
	for line in f_in:
		elements = line.strip("\n").split("\t")
		for i in n_list:
			if elements[i] != "":
				unassign_num[i] += 1
				break


# 2 basic measurement per species, and og count according to their sharing in N species
gene_num = {}
og_num = {}
uni_og_num = {}
uni_gene_num = {}
og_count = {}
for d in [gene_num, og_num, uni_gene_num, uni_og_num, og_count]:
	for i in n_list:
		d[i] = 0
with open(input_assign) as f_in:
	head_line = f_in.readline()
	for line in f_in:
		share_list = []
		elements = line.strip("\n").split("\t")
		for i in n_list:
			if elements[i] != "0":
				og_num[i] += 1
				gene_num[i] += int(elements[i])
				share_list.append(i)
		if len(share_list) == 1:
			uni_i = share_list[0]
			uni_og_num[uni_i] += 1
			uni_gene_num[uni_i] += int(elements[uni_i])
		og_count[len(share_list)] += 1


# 3 gene and og numbers shared in species pairs
og_in_pair = {}
gene_in_pair = {}
for i in itertools.product(n_list, n_list):
	og_in_pair[i] = 0
	gene_in_pair[i] = 0
with open(input_assign) as f_in:
	head_line = f_in.readline()
	for line in f_in:
		share_list = []
		elements = line.strip("\n").split("\t")
		for i in n_list:	
			if elements[i] != "0":
				share_list.append(i)
		for k in og_in_pair.keys():
			if k[0] in share_list and k[1] in share_list:
				og_in_pair[k] += 1
				gene_in_pair[k] += int(elements[k[0]])


# 4 og size distribution per species
og_size = {}
max_size = 0
for i in n_list:
	og_size[i] = {}
with open(input_assign) as f_in:
	head_line = f_in.readline()
	for line in f_in:
		elements = line.strip("\n").split("\t")
		for i in n_list:
			if elements[i] != "0":
				if elements[i] in og_size[i].keys():
					og_size[i][elements[i]] += 1
				else:
					og_size[i][elements[i]] = 1
				if int(elements[i]) > max_size:
					max_size = int(elements[i])


# 5 the distribution of genes per species according to their sharing in N species
og_share = {}
gene_share = {}
for i in n_list:
	og_share[i] = {}
	gene_share[i] = {}
	for j in n_list:
		og_share[i][j] = 0
		gene_share[i][j] = 0
with open(input_assign) as f_in:
	head_line = f_in.readline()
	for line in f_in:
		share_num = 0
		elements = line.strip("\n").split("\t")
		for i in n_list:
			if elements[i] != "0":
				share_num += 1
		for i in n_list:
			if elements[i] != "0":
				og_share[i][share_num] += 1
				gene_share[i][share_num] += int(elements[i])



# fin. output step

def dict2list(dic):
	res_list = []
	for key in sorted(dic.keys()):
		res_list.append(str(dic[key]))
	return res_list

# output gene_num, og_num, uni_og_num, uni_gene_num in step 2, and unassign_num in step 1
with open("OrthoStat.basic.tsv", "w") as f_out:
	og_num_list = dict2list(og_num)
	gene_num_list = dict2list(gene_num)
	unassign_num_list = dict2list(unassign_num)
	uni_og_num_list = dict2list(uni_og_num)
	uni_gene_num_list = dict2list(uni_gene_num)
	og_num_line = "Number of orthogroups" + "\t" + "\t".join(og_num_list) + "\n"
	gene_num_line = "Number of assigned genes" + "\t" + "\t".join(gene_num_list) + "\n"
	unassign_num_line = "Number of unassigned genes" + "\t" + "\t".join(unassign_num_list) + "\n"
	uni_og_num_line = "Number of species-specific orthogroups" + "\t" + "\t".join(uni_og_num_list) + "\n"
	uni_gene_num_line = "Number of species-specific genes" + "\t" + "\t".join(uni_gene_num_list) + "\n"
	for i in [label_line, og_num_line, gene_num_line, unassign_num_line, uni_og_num_line, uni_gene_num_line]:
		f_out.write(i)


# output og_count in step 2
with open("OrthoStat.og_spe_distr.tsv", "w") as f_out:
	f_out.write("Number of species in orthogroup" + "\t" + "Number of orthogroups" + "\n")
	for key in sorted(og_count.keys()):
		new_line = str(key) + "\t" + str(og_count[key]) + "\n"
		f_out.write(new_line)


# output og_in_pair in step 3
with open("OrthoStat.og_pair.tsv", "w") as f_out:
	head_line = "" + "\t" + "\t".join(labels) + "\n"
	f_out.write(head_line)
	for i in n_list:
		i_list = []
		for j in n_list:
			i_list.append(str(og_in_pair[(i,j)]))
		i_line = labels[i-1] + "\t" + "\t".join(i_list) + "\n"
		f_out.write(i_line)

# output gene_in_pair in step 3
with open("OrthoStat.gene_pair.tsv", "w") as f_out:
	head_line = "" + "\t" + "\t".join(labels) + "\n"
	f_out.write(head_line)
	for i in n_list:
		i_list = []
		for j in n_list:
			i_list.append(str(gene_in_pair[(i,j)]))
		i_line = labels[i-1] + "\t" + "\t".join(i_list) + "\n"
		f_out.write(i_line)


# output og_size in step 4
with open("OrthoStat.og_size_distr.tsv", "w") as f_out:
	head_line = "Number of genes in orthogroup" + "\t" + "\t".join(labels) + "\n"
	f_out.write(head_line)
	for i in range(1, max_size+1):
		i_list = []
		for j in n_list:
			if str(i) in og_size[j]:
				i_list.append(str(og_size[j][str(i)]))
			else:
				i_list.append("0")
		i_line = str(i) + "\t" + "\t".join(i_list) + "\n"
		f_out.write(i_line)


# output og_share in step 5
with open("OrthoStat.og_share_distr.tsv", "w") as f_out:
	head_line = "Number of species in orthogroup" "\t" + "\t".join(labels) + "\n"
	f_out.write(head_line)
	for i in n_list:
		i_list = []
		for j in n_list:
			i_list.append(str(og_share[j][i]))
		i_line = str(i) + "\t" + "\t".join(i_list) + "\n"
		f_out.write(i_line)


# output gene_share in step 5
with open("OrthoStat.gene_share_distr.tsv", "w") as f_out:
	head_line = "Number of species in orthogroup" "\t" + "\t".join(labels) + "\n"
	f_out.write(head_line)
	for i in n_list:
		i_list = []
		for j in n_list:
			i_list.append(str(gene_share[j][i]))
		i_line = str(i) + "\t" + "\t".join(i_list) + "\n"
		f_out.write(i_line)
		












