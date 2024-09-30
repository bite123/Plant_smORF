# usage: python rank_cut_list.py N
# originated from RankCutCount.py

import sys
ratio = float(sys.argv[1])
output_file = sys.argv[1] + "_list"

cutoff_dict = {}
with open("potential_list.rank.max") as f_in:
	for line in f_in:
		elements = line.strip().split("\t")
		lenth = elements[0]
		rank = float(elements[1])
		cutoff = rank * ratio
		cutoff_dict[lenth] = cutoff

with open("gma_totalsmorf_rank_count.txt") as f_in, open(output_file,"w") as f_out:
	for line in f_in:
		elements = line.strip().split("\t")
		rank = float(elements[1])
		lenth = elements[3]
		if rank < cutoff_dict[lenth]:
			new_line = elements[0] + "\n"
			f_out.write(new_line)
