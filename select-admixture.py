# This is a script that prints a list of ids from the A and B populations input by the user. 
# Prints to stdout which is used by 02_pickcols.awk to subsample the input vcf. 
# TODO:popfile and vcfFile read in form sys.argv so they can be passed as arguments. ( hopefully named arguments ) 

import pandas as pd
import numpy as np 
import os
import sys

popfile = "/home/sna53/siddharth/AncestryInference/Data/relationships_w_pops_121708.txt"
vcfFile = "/home/sna53/siddharth/Data-Large/AncestryInference/unzipped/hapmap3_r2_b37_fwd_phased.all.vcf" #Don't read this in it is too large 

popsDF = pd.read_table(popfile)
header = list()

# Read in the header line 
with open(vcfFile) as fl:
  for i,line in enumerate(fl):
    if line.startswith("#CHR"):
      header =  line
      break

header = header.strip("\n").split("\t")

# Get ids in population list that are also in header; This is what we will be sampling from
popsList = popsDF.IID.tolist()
commonIDS = [id for id in popsList if id in set(header)]


#
popsDF_final = popsDF[popsDF["IID"].isin(commonIDS)]
A = sys.argv[1] 
B = sys.argv[2]

popsA = popsDF_final[popsDF_final.population == A]
popsB = popsDF_final[popsDF_final.population == B]
inputDF = pd.concat([popsA,popsB])
print(inputDF.IID.to_string())

#Get the locations of the columns we need and return a string of numbers (1-8 by default because of the header fields ) 

#d = {k:v for v,k in enumerate(header)}
#l = [str(i) for i in list(range(1,9))] + ([str(d[k]+1) for k in inputDF.IID.tolist()])  
#s = ' '.join(l)

#print(s)




