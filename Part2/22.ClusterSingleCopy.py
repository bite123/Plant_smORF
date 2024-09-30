# This script accepts Clusters.tsv & Clusters.GeneCount.tsv from 21.BlastParseCluster.v2.py,
# and generates output files retaining only single-copy clusters

import sys

input_file_list = sys.argv[1:]

for input_file in input_file_list:
	output_file = input_file + ".single_copy.tsv"
	with open(input_file) as f_in, open(output_file,"w") as f_out:
		for line in f_in:
			elements = line.strip("\n").split("\t")
			base_num = 1
			if input_file.endswith("Clusters.tsv"):
				for m in elements[1:]:
					n = m.split(",")
					if n == [""]:
						base_num *= 0
					else:
						base_num *= len(n)
				if base_num == 1:
					f_out.write(line)
			elif input_file.endswith("Clusters.GeneCount.tsv"):
				for m in elements[1:len(elements)-1]:
					base_num *= int(m)
				if base_num == 1:
					f_out.write(line)

