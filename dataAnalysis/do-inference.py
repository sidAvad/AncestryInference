#This script takes in simulation number and prints out the estimated p1 and p2 from the processed Hapmix results,
#the true values computed from ped-sim output,
#and the deviations (true - computed). The output is printed as a row of tab separated values 

from scipy.optimize import fsolve
import math
import pandas as pd 
import sys 

with open('/home/sna53/siddharth/InferencePrograms/HapmixRelease/outputYC/' + sys.argv[1] + '/AA.LOCALANC.' + sys.argv[1] + '.SUM') as f:
    content = f.readlines()

c1 = float(content[0].strip('\n').split('\t')[0])
c2 = float(content[0].strip('\n').split('\t')[1])

#Do the math
#~~~~~~~~~~#
b = -2*c1 - c2
c = c1
x = [(-b+math.sqrt(b**2 - 4*c))/2,(-b-math.sqrt(b**2 - 4*c))/2]
y = [None]*2 

y[0] = c1/x[0] 
y[1] = c1/x[1] 
############

#Get the true values 
#~~~~~~~~~~~~~~~~~~#

#Get pedsim-ids corresponding to split (sys.argv[1]) from Splits/infer.txt and append source population
#Get the true p1 and p2 calculations from the source population structure for the split 

CURRENTINFERENCEFILE = "/home/sna53/siddharth/AncestryInference/Output/admixYC/Splits/" + sys.argv[1] + "_infer.txt"
IDFILE = "/home/sna53/siddharth/AncestryInference/Output/admixYC/pedsimOutput/admix-YRI|CEU-output.ids" 
POPFILE = "/home/sna53/siddharth/AncestryInference/Data/relationships_w_pops_121708.txt"

popDF = pd.read_table(POPFILE)
idDF = pd.read_table(IDFILE,header=None,names=['simids','popids'])
inferDF = pd.read_table(CURRENTINFERENCEFILE, header=None, names=['simids'])

merge1 = pd.merge(idDF,popDF,left_on = 'popids', right_on='IID')
mergedDF = pd.merge(merge1, inferDF, on='simids')[['simids','popids','population']]

#print(mergedDF)
truep1 = sum(mergedDF.population.iloc[:2]=="CEU")/2
truep2 = sum(mergedDF.population.iloc[2:]=="CEU")/2
########

#compile allresults and print to stdout
resultsList = [sys.argv[1],y[0],x[0],x[1],y[1],truep1,truep2,truep1-y[0],truep2-x[0]]
print(*resultsList, sep ='\t')

#resultFrame = pd.DataFrame(data=[resultsList], columns = ['estp1', 'estp2' , 'altp1', 'altp2', 'truep1' ,'truep2' ])

