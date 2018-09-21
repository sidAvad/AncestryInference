#!/bin/bash

set +o posix  

for ((j=0; j<=36; j++))
do
    for ((i=1; i<=22; i++))
    do
        sh create-Hapmix-files.sh ${j} ${i}
    done
done




