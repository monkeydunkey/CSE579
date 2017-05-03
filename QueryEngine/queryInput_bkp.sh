#!/bin/bash
echo -e "Please enter the terms you want to search separated by comma: and categories by ;"
read query
#Setting the default query for now
python KB/QuerySetup_bkp.py "structured svm;;"
#Calling the learnwts
#learnwts -i prog.mln -o ../test/trained.mln -t ../test/new-2.db -ne paperuses paperoutputpwd
dest='output'
#To change once we have MLN from Ashish
for filename in KB/tmp2/*.db; do
    outputFile="${filename/\KB\/tmp/$dest}.mln"
    infer -i prog_bkp.mln -r $outputFile -e $filename -q paperuses
    #Add a python file that adds the query terms to the output if that term was present in the paper
    python addRuleFile.py $outputFile "structured svm;;"
done
