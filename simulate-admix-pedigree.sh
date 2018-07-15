#!/bin/bash
Data=/home/sna53/siddharth/Data-Large/AncestryInference/unzipped/
#Disable posix mode to allow process substitution to work 
set +o posix  

# Pick the CEU and YRI population columns from the 'parents' (TODO:also need to do this with children ) vcf file. 
sh pickcols.awk <(python select-admixture.py "CEU" "YRI" | awk '{print $2; end}' | sed '$d' - ) <( tail -n +6 ${Data}/hapmap3_r2_b37_fwd_phased.trio-parents.recode.vcf) | tr ' ' \\t > admix-YRI\|CEU-input.vcf 

MAP=/fs/cbsubscb09/storage/resources/genetic_maps/refined_mf.simmap #mapfile for ped-sim run 

# TODO: Create def file: to modify the number of simulations directly from this script
# Run ped-sim
/home/sna53/siddharth/ped-sim/ped-sim -d admix-YRI\|CEU-deffile.txt -m $MAP -i admix-YRI\|CEU-input.vcf -o admix-YRI\|CEU-output --founder_ids 


# Prune out identical founders from ped-sim output and write to _pruned.vcf file 
sh pickcols.awk <(python prune-admixture.py admix-YRI\|CEU-output.ids) <(cat admix-YRI\|CEU-output.vcf) | tr ' ' \\t > admix-YRI\|CEU-output_pruned.vcf

# NOTE : check output by running print-ids\&pops.py on the simid-outid.ids file ( e.g admix-YRI\|CEU-output.ids) and comparing it with the 
# header of the corresonding _pruned vcf file.  
