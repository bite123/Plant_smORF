# This script accepts a list of OrthoGroups, and count seed, COG, GO, KEGG, and PFAM numbers in them
# usage: python 11.OthoAnaly.FuncCount.py og.list
# This script requires annotation files as belows:
# go-basic.obo.txt, ko2pathway.tsv, pathway_rank.tsv，pathway_info.tsv
# and a prepared file OrthoStat.og_emapper_annotation.tsv

import sys
input_file = sys.argv[1]
output_seed = sys.argv[1] + ".seed.tsv"
output_cog = sys.argv[1] + ".cog.tsv"
output_go = sys.argv[1] + ".go.tsv"
output_kegg_rank2 = sys.argv[1] + ".kegg_rank2.tsv"
output_kegg_rank3 = sys.argv[1] + ".kegg_rank3.tsv"
output_pfam = sys.argv[1] + ".pfam.tsv"

og_map_file = "OrthoStat.og_emapper_annotation.tsv"
go_anno_file = "go-basic.obo.txt"
ko2pathway_file = "ko2pathway.tsv"
pathway_rank_file = "pathway_rank.tsv"
pathway_info_file = "pathway_info.tsv"


#### PROCESSING FILES ####
og_list = []
with open(input_file) as f_in:
	for line in f_in:
		og_list.append(line.strip("\n"))

go_map = {}
with open(go_anno_file) as f_in:
	for line in f_in:
		elements = line.strip("\n").split("\t")
		go_map[elements[0]] = "\t".join(elements[1:])

ko2pathway = {}
with open(ko2pathway_file) as f_in:
	for line in f_in:
		elements = line.strip("\n").split("\t")
		pathways = elements[1].split(",")
		ko2pathway[elements[0]] = pathways

pathway_rank = {}
with open(pathway_rank_file) as f_in:
	for line in f_in:
		elements = line.strip("\n").split("\t")
		pathway_rank[elements[0]] = elements[1]

pathway_info = {}
with open(pathway_info_file) as f_in:
	for line in f_in:
		elements = line.strip("\n").split("\t")
		pathway_info[elements[0]] = elements[1]

og_map = {}
with open(og_map_file) as f_in:
	for line in f_in:
		elements = line.strip("\n").split("\t")
		og_id = elements[0]
		seed = elements[1]
		cog_list = list(elements[6])
		go_list = elements[9].split(",")
		kegg_list = elements[11].split(",")
		pfam_list = elements[20].split(",")
		og_map[og_id] = [cog_list, go_list, kegg_list, pfam_list, seed]


#### COUNT ####
seed_count = {}
for og in og_list:
	if og in og_map:
		seed = og_map[og][4]
		if seed in seed_count:
			seed_count[seed] += 1
		else:
			seed_count[seed] = 1

cog_count = {}
for og in og_list:
	if og in og_map:
		value = og_map[og]
		for cog in value[0]:
			if cog in cog_count:
				cog_count[cog] += 1
			else:
				cog_count[cog] = 1

pfam_count = {}
for og in og_list:
	if og in og_map:
		value = og_map[og]
		for pfam in value[3]:
			if pfam in pfam_count:
				pfam_count[pfam] += 1
			else:
				pfam_count[pfam] = 1

go_count = {}
for og in og_list:
	if og in og_map:
		value = og_map[og]
		for go in value[1]:
			if go in go_count:
				go_count[go] += 1
			else:
				go_count[go] = 1

kegg_rank2 = {}
kegg_rank3 = {}
for og in og_list:
	if og in og_map:
		value = og_map[og]
		kegg_list = value[2]
		total_rank3 = set()
		for kegg in kegg_list:
			kegg = kegg[3:]
			if kegg in ko2pathway:
				adding_rank3 = set(ko2pathway[kegg])
				total_rank3.update(adding_rank3)
		for rank3 in total_rank3:
			rank2 = pathway_rank[rank3]
			if rank3 in kegg_rank3:
				kegg_rank3[rank3] += 1
			else:
				kegg_rank3[rank3] = 1
			if rank2 in kegg_rank2:
				kegg_rank2[rank2] += 1
			else:
				kegg_rank2[rank2] = 1	


#### OUTPUT FILE ####
with open(output_seed,"w") as f_out:
	for k,v in seed_count.items():
		new_line = k + "\t" + str(v) + "\n"
		f_out.write(new_line)

with open(output_cog,"w") as f_out:
	for k,v in cog_count.items():
		new_line = k + "\t" + str(v) + "\n"
		f_out.write(new_line)

with open(output_pfam,"w") as f_out:
	for k,v in pfam_count.items():
		new_line = k + "\t" + str(v) + "\n"
		f_out.write(new_line)

with open(output_go,"w") as f_out:
	for k,v in go_count.items():
		if k in go_map:
			new_line = k + "\t" + go_map[k] + "\t" + str(v) + "\n"
			f_out.write(new_line)

with open(output_kegg_rank2,"w") as f_out:
	for key in sorted(kegg_rank2.keys()):
		if key in pathway_info:
			new_line = key + "\t" + pathway_info[key] + "\t" + str(kegg_rank2[key]) + "\n"
			f_out.write(new_line)

with open(output_kegg_rank3,"w") as f_out:
	for key in sorted(kegg_rank3.keys()):
		new_line = key + "\t" + pathway_info[key] + "\t" + str(kegg_rank3[key]) + "\n"
		f_out.write(new_line)


