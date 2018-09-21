#This script takes in chr no and the snp data as arguments and prints the final interpolated recombination information 
#Update: The script now drops rows with missing values 
#Update: The script now writes snpIDS of dropped rows into a file as a side-effect 
import pandas as pd
import sys
import os 

hapmapFile_path = '/bscb/data/genetic_maps/HapMap_GRCh37/genetic_map_GRCh37_chr' + sys.argv[1] + '.txt'

snpinfoDF = pd.read_table(sys.argv[2], header=None,names=["Chr","Position(bp)","snpID"])
desired_snplist = snpinfoDF["Position(bp)"].tolist()

hapmapDF_all = pd.read_table(hapmapFile_path)
hapmapDF = hapmapDF_all[hapmapDF_all["Position(bp)"].isin(desired_snplist)]

mergeDF = pd.merge(snpinfoDF, hapmapDF,  on='Position(bp)',how='outer')[["snpID","Chr","Map(cM)","Position(bp)"]] 

#Interpolation of missing cM values:
DFinterpolated = mergeDF.interpolate()

#Write out the list of snpIDs that have NA Map(cM) values as a side effect of this script 
with open('snpNAids.txt', 'w') as f:
    print(DFinterpolated.snpID[pd.isnull(DFinterpolated).any(axis=1)].to_string(index=False),file=f)

#Print out the interpolated dataframe as the primary effect of this script 
print(DFinterpolated.dropna().reset_index(drop=True).to_string())




