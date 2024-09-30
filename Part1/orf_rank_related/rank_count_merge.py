count_dict = {}
with open("tvc_count_sum.txt") as f_in:
	for line in f_in:
		ele = line.strip().split("\t")
		count_dict[ele[0]] = ele[1]

with open("Gmax_275_Wm82.a2.v1.gene.out_total.faa.fai.total_rank") as f_in, open("gma_totalsmorf_rank_count.txt", "w") as f_out:
	for line in f_in:
		orf = line.strip().split("\t")[0]
		count = count_dict.pop(orf, "0") # if no orf in count_dict, count = "0"
		new_line = line.strip() + "\t" + count + "\n"
		f_out.write(new_line)

		