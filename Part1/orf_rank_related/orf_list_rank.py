rank_dict = {}
with open("gma_totalsmorf_rank_count.txt") as f_in:
	for line in f_in:
		elements = line.strip().split("\t")
		orf = elements[0]
		rank = elements[1]
		lenth = elements[3]
		count = int(elements[4])
		len_rank = [lenth,rank,count]
		rank_dict[orf] = len_rank

i = 0
t = 0
with open("potential_list") as f_in, open("potential_list.rank","w") as f_out:
	for line in f_in:
		i += 1
		p = line.strip()
		p_dat = rank_dict[p]
		p_len = p_dat[0]
		p_rank = p_dat[1]
		p_count = p_dat[2]
		t += p_count

		new_line = p + "\t" + p_len + "\t" + p_rank + "\t" + str(p_count) + "\n"
		f_out.write(new_line)

with open("stat","w") as f_out:
	l_1 = "smORF:" + "\t" + str(i) + "\n"
	l_2 = "Total Rank:" + "\t" + str(t) + "\n"
	avg_rank = float(t)/i
	l_3 = "Average Count:" + "\t" + str(avg_rank) + "\n"
	f_out.write(l_1 + l_2 + l_3)




