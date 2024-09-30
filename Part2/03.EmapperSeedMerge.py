# This script extract seed_ortholog from emapper.annotation files and merge them together
# usage: python 03.EmapperSeedMerge.py dir/
# target file example: Ath_sORF.emapper.annotations

import os
import sys

work_dir = sys.argv[1]
output_file = sys.argv[1].strip("/") + ".EmapperSeedMerge.tsv"
file_list = []
file_to_spe = {}
for root,dirs,files in os.walk(work_dir):
	for file in files:
		file_path = work_dir + "/" + file
		file_to_spe[file_path] = file.split("_")[0]
		file_list.append(file_path)

with open(output_file, "w") as f_out:
	for input_file in sorted(file_list):
		spe_name = file_to_spe[input_file]
		with open(input_file) as f_in:
			for line in f_in:
				if line.startswith("#"):
					continue
				elements = line.strip("\n").split("\t")
				gene_name = elements[0]
				seed_ortho = elements[1]
				new_line = spe_name + "\t" + gene_name + "\t" + seed_ortho + "\n"
				f_out.write(new_line)


