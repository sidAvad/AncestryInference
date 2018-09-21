import numpy as np 
import pandas as pd 
import math 

res = pd.read_table('Results/admixYC-results2.txt')

res["diff1"] = abs(res.p1est-res.p1)
res["diff2"] = abs(res.p2est-res.p2)
res["diff3"] = abs(res.p1est-res.p2)
res["diff4"] = abs(res.p2est-res.p1)

res = res.drop(['devp1','devp2','p1','p2'], axis=1)
print(res.head())

#Convert rows into a list of lists , find minimum two deviations then average
#~~~~~~~~
tosort = res.values.tolist()
sortedLists = [sorted(x) for x in tosort]
finalDeviations = [x[:2] for x in sortedLists]
avgDeviations = [sum(x)/2 for x in finalDeviations]
median = np.median(avgDeviations)
outliersList = [(ind,x) for ind,x in enumerate(avgDeviations) if (x >= median + (1.5)*np.std(avgDeviations))]

print(finalDeviations)
print(avgDeviations)
print(len(avgDeviations))
print(median)
final = sum(avgDeviations)/len(avgDeviations)
print(final)
print(outliersList)
#Get p1 and p2 inference deviations individually ( this might not make sense to do ) 
#~~~~~~~~

#p1deviations = [x[0] for x in finalDeviations]
#p2deviations = [x[1] for x in finalDeviations]
#print(sum(p1deviations)/len(p1deviations))
#print(sum(p2deviations)/len(p2deviations))
