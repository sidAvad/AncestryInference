import pandas as pd
import numpy as np

##

def maxRow(x):
    '''
    
    Returns array with transformed rows. Rows are transformed with 1 in place of maximum value, and zeros elsewhere

    Args:
    x - Array to be transformed

    Returns:
    b - transformed array

    '''
    b = np.zeros_like(x)
    b[np.arange(len(x)), x.argmax(1)] = 1
    return(b)

##

def collapse_Array(inputarray,genetic_positions):

    '''
    returns array with identical rows collapsed into a block, with length of block appended
    
    Args:

    inputarray: input data as a numpy array containing MAP estimate at each locus e.g [[0,1,0],......,[1,0,0],....]
    genetic_positions : corresponding genetic positions for each locus as a numpy array

    Returns:
    
    array_collapsed : array with identical loci collapsed into a block, along with block lengths 

    '''

    block_elem = inputarray[0]
    array_collapsed = list()
    array_collapsed.append(block_elem) # initialize output list with first block 
    #print(array_collapsed)

    blocklengths = list()

    block_start = genetic_positions[0] # start position of first block

    for index,item in enumerate(inputarray):

        # IF block for whenever a new element is encountered in input array
        if not np.array_equal(item,block_elem): 
            block_elem = item #Assign new block element  
            block_end = genetic_positions[index-1] #Previous block end 
            block_length = block_end - block_start #Previous block length
            block_start = genetic_positions[index] #Next block start

            array_collapsed.append(block_elem) #Append new block element
            blocklengths.append(block_length) #Append previous block length
            #print(array_collapsed)

        # end of input IF block
        if index == len(inputarray)-1:
            block_end = genetic_positions[index]  #Current block end if loop has arrived at end of array 
            block_length = block_end - block_start #Compute final element block length
            blocklengths.append(block_length) #Append final block length (final block element already appended)

    assert len(blocklengths) == len(array_collapsed), "Outputs have different sizes"  
    
    return(np.column_stack((np.array(array_collapsed),np.array(blocklengths))))

####

##TODO:This function needs to append chromosome to outputed array, and reformat 0,1 values which are currently floats to ints in output  

def reformat_hapmixFile(inputdir, chromosome, simulation, outfile=None):

    '''
    Reformat HapMix output for a chromosome into ANCESTOR input format, 
    which is a table where each entry is a block of most likely ancestry 
    inference for each chromosome ( unphased ) paried with centimorgan 
    length of that block. Calls collapse_Array for the heavy lifing

    Args:
    inputdir - Path where all the simulation and chromsome folders for Hapmix
    output are stored
    output are stored
    outfile - write output dataframe to a file if specified
    chromosome - chromosome number to locate input file
    simulation - simulation nubmer to locae input file

    Returns: 
    arrayReform - dataframe containing transformed data.
    Writes arrayReform to outFile if specified 
    '''

    #Get input files to read in based on chromosome and simulation no. argument 
    inputfile =  inputdir + '/outputYC/' + str(simulation) + '/' + str(chromosome) + '/AA.LOCALANC.0.' + str(chromosome) 
    SNPdatafile =  inputdir + '/inputYC/' + str(simulation) + '/' + str(chromosome) + '/AAsnpfile.' + str(chromosome) +'.ORIG'

    #Store inputfile in array, compute MAP estimates of each row
    inputArray = np.loadtxt(inputfile)
    inputArray_maxrow = maxRow(inputArray)


    #get genetic positions and store it in an array
    genetic_positions = np.loadtxt(SNPdatafile,usecols = 2)
    assert len(genetic_positions) == len(inputArray_maxrow)

    #Collapse input array (identical rows get collapsed into blocks), total centimorgan length of blocks is stored
    inputArray_collapsed = collapse_Array(inputArray_maxrow,genetic_positions) 
    
    #Reformat the output of 'collapse_Array' to match ANCESTOR input format 
    arrayReform = np.array([np.array([0,1,x[3]]) if np.array_equal(x[:3], np.array([0,1,0]))
                        else np.array([1,1,x[3]]) if np.array_equal(x[:3],np.array([1,0,0])) 
                        else np.array([0,0,x[3]]) for x in inputArray_collapsed])
        

    #Write output (in append mode) if outfile is specified 
    if outfile is not None:
        f = open(outfile + '_' + str(simulation) + '.txt', "ab+")
        np.savetxt(f, arrayReform, fmt='%.5f')
        f.close
        
    return(arrayReform)

####
      



