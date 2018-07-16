import sys

#Filename
pedsim_output_pruned = sys.argv[1] 
     
h = pd.read_table(pedsim_output_pruned,nrows =1 , sep = '\t')
headerlist = list(h.columns.values)
prunedAll = headerlist[9:-1]

prunedFounders = list(set([x[:(x.find('_')+1)] for x in prunedAll])) # get the identifier correposing to founders set because we want unique founders from the entire pruned output header

def getHoldoutIds(prunedFounders):
    #Writes _infer.txt and _holdout.txt files as a side effect. 
    #Returns dictionaries which is pretty useless. Was being lazy.
    dictPopped = {} 
    dictRetained= {} 

    for i in range(len(prunedFounders)):
        popped = prunedFounders[i] 
        retained = prunedFounders[:i] + prunedFounders[i+1:]
        retainedAll = [x for x in prunedAll if x[:(x.find('_')+1)] in retained] # get entry from pruned all if founder part of id matches correponding list
        poppedAll = [x for x in prunedAll if x[:(x.find('_')+1)] in popped] # get entry from pruned all if founder part of id matches correponding list
        dictPopped[i] = poppedAll 
        dictRetained[i] = retainedAll
        
        #Write out infer and holdout files which contains the ids as a list to run pickcols.awk on and generate corresponding vcf files.See infer-admix-pedigree.sh 
        with open('%s_infer.txt'% i, 'w') as f1, open('%s_holdout.txt' % i,'w') as f2 :
            print(*poppedAll,sep='\n',file=f1)
            print(*retainedAll, sep='\n',file=f2)
            
    return(dictRetained, dictPopped)

#We make a call to getHoldoutIds for the side effect of writing out split files 
r = getHoldoutIds(prunedFounders)

 
