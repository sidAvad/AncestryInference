#!/bin/bash

# To allow process substitution to work we need to disable posix mode
set +o posix  

# This part of the script picks the ASW and CEU population columns from the 'all' vcf file. 
sh pickcols.awk <(python 02_select-admixture.py "ASW" "CEU" | awk '{print $2; end}' | sed '$d' - ) <( tail -n +6 /home/sna53/siddharth/Data-Large/AncestryInference/unzipped/hapmap3_r2_b37_fwd_phased.all.vcf ) | tr ' ' \\t > admix60-input.vcf 

MAP=/fs/cbsubscb09/storage/resources/genetic_maps/refined_mf.simmap #mapfile for ped-sim run 

# TODO: Create def file: here you can modify the number of simulations 
# Run ped-sim
/home/sna53/siddharth/ped-sim/ped-sim -d admix60-deffile.txt -m $MAP -i admix60-input.vcf -o admix60-output --founder_ids 


# Pick ids from ped-sim 'outid' vcf file that correspond to ABAB founders and write to `outid_pruned` vcf file.
sh pickcols.awk <(python 03_prune-admixture.py admix60-output.ids) <(cat admix60-output.vcf) | tr ' ' \\t > admix60-output_pruned.vcf

# NOTE : check output by running 04_print-ids\&pops.py on the simid-outid.ids file ( e.g admix60-output.ids) and comparing it with the 
# header of the corresonding _pruned vcf file.  


