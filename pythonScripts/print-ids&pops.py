# Input : .ids file from ped-sim run
# Output : .ids file with source populations appended

import sys 
import pandas as pd

IDFILE = sys.argv[1]
POPFILE = "/home/sna53/siddharth/AncestryInference/Data/relationships_w_pops_121708.txt"

popDF = pd.read_table(POPFILE)
idDF = pd.read_table(IDFILE,header=None,names=['simids','popids'])

mergedDF = pd.merge(idDF,popDF,left_on = 'popids', right_on='IID')
mergedDF = mergedDF[['simids','popids','population']]

print(mergedDF.to_string())

