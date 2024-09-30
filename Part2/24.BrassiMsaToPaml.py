# usage: python 24.BrassiMsaToPaml.py msa.file <speA,speB, ...> [msa.paml]
# This script accepts the MSA result from Brassi processing,
# and transforms it into PAML input format.

import sys
input_file = sys.argv[1]
spe_list = sys.argv[2].split(",")
if len(sys.argv) == 4:
	output_file = sys.argv[3]
else:
	output_file = "msa.paml"

seq_dict = {}
with open(input_file) as f_in:
	i = 0
	for line in f_in:
		if line.startswith(">"):
			i += 1
			spe_id = spe_list[i-1]
			seq_dict[seq_id] = []
		else:
			seq_dict[seq_id].append(line.strip())

new_dict = {}
stop_codon = 0
for key,value in seq_dict.items():
	new_seq = "".join(value)
	if new_seq[-3:] in ["TAA", "TAG", "TGA"]:
		stop_codon += 1
	new_dict[key] = new_seq
final_len = len(new_seq)

if stop_codon:
	for key,value in new_dict.items():
		len_seq = len(value)
		new_seq = value[:len_seq-3]
		new_dict[key] = new_seq
	final_len = len_seq - 3

spe_num = str(len(spe_list))
with open(output_file,"w") as f_out:
	head_line = "\t" + spe_num + "\t" + str(final_len) +"\n"
	f_out.write(head_line) 
	for key in sorted(new_dict.keys()):
		f_out.write(key + "\n" + new_dict[key] + "\n")
