# usage: python MergeMatrix_update.py dir
# originated from MergeMatrix.py
# to merge any "A\tB" format files to a matrix,
# with A as the first column, and each file for an following column

import pandas as pd
import os
import sys

work_dir = sys.argv[1]
output_file = sys.argv[1].strip("/") + ".MergedMatrix.txt"
file_list = []
for root,dirs,files in os.walk(work_dir):
	for file in files:
		file_path = work_dir + "/" + file
		file_list.append(file_path)

data = []
for f_in in sorted(file_list):
	df_in = pd.read_csv(f_in, header=None, sep="\t", dtype=str)
	df_in.columns = ["gene", f_in.split("/")[1]] #removing path to get file name as column name
	data.append(df_in)

merged = data[0]
del(data[0])
for f in data:
	merged = pd.merge(merged, f, how="outer", on="gene")

merged.to_csv(output_file, sep="\t", index=False)