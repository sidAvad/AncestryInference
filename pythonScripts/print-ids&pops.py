# Input : .ids file from ped-sim run
# Output : .ids file with source populations appended
# Update ( 09/20/2018) : pruned (only admixed pairings) .ids file with source populations appended ( look at Update section ) 


import sys 
import pandas as pd
import math 

IDFILE = sys.argv[1]
POPFILE = "/home/sna53/siddharth/AncestryInference/Data/relationships_w_pops_121708.txt"

popDF = pd.read_table(POPFILE)
idDF = pd.read_table(IDFILE,header=None,names=['simids','popids'])

mergedDF = pd.merge(idDF,popDF,left_on = 'popids', right_on='IID')
mergedDF = mergedDF[['simids','popids','population']]

#print(mergedDF.to_string())




#~~~~~~~~~~#
#Update: 09/20/2018 - We now prune the output to include only admixed pairings 
           
   
#Loop over founders from the ids file as blocks of 4 and append the ids if not AAAA or not BBBB holds.  
#Outputs pruned Dataframe with only admixed pairings 
blocks = math.ceil(float(len(mergedDF)/4))
pruned_founders = []
for block in range(1,blocks):\

    start = (block - 1)*4
    end = start + (4-1)\

    subset = mergedDF[start:(end+1)]\
    
    l = list(subset.population)
    if not (l.count(l[0])==len(l)):
        simids = subset.simids.tolist()
        blockel = [x for x in simids]
        print(blockel)
        pruned_founders = pruned_founders + blockel 


print(pruned_founders)
mergedDFpruned=mergedDF[mergedDF.simids.isin(pruned_founders)]
print(mergedDFpruned.to_string())


