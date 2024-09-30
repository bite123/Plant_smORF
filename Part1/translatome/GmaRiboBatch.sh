#!/bin/bash
# usage: ./GmaRiboBatch.sh N
# to extract a smORF list and its sequences from Total smORF, build a database to search Ribo-seq data, count and merge to the final matrix
# ENSURE conda activate cnigeome

prop=$1
home="/newlustre/home/pengzhao"
wd="/newlustre/home/pengzhao/translatome_dl"
scrp="/newlustre/home/pengzhao/translatome_dl/batch_script"
gma="/newlustre/home/pengzhao/plant_sep/gma_total_smORF"

cd ${wd}

# Step 1 Extracting the sequences of target smORFs

# 1.1 getting list
python ${scrp}/rank_cut_list.py ${prop}

# 1.2 filtering list
sort ${prop}_list ${gma}/blast_filt/Gmax_275_Wm82.a2.v1.gene.out_total.faa.fai.parse_list ${gma}/blast_filt/Gmax_275_Wm82.a2.v1.gene.out_total.faa.fai.parse_list | uniq -u > ${prop}_f_list

# 1.3 getting sequence
python ${scrp}/FastaExtract_update.py ${gma}/Gma_totalORF.v1.fna ${prop}_f_list
rm ${prop}_f_list.unextracted
mv ${prop}_f_list.extracted ${prop}_orf.fasta

# Step 2 Using bwa

# 2.1 building database
mkdir ${home}/database/gma_orf_db/orf_${prop}/
bwa index -p ${home}/database/gma_orf_db/orf_${prop}/orf_${prop} ${prop}_orf.fasta

# 2.2 aligning
for file in `ls gma`
do
	bwa aln ${home}/database/gma_orf_db/orf_${prop}/orf_${prop} gma/${file} -f ${file}.orf_${prop}.sai
	bwa samse ${home}/database/gma_orf_db/orf_${prop}/orf_${prop} ${file}.orf_${prop}.sai gma/${file} -f ${file}.orf_${prop}.sam
	samtools view -S ${file}.orf_${prop}.sam -bF 4 -o ${file}.orf_${prop}.bam
	${home}/miniconda2/bin/bedtools bamtobed -i ${file}.orf_${prop}.bam > ${file}.orf_${prop}.bed
	rm ${file}.orf_${prop}.sai ${file}.orf_${prop}.sam ${file}.orf_${prop}.bam
done

# Step 3 Count and merge

# 3.1 arranging files
mv ${prop}_list ${prop}_f_list batch_orflist/
mv ${prop}_orf.fasta batch_fasta/
for file in `ls *.orf_${prop}.bed`
do
	awk '{print $1,$4}' ${file} > ${file}.list
done
mv *.orf_${prop}.bed batch_bed/
mkdir orf_${prop}
mv *.orf_${prop}.bed.list orf_${prop}

# 3.2 counting
cd orf_${prop}
for file in `ls *.list`
do
	clist=${wd}/batch_clist/${file:0:27}.c.bed.list
	sort -t " " -k 2 ${file} ${clist} ${clist} | uniq -f 1 -u | awk '{print $1}' | sort | uniq -c | awk 'BEGIN{OFS="\t"}{print $2,$1}' > ${file:0:27}.orf_${prop}.count
done
rm *.list
cd ..

# 3.3 merging files
python ${scrp}/MergeMatrix.py orf_${prop}
