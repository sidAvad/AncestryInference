import pandas as pd
import numpy as np 
import os
import sys

#FILENAMES
popfile = "/home/sna53/siddharth/AncestryInference/Data/relationships_w_pops_121708.txt"
idfile = "/home/sna53/siddharth/AncestryInference/Output/admixYC/pedsimOutput/admix-YRI|CEU-output.ids"
vcfFile = sys.argv[1] 

#Files to Dataframes 
popsDF = pd.read_table(popfile)
idDF = pd.read_table(idfile,header=None)
idDF.columns = ['pedsimIDS','IID']
popIDS = pd.merge(popsDF, idDF)


#print(popsDF.head())
#print(idDF.head())
#print(popIDS.head())

# Read in the header line 
with open(vcfFile) as fl:
  for i,line in enumerate(fl):
    if line.startswith("#CHR"):
      header =  line
      break

header = header.strip("\n").split()

#Select elements that are CEU write to CEUlist ; select elements that are YRI and write to YRIlist

if sys.argv[2]=="CEU":
    CEUlist = popIDS[popIDS.population == "CEU"].pedsimIDS.tolist()
    print(*CEUlist,sep='\n')
elif sys.argv[2]=="YRI":
    YRIlist = popIDS[popIDS.population == "YRI"].pedsimIDS.tolist()
    print(*YRIlist,sep='\n')
else:
    print("No population given!")




