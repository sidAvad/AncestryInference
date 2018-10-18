##### Here we do the inference from hapmix for one pedigree input as argument:$1
##### For chromosome number input as argument:$2  
##### Note : the splits are generated for the entired pruned vcf from simulate-admix-pedigree.sh (i.e for all simulated pedigrees )
##### Update: We are now removing rows(snps) with missing values in teh genetic map files 
#!/bin/bash

set +o posix  

PROJ_DIR=~/siddharth/AncestryInference
SPLITS=~/siddharth/AncestryInference/Output/admixYC/Splits
PARENTDIR=~/siddharth/InferencePrograms/HapmixRelease/inputYC/$1
HAPMIXFILEPATH=${PARENTDIR}/$2
PRUNEDVCFFILEPATH=~/siddharth/AncestryInference/Output/admixYC/pedsimOutput/admix-YRI\|CEU-output_pruned.vcf

mkdir ${PARENTDIR}
mkdir ${HAPMIXFILEPATH} 

#Generate HapMix input files 
#~~~~~~~~~~~~~~~~~~#

#Awk one-liners to generate the Hapmix files for the particular chromosome
#~~~~~#


#Some preprocessing : merging the hapmap recombination data 
#for the chromosome with the rest of the snpfile information
#using a python script 'createMapfile.py'
awk '{print $1,$2,$3;}' <( grep -w "^$2" ${SPLITS}/$1_holdoutCEU.vcf ) | tr ' ' '\t' > snpData_nocM_$2.vcf 


#Population SNPfiles ( they need to be identical ) Note:createMapfile.py does interpolation and prunes out NA snps. 
awk '{print $2,$3,$4,$5;}' <( python pythonScripts/createMapfile.py $2 snpData_nocM_$2.vcf) | tail -n+2 |tr ' ' '\t'  >${HAPMIXFILEPATH}/CEUsnpfile.$2 
cp ${HAPMIXFILEPATH}/CEUsnpfile.$2 ${HAPMIXFILEPATH}/YRIsnpfile.$2
rm snpData_nocM_$2.vcf # Delete the snp information file


#Preprocessing for Population Genofiles: grep in the chromosome and grep out the snpids in snpNAids.txt from the holdout vcfs 

grep -vwF -f snpNAids.txt <(grep -w "^$2" ${SPLITS}/$1_holdoutCEU.vcf) > prunedChrom_holdoutCEU.vcf 
grep -vwF -f snpNAids.txt <(grep -w "^$2" ${SPLITS}/$1_holdoutYRI.vcf) > prunedChrom_holdoutYRI.vcf 

#Population Genofiles :
awk '{$1=$2=$3=$4=$5=$6=$7=$8=$9=""; print $0}' prunedChrom_holdoutCEU.vcf | tr -d ' /' > ${HAPMIXFILEPATH}/CEUgenofile.$2
awk '{$1=$2=$3=$4=$5=$6=$7=$8=$9=""; print $0}' prunedChrom_holdoutYRI.vcf | tr -d ' /' > ${HAPMIXFILEPATH}/YRIgenofile.$2

#Similar preprocessing for the inference vcf ( grep in chromosome and grep out bad snps)
grep -vwF -f snpNAids.txt <(grep -w "^$2\|#CHROM" ${SPLITS}/$1_infer.vcf) | sh selectColumn.awk | tail -n +2  > prunedChrom_infer.vcf

#Admixed individual geno, snp and individual files
#AAgenofile summed over the phase
awk -F "/" '{print $1+$2;}' <(awk '{$1=""; print $0}' prunedChrom_infer.vcf) > ${HAPMIXFILEPATH}/AAgenofile.$2
cp ${HAPMIXFILEPATH}/CEUsnpfile.$2 ${HAPMIXFILEPATH}/AAsnpfile.$2
echo -e "AA_0\tM\tAfricanEuropean" > ${HAPMIXFILEPATH}/AA.ind

#Creating rates file 
paste -d'\0' <(echo ":sites:") <(wc -l < ${HAPMIXFILEPATH}/AAgenofile.$2) > ${HAPMIXFILEPATH}/rates.$2
awk '{print $4}' ${HAPMIXFILEPATH}/AAsnpfile.$2 | tr '\n' ' ' >> ${HAPMIXFILEPATH}/rates.$2 
echo "" >> ${HAPMIXFILEPATH}/rates.$2 #this is for adding a newline
awk '{print $3}' ${HAPMIXFILEPATH}/AAsnpfile.$2 | tr '\n' ' ' >> ${HAPMIXFILEPATH}/rates.$2 

#Copy and edit params file according to chromosome input and simulation number input 
cp ~/siddharth/InferencePrograms/HapmixRelease/example.par ${HAPMIXFILEPATH}/params.par
sed -i "s/.22/.$2/g" ${HAPMIXFILEPATH}/params.par
sed -i "s/CHR\:22/CHR\:$2/g" ${HAPMIXFILEPATH}/params.par
sed -i "s/inputYC/inputYC\/$1\/$2/g" ${HAPMIXFILEPATH}/params.par
sed -i "s/outputYC/outputYC\/$1\/$2/g" ${HAPMIXFILEPATH}/params.par

#Clean-up
rm  prunedChrom* snp*
