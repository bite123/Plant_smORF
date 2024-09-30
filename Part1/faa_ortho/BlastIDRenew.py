# usage: python BlastIDRenew.py Blast0_0.txt.gz OrthoIDRenew.txt
# using mapping file OrthoIDRenew.txt, to transfer old ids in BLAST to new ids

import sys
import gzip

input_file = sys.argv[1]
map_file = sys.argv[2]
output_file = input_file + ".renew.txt.gz"

map_dict = {}
with open(map_file) as f_in:
	for line in f_in:
		elements = line.strip().split("\t")
		map_dict[elements[0]] = elements[1]

with gzip.open(input_file, "rb") as f_in, gzip.open(output_file, "wb") as f_out:
	for line in f_in:
		line = line.decode()
		elements = line.strip().split("\t")
		if elements[0] not in map_dict or elements[1] not in map_dict:
			continue
		elements[0] = map_dict[elements[0]]
		elements[1] = map_dict[elements[1]]
		new_line = "\t".join(elements) + "\n"
		new_line = new_line.encode()
		f_out.write(new_line)


