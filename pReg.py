import pandas as pd 
import math
import sys

pedsimIDFILE = "~/siddharth/AncestryInference/Results/admix60/admix60-output.ids"
idDF = pd.read_table(pedsimIDFILE,header=None,names=['simids','popids'])


