#!/bin/bash
# usage: ./SmorfClassify.sh DIR
# to accomplish the pipeline, the existing files of each species are gathered in the DIR, including:
# genome.fai, gff, sORF.bed, cds.bed, intron.bed, mRNA.+.bed, mRNA.-.bed

home="/newlustre/home/pengzhao/"
wd="/newlustre/home/pengzhao/plant_sep/classification/"
bedtools="/newlustre/home/pengzhao/miniconda2/bin/bedtools"
spe=$1

cd ${wd}
cd ${spe}/

# Step 1 Prepare for processing data

# 1.1 5utr.bed & 3utr.bed
awk '{if($3=="five_prime_UTR") print $0}' ${spe}.gff > ${spe}.5utr.gff
awk '{if($3=="three_prime_UTR") print $0}' ${spe}.gff > ${spe}.3utr.gff

awk 'BEGIN{FS="\t|:|;|=";OFS="\t"} {print $1,$4-1,$5,$10,$6,$7}' ${spe}.5utr.gff > ${spe}.5utr.bed
awk 'BEGIN{FS="\t|:|;|=";OFS="\t"} {print $1,$4-1,$5,$10,$6,$7}' ${spe}.3utr.gff > ${spe}.3utr.bed

rm ${spe}.5utr.gff ${spe}.3utr.gff

# 1.2 intergenic.bed
awk 'BEGIN{OFS="\t"}{print $1,"0",$2,$1,"1","+"}' ${spe}.genome.fai > ${spe}.genome.+.bed
awk 'BEGIN{OFS="\t"}{print $1,"0",$2,$1,"1","-"}' ${spe}.genome.fai > ${spe}.genome.-.bed

${bedtools} subtract -a ${spe}.genome.+.bed -b ${spe}.mRNA.+.bed > ${spe}.intergenic.+.bed
${bedtools} subtract -a ${spe}.genome.-.bed -b ${spe}.mRNA.-.bed > ${spe}.intergenic.-.bed
cat ${spe}.intergenic.+.bed ${spe}.intergenic.-.bed > ${spe}.intergenic.bed
cat ${spe}.mRNA.+.bed ${spe}.mRNA.-.bed > ${spe}.mRNA.bed

rm ${spe}.genome.+.bed ${spe}.genome.-.bed ${spe}.intergenic.+.bed ${spe}.intergenic.-.bed


# Step 2 Generate overlapping files

# 2.1 completely overlapping
${bedtools} intersect -a ${spe}.sORF.bed -b ${spe}.mRNA.bed -u -f 1 -s > ${spe}.mRNA_cmpl.bed
${bedtools} intersect -a ${spe}.sORF.bed -b ${spe}.cds.bed -u -f 1 -s > ${spe}.cds_cmpl.bed
${bedtools} intersect -a ${spe}.sORF.bed -b ${spe}.5utr.bed -u -f 1 -s > ${spe}.5utr_cmpl.bed
${bedtools} intersect -a ${spe}.sORF.bed -b ${spe}.3utr.bed -u -f 1 -s > ${spe}.3utr_cmpl.bed
${bedtools} intersect -a ${spe}.sORF.bed -b ${spe}.intron.bed -u -f 1 -s > ${spe}.intron_cmpl.bed

# 2.2 both completely and partially overlapping
${bedtools} intersect -a ${spe}.sORF.bed -b ${spe}.mRNA.bed -u -s > ${spe}.mRNA_olp.bed
${bedtools} intersect -a ${spe}.sORF.bed -b ${spe}.cds.bed -u -s > ${spe}.cds_olp.bed
${bedtools} intersect -a ${spe}.sORF.bed -b ${spe}.5utr.bed -u -s > ${spe}.5utr_olp.bed
${bedtools} intersect -a ${spe}.sORF.bed -b ${spe}.3utr.bed -u -s > ${spe}.3utr_olp.bed
${bedtools} intersect -a ${spe}.sORF.bed -b ${spe}.intron.bed -u -s > ${spe}.intron_olp.bed

# 2.3 partially overlapping (UNNESSESARY)
# sort ${spe}.cds_olp.bed ${spe}.cds_cmpl.bed | uniq -u > ${spe}.cds_prt.bed
# sort ${spe}.5utr_olp.bed ${spe}.5utr_cmpl.bed | uniq -u > ${spe}.5utr_prt.bed
# sort ${spe}.3utr_olp.bed ${spe}.3utr_cmpl.bed | uniq -u > ${spe}.3utr_prt.bed
# sort ${spe}.intron_olp.bed ${spe}.intron_cmpl.bed | uniq -u > ${spe}.intron_prt.bed

# Step 3 Generate classification files

# 3.1 CLASS 1 Intergenic smORF
sort ${spe}.sORF.bed ${spe}.mRNA_olp.bed | uniq -u > ${spe}.CLASS1.bed

# 3.2 CLASS 2 Intergenic overlapping smORF
sort ${spe}.mRNA_olp.bed ${spe}.mRNA_cmpl.bed | uniq -u > ${spe}.CLASS2.bed

# 3.3 CLASS 3 Upstream smORF
sort ${spe}.mRNA_cmpl.bed ${spe}.5utr_olp.bed | uniq -d > ${spe}.CLASS3.bed

# 3.4 CLASS 4 Downstream smORF
sort ${spe}.mRNA_cmpl.bed ${spe}.3utr_olp.bed | uniq -d > ${spe}.CLASS4P.bed
sort ${spe}.CLASS4P.bed ${spe}.CLASS3.bed ${spe}.CLASS3.bed | uniq -u > ${spe}.CLASS4.bed
rm ${spe}.CLASS4P.bed

# 3.5 CLASS 5 Intron Overlapping smORF
sort ${spe}.mRNA_cmpl.bed ${spe}.intron_olp.bed | uniq -d > ${spe}.CLASS5P.bed
sort ${spe}.CLASS5P.bed ${spe}.CLASS3.bed ${spe}.CLASS3.bed | uniq -u > ${spe}.CLASS5Q.bed
sort ${spe}.CLASS5Q.bed ${spe}.CLASS4.bed ${spe}.CLASS4.bed | uniq -u > ${spe}.CLASS5.bed
rm ${spe}.CLASS5P.bed ${spe}.CLASS5Q.bed

# 3.6 CLASS 6 Others
sort ${spe}.mRNA_cmpl.bed ${spe}.CLASS3.bed | uniq -u > ${spe}.CLASS6P.bed
sort ${spe}.CLASS6P.bed ${spe}.CLASS4.bed | uniq -u > ${spe}.CLASS6Q.bed
sort ${spe}.CLASS6Q.bed ${spe}.CLASS5.bed | uniq -u > ${spe}.CLASS6.bed
rm ${spe}.CLASS6P.bed ${spe}.CLASS6Q.bed

# Step 4 Clear up & Generate a result file
mkdir ori_files olp_files
rm *mRNA.bed *intergenic.bed *utr.bed
mv *_olp.bed *_cmpl.bed olp_files/
mv *genome.fai *gff *sORF.bed *cds.bed *intron.bed *mRNA.+.bed *mRNA.-.bed ori_files/

cd ..
python ClassFiles2List.py ${spe}
