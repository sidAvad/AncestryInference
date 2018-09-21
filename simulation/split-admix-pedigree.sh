#NOTE: ALWAYS RUN FROM THE SPLITS DIRECTORY 
#Here we create separate out each simulated pedigree into _holdout and _infer vcfs.
#!/bin/bash

set +o posix  

PROJ_DIR=~/siddharth/AncestryInference
SPLITS=~/siddharth/AncestryInference/Output/admixYC/Splits
HAPMIXFILEPATH=~/siddharth/AncestryInference/Output/admixYC/HapmixInput
PRUNEDVCFFILEPATH=~/siddharth/AncestryInference/Output/admixYC/pedsimOutput/admix-YRI\|CEU-output_pruned.vcf

# Takes a '_pruned' vcf and creates .txt split files in Output/admixYC/Splits/

python ${PROJ_DIR}/pythonScripts/split-admixture.py ${PRUNEDVCFFILEPATH}


# Generate .vcf files from .txt split files in Output/admixYC/Splits/
# Use pickcols.awk to select colums in .txt file from the pruned .vcf file
# TODO: loop over all .txt files in SPLITS path and create vcfs.

for ((i=0; i<=36; i++))
do
    #Split the pruned vcf into infer and holdout vcfs
    sh ${PROJ_DIR}/pickcols.awk ${SPLITS}/${i}_infer.txt ${PRUNEDVCFFILEPATH} > ${SPLITS}/${i}_infer.vcf
    sh ${PROJ_DIR}/pickcols.awk ${SPLITS}/${i}_holdout.txt ${PRUNEDVCFFILEPATH} > ${SPLITS}/${i}_holdout.vcf
    #Create Holdout sets for both populations
    sh ${PROJ_DIR}/pickcols.awk <(python ${PROJ_DIR}/pythonScripts/split-holdout.py ${SPLITS}/${i}_holdout.vcf "CEU") <(cat ${SPLITS}/${i}_holdout.vcf) > ${SPLITS}/${i}_holdoutCEU.vcf
    sh ${PROJ_DIR}/pickcols.awk <(python ${PROJ_DIR}/pythonScripts/split-holdout.py ${SPLITS}/${i}_holdout.vcf "YRI") <(cat ${SPLITS}/${i}_holdout.vcf) > ${SPLITS}/${i}_holdoutYRI.vcf
done



