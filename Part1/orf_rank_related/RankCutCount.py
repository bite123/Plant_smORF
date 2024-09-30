# usage: python RankCutCount.py N
# based on potential_list.rank.max and gma_totalsmorf_rank_count.txt
# use cutoff as N*maxrank for any length of smORF to filter, and calculate the filter set's average count and average number 

import sys
ratio = float(sys.argv[1])
output_file = sys.argv[1] + "_stat"

cutoff_dict = {}
with open("potential_list.rank.max") as f_in:
	for line in f_in:
		elements = line.strip().split("\t")
		lenth = elements[0]
		rank = float(elements[1])
		cutoff = rank * ratio
		cutoff_dict[lenth] = cutoff

i = 0
t = 0
n = 0
with open("gma_totalsmorf_rank_count.txt") as f_in:
	for line in f_in:
		elements = line.strip().split("\t")
		rank = float(elements[1])
		lenth = elements[3]
		count = int(elements[4])
		if rank < cutoff_dict[lenth]:
			i += 1
			t += count
			if count != 0:
				n += 1

with open(output_file,"w") as f_out:
	l_1 = "smORF:" + "\t" + str(i) + "\n"
	l_2 = "Total Rank:" + "\t" + str(t) + "\n"
	avg_rank = float(t)/i
	avg_num = float(n)/i
	l_3 = "Average number:" + "\t" + str(avg_num) + "\n"
	l_4 = "Average count:" + "\t" + str(avg_rank) + "\n"
	f_out.write(l_1 + l_2 + l_3 + l_4)
