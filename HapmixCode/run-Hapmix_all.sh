#!/bin/bash
#!/usr/bin/perl -w  

for ((j=0; j<=36; j++))
do
    for ((i=1; i<=22; i++))
    do
        sed -i "s/CHR\./CHR\:/g" inputYC/${j}/${i}/params.par  #Correct the input files
        mkdir outputYC/${j} #Create the output directories mentioned in the input files
        mkdir outputYC/${j}/${i}
        perl bin/runHapmix.pl inputYC/${j}/${i}/params.par
    done
done
