# usage: python aa_count.py XXX.faa
# to count amino acids of proteins

from collections import Counter
import sys

input_file = sys.argv[1]
output_file = sys.argv[1] + ".aa_stat"

# to sum values in two dicts according to keys
def sum_dict(x,y):
	res = {}
	for k in x.keys() | y.keys():
		res[k] = sum(i.get(k,0) for i in (x,y))
	return res
		
prot_dict = {}
with open(input_file) as f_in:
	for line in f_in:
		if line.startswith(">"):
			prot_id = line.strip().lstrip(">").split(":")[0] # CUSTOMIZED IN CONDITION!
			prot_dict[prot_id] = []
		else:
			prot_dict[prot_id].append(line.strip())

aa_dict = {}
for k,v in prot_dict.items():
	total = "".join(v)
	aa_stat = Counter(total)
	aa_dict[k] = aa_stat

stat_dict = {}
for prot in prot_dict:
	p = aa_dict[prot]
	stat_dict = sum_dict(stat_dict, p)

with open(output_file,"w") as f_out:
	for k,v in stat_dict.items():
		new_line = k + "\t" + str(v) + "\n"
		f_out.write(new_line)

