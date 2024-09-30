# usage: python 37.EggnogTCDB.py eggnog_file rank(3 or 4)
# count the numbers of TCDBs in KEGG_TC column 
# only count when ko02000 (transporters) in BRITE column
# TCDB ID is like a.b.c.d.e, count a.b.c.d for rank 4, and a.b.c for rank 3
# if there is a.b.c.d.e and a.b.c.d.f, then assign to a.b.c.d (this condition is for most of multi-ID)
# if there is a.b.c.d1.e and a.b.c.d2.f, then assign to a.b.c

import sys

input_file = sys.argv[1]
rank = int(sys.argv[2])
output_file = input_file + ".tcdb"

def check_if_tcdb(line:str):
	label = 0
	elements = line.strip("\n").split("\t")
	kegg_pathway = elements[16]
	kp_list = kegg_pathway.split(",")
	for kp in kp_list:
		if kp == "ko02000":
			label = 1
	return label

def parse_tcdb(tcdb:str):
	t_list = tcdb.split(",")
	retain_num = rank
	if len(t_list) == 1: # if there is only 1 ID
		sole_t = t_list[0]
		t_div = sole_t.split(".")
		if len(t_div) > retain_num:
			sole_t = ".".join(t_div[:retain_num])
	else: # multi-ID
		tmp_dict = {}
		min_len = 5
		for t in t_list:
			tmp_dict[t] = t.split(".")
			if len(tmp_dict[t]) < min_len:
				min_len = len(tmp_dict[t]) # the shortest ID
		for i in range(min_len):
			break_num = min_len
			equal_list = []
			for v in tmp_dict.values():
				equal_list.append(v[i])
			if len(set(equal_list)) != 1: # to see if the first i+1 site is the same
				break_num = i
				break
		retain_num = min(retain_num, break_num)
		sole_t = ".".join(tmp_dict[t_list[0]][:retain_num])
	if sole_t == "":
		sole_t = "-"
	return sole_t

tcdb_count = {}
with open(input_file) as f_in:
	for line in f_in:
		if line.startswith("#") or not check_if_tcdb(line):
			continue
		elements = line.strip().split("\t")
		tc = elements[17]
		tcdb_id = parse_tcdb(tc)
		if tcdb_id in tcdb_count:
			tcdb_count[tcdb_id] += 1
		else:
			tcdb_count[tcdb_id] = 1

with open(output_file, "w") as f_out:
	for k,v in tcdb_count.items():
		line = k + "\t" + str(v) + "\n"
		f_out.write(line)

		 


