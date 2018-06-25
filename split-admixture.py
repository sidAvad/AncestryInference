import pandas as pd 
import math
import sys
import importlib

pr = importlib.import_module('prune-admixture')


#Filenames
popfile= "~/siddharth/AncestryInference/Data/relationships_w_pops_121708.txt"
pedsim_idfile = "~/siddharth/AncestryInference/Results/admix60/admix60-output.ids"
pedsim_output = "/home/sna53/siddharth/AncestryInference/Results/admix60/admix60-output.vcf"

     
def getHoldoutIds(prunedFounders, founderNo):
    #Note prunedFounders should be a list not a pretty printed list. 
    #idDF = pd.read_table(prunedFounders,header=None,names=['simids','popids'])
    result = prunedFounders.pop(founderNo-1)
    
    return(prunedFounders, result)

prunedFounders = pr.pruneOutput(pedsim_output, popfile, pedsim_idfile)[0]
print(getHoldoutIds(prunedFounders,5))
