# This script uses the concatenate file total.emapper.annotations from 15 species annotation,
# and OrthoStat.og_seed_stat.tsv from 04.OrthoGroupSeedAnno.py,
# to link annotation to OG through seed.

# usage: python 05.SeedAnnoDetails.py

og_seed_file = "OrthoStat.og_seed_stat.tsv"
seed_anno_file = "total.emapper.annotations"
output_file = "OrthoStat.og_emapper_annotation.tsv"

seed_dict = {}
with open(seed_anno_file) as f_in:
	for line in f_in:
		if line.startswith("#"):
			continue
		elements = line.strip("\n").split("\t")
		seed = elements[1]
		if seed not in seed_dict:
			seed_dict[seed] = elements[2:]

with open(og_seed_file) as f_in, open(output_file, "w") as f_out:
	for line in f_in:
		elements = line.strip("n").split("\t")
		og_id = elements[0]
		seed = elements[1]
		anno = seed_dict[seed]
		new_line = og_id + "\t" + seed + "\t" + "\t".join(anno) + "\n"
		f_out.write(new_line)

 