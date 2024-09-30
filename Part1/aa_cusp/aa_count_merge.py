# usage: python aa_count_merge.py <dir>
# to merge output files from aa_count.py together

import os
import sys
import pandas as pd

input_dir = sys.argv[1]
output_file = sys.argv[1] + ".merge"

f_list = os.listdir(input_dir)
path_list = []
for f in f_list:
	f_path = input_dir + "/" + f
	path_list.append(f_path)

data = []
for f_in in path_list:
	df_in = pd.read_csv(f_in, header=None, sep="\t")
	df_in.columns = ["aa", f_in.split("/")[1]] #removing path to get file name as column name
	data.append(df_in)

merged = data[0]
del(data[0])
for f in data:
	merged = pd.merge(merged, f, how="outer", on="aa")

merged.to_csv(output_file, sep="\t")
