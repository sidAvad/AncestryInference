import pandas as pd 
import math
import sys

#~~~~~~~~~~~~~#
def pruneOutput(pedsim_output,popfile, pedsim_idfile):
    #Function that takes the output vcf from pedsim, a lookup file for source populations and the id file from pedsim
    #to identify individuals in output vcf on input basis. 
    #Returns list containing all individuals form pedigrees that satisfy ABAB. 
    # We need to append population information to the .ids file, and return ped-sim sample ids ( or simulation runs ) that we retain
    popDF = pd.read_table(popfile)
    idDF = pd.read_table(pedsim_idfile,header=None,names=['simids','popids'])
    mergedDF = pd.merge(idDF,popDF,left_on = 'popids', right_on='IID')\

    #Iterate over mergedDf in blocks ( corresponding to simulation number ) and 
    #print only those ped sim ids where the founders are AB/AB admixed. Blocks are of size four = number of founders.
    mergedDF = mergedDF[['simids','popids','population']]\

    #Read in the header from the pedsim outputfile and store the values as a list
    h = pd.read_table(pedsim_output,nrows =1 , sep = '\t')
    headerlist = list(h.columns.values)\
    
    
    #Loop over founders forom the ids file as blocks of 4 and append the ids if ABAB holds.  
    blocks = math.ceil(float(len(mergedDF)/4))
    pruned_founders = []
    for block in range(1,blocks):\

        start = (block - 1)*4
        end = start + (4-1)\

        subset = mergedDF[start:(end+1)]\
        
        l = list(subset.population)
        if not(l[0]==l[1] or  l[2]==l[3]):
            simids = subset.simids.tolist()
            blockel = [x[:(x.find('_')+1)] for x in simids][0] 
            pruned_founders.append(blockel) #print everything before the underscore including the underscore
    
    #Select elements from header list if the founder portion of ped-sim id matches the pruned_founders             
    pruned_all = [x for x in headerlist if x[:(x.find('_')+1)] in pruned_founders]
    return pruned_founders, pruned_all
#~~~~~~~#

#Filenames
popfile= "~/siddharth/AncestryInference/Data/relationships_w_pops_121708.txt"
pedsim_idfile = "~/siddharth/AncestryInference/Results/admix60/admix60-output.ids"
pedsim_output = "/home/sna53/siddharth/AncestryInference/Results/admix60/admix60-output.vcf"

#Grab the results we need and pretty print
founders = pruneOutput(pedsim_output, popfile, pedsim_idfile)[0]
print(*founders, sep='\n'  )


