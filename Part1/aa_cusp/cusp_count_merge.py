# usage: python cusp_count_merge.py <dir>
# to merge output files from emboss-cusp (measure codons frequency) together

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
	df_in = pd.read_csv(f_in, header=None, sep="\s+", comment="#") #not \t, but 4 spaces
	df_in.columns = list("abcde") #hard to retreive columns without colname
	df = df_in[["a","c"]]
	df.columns = ["Frac", f_in.split("/")[1]] #removing path to get file name as column name
	data.append(df)

merged = data[0]
del(data[0])
for f in data:
	merged = pd.merge(merged, f, how="outer", on="Frac")

merged.to_csv(output_file, sep="\t")
