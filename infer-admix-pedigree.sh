#!/bin/bash

PROJ_DIR=~/siddharth/AncestryInference
SPLITS=~/siddharth/AncestryInference/Output/admixYC/Splits

prunedVcfFilePath =  ${PROJ_DIR}/Output/admixYC/admix-YRI|CEU-output_pruned.vcf

# Takes a '_pruned' vcf and creates .txt split files in Output/admixYC/Splits/
python split-admixture.py prunedVcfFilePath


# Generate .vcf files from .txt split files in Output/admixYC/Splits/ (TODO:We do this for one split first ) 
sh pickcols.awk ${SPLITS}/0_infer.txt ${PROJ_DIR}/Output/admixYC/admix-YRI\|CEU-output_pruned.vcf >  ${SPLITS}/0_infer.vcf
sh pickcols.awk ${SPLITS}/0_holdout.txt ${PROJ_DIR}/Output/admixYC/admix-YRI\|CEU-output_pruned.vcf > ${SPLITS}/0_holdout.vcf

#Generate HapMix input files ( TODO:for chromosome 22 first ) 
#~~~~~~~~~~~~~~~~~~#

#Split holdout.vcf into CEU and YRI holdouts

sh pickcols.awk <(python split-holdout.py ${PROJ_DIR}/Output/admixYC/Splits/0_holdout.vcf "YRI") <(cat ${PROJ_DIR}/Output/admixYC/Splits/0_holdout.vcf | tr " " "\t") > ${PROJ_DIR}/Output/admixYC/Splits/0_holdoutYRI.vcf 

sh pickcols.awk <(python split-holdout.py ${PROJ_DIR}/Output/admixYC/Splits/0_holdout.vcf "CEU") <(cat ${PROJ_DIR}/Output/admixYC/Splits/0_holdout.vcf | tr " " "\t") > ${PROJ_DIR}/Output/admixYC/Splits/0_holdoutCEU.vcf 


#Just some harmless awking seding and greping fun ! :) 

grep 
CEUgenofile.22
YRIgenofile.22


CEUsnpfile.22
YRIsnpfile.22
AAgenofile.22
AAsnpfile.22
AA.ind
rates.22

# Run Hapmix 

# Run RFMix or LAMP LD 



