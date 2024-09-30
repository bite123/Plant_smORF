with open("Orthogroups.GeneCount.tsv") as f_in, open("count_parse.tsv","w") as f_out:
	for line in f_in:
		elements = line.strip().split("\t")
		k = 1
		for i in elements:
			if i == "0":
				k = 0
		if k:
			f_out.write(line)
