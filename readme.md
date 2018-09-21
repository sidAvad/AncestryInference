#This folder contains all the code for simulating admixture ( ~36 simulations ) as well as for inferring admixture proportions in parents using HapMix. We dont do grandparental admixture inference here. 

create-Hapmix-files.sh
    create the input files for HapMix

create-Hapmix-files_all.sh
    create the HapMix input files for all simulations and for all chromosomes 

infer-admix_all.sh
     Average all the HapMix results for each chromosome and then over all chromosomes for each simulation. Output is the averaged results for each simulation

pickcols.awk
    pick columns from a large text file according to a second file list        

run-Hapmix_all.sh
    run HapMix over all simulations and chromosomes

scratch.sh
    scratch file for shell code

selectColumn.awk
    selectColumns from a file according to hard coded pattern match
    
simulate-admix-pedigree.sh
    simulate admixture using ped-sim and then pruning the output 

split-admix-pedigree.sh
    create infer and holdout vcfs from simulate-admix-pedigree output
