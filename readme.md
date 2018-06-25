#*README - ANCESTRY INFERENCE v1.0*

This data is used to simulate children of recently admixed parents ( 1 generation back  ). The individuals from the raw data are the un-admixed individuals and are input into ped-sim to simulate admixed parents and then their children.

## RAW DATA:
-------------
Phased Hapmap Data for trio families split into files for parents and children found in the following directory
`/fs/cbsubscb09/storage/sushila/hapmap3/`
We need the input files for parents only:
`/fs/cbsubscb09/storage/sushila/hapmap3/hapmap3_r2_b37_fwd_phased.trio-parents.recode.vcf.gz`


NOTE : All files are copied into the Data/ directory. Data/unzipped contains unzipped versions of the data for viewing. 

## SHELL SCRIPTS:
--------------
`beagle2vcf.sh`:
Shell script to convert beagle-phased trio files into vcf formatted files, and split them into parent data only.

NOTE : DEPRECATED , we now have the phased vcf data separated into parents and children from Sushila.

`simulate-admix-pedigree.sh`:
1. ped-sim doesnt allow for choosing founder individuals. Since we need A-B A-B admixture, we need to run ped-sim multiple times with input vcfs that contain only 2 individuals.
2. This script automates this process so that we can do mulitple simulations.
3. Can work with AB/CD admixture.
4. Contains Python script that generates A/B C/D founder population, which then sends it through the appropriate number of ped-sim calls to finally generate a simulated individuals. 
5. Script should take in ABCD and nsim as arguments. We might want to return the intermediate output as well as the founder individuals as well 
 
NOTE : Looks like this is not needed as well. Amy implemented a new option in ped-sim. 

`select-admixture.py`

1. This is a script that prints a list of ids from the A and B populations input by the user. 
2. Prints to stdout which is used by `02_pickcols.awk` to subsample the input vcf. 
3. TODO:popfile and vcfFile read in form sys.argv so they can be passed as arguments. ( hopefully named arguments ) 
 
`prune-admixture.py`
1. Python script to select ped-sim simulations that are AB/AB admixture. Outpus a series of ped-sim ids to retain. 
2. Arguments : .ids file from ped-sim. 
3. Deprecated : Retains only founders and not entire pedigree. `03_prune-admixture.py` is current.

`pickcols.awk`
awk script that takes in two files, first one contains field names to pick as a list, second one is a vcf file to pick columns from

`prune-admixture.py`

Updated prune-admixture script that now outputs all ped-sim ids to be retained ( based on founders that have ABAB admixture ) 

`simulate-admix-pedigree.sh`

Mostly the same. Just uses `03_prine-admixture.py` and output file names are improved


