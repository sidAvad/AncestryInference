#!/bin/bash

awk -F'\t' '{OFS="\t";ORS=" "}

	NR==FNR{ 
	arr[$1]++;
	next
}
{
	print $1,$2,$3,$4,$5,$6,$7,$8,$9
	for(i=1; i<=NF; i++) if ($i in arr ){
	a[i]++;
	}	
}
 
{ 
	for (i in a) printf "%s\t", $i; 
	printf "\n"
}' $1 $2 

