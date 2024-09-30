# usage: python TotalOrfScoreRank.py XXX.total.smORF.fa.fai
# for smORF (eg. Chr01#10000243#+#20.7), the last number "20.7" is score. This script will calculate the order of the score among all smORFs with the same length (that's why inputting a faidx file)

from __future__ import division # apply division of python3 in python2
import sys


input_file = sys.argv[1]

dict_orf = {}

with open(input_file) as f_in:
	for line in f_in:
		elements = line.strip().split("\t")
		orf_id = elements[0]
		orf_len = elements[1]
		orf_score = orf_id.split("#")[-1]
		dict_orf[orf_id] = [orf_len, float(orf_score)]

for i in range(10,102):
	s_len = str(i)
	output_file = input_file + "." + s_len.rjust(3,"0") + ".rank"
	s_dict = {k:v for k,v in dict_orf.items() if v[0] == s_len}
	total_num = len(s_dict)

	order_list = sorted(s_dict.items(), key=lambda x:x[1][1], reverse=True)

	with open(output_file,"w") as f_out:
		i = 0
		for pairs in order_list:
			i += 1
			orf_id = pairs[0]
			orf_score = str(pairs[1][1])
			orf_rank = str(i/total_num*1000000)
			new_line = orf_id + "\t" + orf_rank + "\t" + orf_score + "\t" + s_len + "\n"
			f_out.write(new_line)
