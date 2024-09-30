# usage: python OrthoIDRenew.py old_v1.SequenceIDs.txt new_v1s.SequenceIDs.txt
# eg. in SequenceIDs.txt: 0_18: Chr1#10024394#+#88.5
# to map old_v1 to new_v1s, using smORF ID as a bridge

import sys
old = sys.argv[1]
new = sys.argv[2]

old_dict = {}
new_dict = {}

with open(old) as f_in:
	for line in f_in:
		elements = line.strip().split(": ")
		old_dict[elements[1]] = elements[0]

with open(new) as f_in:
	for line in f_in:
		elements = line.strip().split(": ")
		new_dict[elements[0]] = elements[1]

output_file = "OrthoIDRenew.txt"
with open(output_file,"w") as f_out:
	for k,v in new_dict.items():
		new_id = k
		old_id = old_dict[v]
		f_out.write(old_id + "\t" + new_id + "\n")
