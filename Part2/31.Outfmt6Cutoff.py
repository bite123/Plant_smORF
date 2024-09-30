# usage: python 31.Outfmt6Cutoff.py --input_outfmt6 --output --similarity --query_ratio --subject_ratio --query_length_file --subject_length_file
# Thise script parses the BLAST result, and retain the results by three cutoffs:
# 1) the alignment similarity
# 2) the ratio of aligning length of the query
# 3) the ratio of aligning length of the subject
# All of the cutoffs are optional.

import sys
import argparse

parser = argparse.ArgumentParser(description='Parsing blast result with cutoffs')
parser.add_argument('--input_outfmt6', '-i', required=True)
parser.add_argument('--output', '-o', required=True)
parser.add_argument('--similarity', '-s', required=False)
parser.add_argument('--query_ratio', '-m', required=False)
parser.add_argument('--subject_ratio', '-n', required=False)
parser.add_argument('--query_length_file', '-u', required=False)
parser.add_argument('--subject_length_file', '-v', required=False)
ARGS = parser.parse_args()

if ARGS.query_ratio:
	qlen_dict = {}
	with open(ARGS.query_length_file) as f_in:
		for line in f_in:
			elements = line.split("\t")
			qlen_dict[elements[0]] = int(elements[1])

if ARGS.subject_ratio:
	slen_dict = {}
	with open(ARGS.subject_length_file) as f_in:
		for line in f_in:
			elements = line.split("\t")
			slen_dict[elements[0]] = int(elements[1])

with open(ARGS.input_outfmt6) as f_in, open(ARGS.output, "w") as f_out:
	for line in f_in:
		label = 1
		elements = line.split("\t")
		if ARGS.similarity:
			if float(elements[2]) < float(ARGS.similarity):
				label = 0
		if ARGS.query_ratio:
			if int(elements[3])/qlen_dict[elements[0]] < float(ARGS.query_ratio):
				label = 0
		if ARGS.subject_ratio:
			if int(elements[3])/slen_dict[elements[0]] < float(ARGS.subject_ratio):
				label = 0			
		if label:
			f_out.write(line)

