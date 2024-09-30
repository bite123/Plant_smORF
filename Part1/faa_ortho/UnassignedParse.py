# usage: python UnassignedParse.py Orthogroups_UnassignedGenes.tsv
# to generate lists of unassigned genes for each species

with open("Orthogroups_UnassignedGenes.tsv") as f_in:
	head_line = f_in.readline()
	species_list = head_line.strip().split("\t")[1:]
	total_dict = {}
	for spe in species_list:
		total_dict[spe] = []
	for line in f_in:
		elements = line.strip().split("\t")[1:]
		for i in range(len(elements)):
			if elements[i] != "":
				total_dict[species_list[i]].append(elements[i])

for spe in species_list:
	output_file = spe + ".unassigned.list"
	with open(output_file,"w") as f_out:
		for orf in total_dict[spe]:
			f_out.write(orf + "\n")


