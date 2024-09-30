rank_dict = {}
with open("potential_list.rank") as f_in:
	for line in f_in:
		elements = line.strip().split("\t")
		lenth = elements[1]
		rank = float(elements[2])
		if lenth not in rank_dict:
			rank_dict[lenth] = rank
		else:
			if rank > rank_dict[lenth]:
				rank_dict[lenth] = rank

with open("potential_list.rank.max","w") as f_out:
	for k,v in rank_dict.items():
		new_line = k + "\t" + str(v) + "\n"
		f_out.write(new_line)

