#!/bin/bash

#Average the results of each chromosome and write to one file (we ignore zero becuase that's already done )
for ((j=1; j<=36; j++))
do
    rm ~/siddharth/InferencePrograms/HapmixRelease/outputYC/${j}/AA.LOCALANC.${j}.ALLCHROM # remove file if it already exists .
    for ((i=1; i<=22; i++))
    do
        cat ~/siddharth/InferencePrograms/HapmixRelease/outputYC/${j}/${i}/AA.LOCALANC.0.${i} | awk '{for (i=1;i<=NF;i++){a[i]+=$i;}} END {for (i=1;i<=NF;i++){printf a[i]/NR; printf "\t"};printf "\n"}'  >> ~/siddharth/InferencePrograms/HapmixRelease/outputYC/${j}/AA.LOCALANC.${j}.ALLCHROM #average the output probabilities for each chromosome and append to allchrom file   
    done

    #Remove any empty lines ( chrom 14 has a problem)
    sed -i '/^$/d' ~/siddharth/InferencePrograms/HapmixRelease/outputYC/${j}/AA.LOCALANC.${j}.ALLCHROM
    
    #Average over all chromosomes
    cat ~/siddharth/InferencePrograms/HapmixRelease/outputYC/${j}/AA.LOCALANC.${j}.ALLCHROM | awk '{for (i=1;i<=NF;i++){a[i]+=$i;}} END {for (i=1;i<=NF;i++){printf a[i]/NR; printf "\t"};printf "\n"}'  > ~/siddharth/InferencePrograms/HapmixRelease/outputYC/${j}/AA.LOCALANC.${j}.SUM  


done
