# usage: python 25.CodemlPairwiseParse.py output_prefix [msa.codeml]
# This script reads the output file of codeml in Brassi Processing,
# and retrieve dN/dS information of each species pairwise.
# There will be a definite format and ID in the output file, as seen in the following code.

'''CODEML RESULT EXAMPLE

2 (Bna) ... 1 (Ath)
lnL =-1442.217731
  0.91665  1.46157  0.31723

t= 0.9167  S=   187.4  N=   499.6  dN/dS=  0.3172  dN = 0.1925  dS = 0.6069

'''

import sys
import re

if len(sys.argv) == 3:
	input_file = sys.argv[2]
else:
	input_file = "msa.codeml.out"
output_file = sys.argv[1] + ".pairwise"

score_dict = {}
pat_head = re.compile(r'\d+\s\((\w+)\)\s\.\.\.\s\d+\s\((\w+)\)')
pat = re.compile(r'dN/dS=\s\s([\d\.]*)\s')

with open(input_file) as f_in:
	for line in f_in:
		head = pat_head.match(line)
		if head:
			pairwise = head.group(1) + "," + head.group(2)
			for i in range(4):
				line = f_in.readline()
			score = pat.search(line).group(1)
			score_dict[pairwise] = score

with open(output_file,"w") as f_out:
	for key in sorted(score_dict.keys()):
		new_line = sys.argv[1] + "\t" + key + "\t" + score_dict[key] + "\n"
		f_out.write(new_line)

