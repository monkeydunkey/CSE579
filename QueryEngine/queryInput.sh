#!/bin/bash
echo -e "Please enter the terms you want to search separated by comma: and categories by ;  the query has to be of the form paper uses; paper outputs; paper solves"
read query
#Setting the default query for now
python KB/QuerySetup.py $query
#Calling the learnwts
#learnwts -i prog.mln -o ../test/trained.mln -t ../test/new-2.db -ne paperuses paperoutputpwd
dest='output'
#To change once we have MLN from Ashish
for filename in KB/tmp/*.db; do
    outputFile="${filename/\KB\/tmp/$dest}.mln"
    learnwts -i prog.mln -o $outputFile -t $filename -ne paperuses,paperoutputs,papersolves
done
echo $query
python ../Evaluation/resultEvaluation.py $query
