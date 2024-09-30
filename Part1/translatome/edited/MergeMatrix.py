#!/usr/bin/env python2

# usage: python MergeMatrix.py dir
# to merge gene expression matrices in dirXXX

import pandas as pd
import os
import sys

work_dir = sys.argv[1]
output_file = sys.argv[1] + ".MergedMatrix.txt"

file_list = []
for root,dirs,files in os.walk(work_dir):
	for file in files:
		file_path = work_dir + "/" + file
		file_list.append(file_path)

data = []
for f_in in file_list:
	df_in = pd.read_csv(f_in, header=None, sep="\t")
	df_in.columns = ["gene", f_in.split("/")[1]] #removing path to get file name as column name
	data.append(df_in)

merged = data[0]
del(data[0])
for f in data:
	merged = pd.merge(merged, f, how="outer", on="gene")


merged.to_csv(output_file, sep="\t")

