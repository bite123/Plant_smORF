# Usage: python EnogAnnoCogCount.py dir
# to extract "COG_category" column from EGGNOG annotation tables in dirXXX and export a merged count table

import sys
import os

work_dir = sys.argv[1]

file_list = []
for root,dirs,files in os.walk(work_dir):
	for file in files:
		file_path = work_dir + "/" + file
		file_list.append(file_path)

file_dict = {}
for file in file_list:
	cog_dict = {}
	with open(file) as f_in:
		f_in.readline()
		for line in f_in:
			elements = line.strip().split("\t")
			cog = elements[5]
			for char in cog:
				if char in cog_dict:
					cog_dict[char] += 1
				else:
					cog_dict[char] = 1

	file_dict[file] = cog_dict

with open("cog_stat.txt","w") as f_out:
	for k,v in file_dict.items():
		f_out.write(k + "\n")
		for m,n in v.items():
			f_out.write(m + "\t" + str(n) + "\n")

