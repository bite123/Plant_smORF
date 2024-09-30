# python 36.EggnogSeedN50.py emapper.annotations
# This script tells if we count the gene numbers for each Seed ortholog in annotation,
# and then order Seeds according to their size, and summarize Seeds from the top,
# when the summary comes to half of total genes, what is the Seed size?

import sys
input_file = sys.argv[1]

seed_count = {}
with open(input_file) as f_in:
	for line in f_in:
		if line.startswith("#"):
			continue
		elements = line.strip("\n").split("\t")
		seed = elements[1]
		if seed in seed_count:
			seed_count[seed] += 1
		else:
			seed_count[seed] = 1

size_list = list(seed_count.values())
size_list.sort()
total = sum(size_list)
half = total/2

accu = 0
for size in size_list:
	accu += size
	if accu >= half:
		print(size)
		break


