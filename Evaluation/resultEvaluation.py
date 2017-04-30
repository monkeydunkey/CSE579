'''
This file reads through the results and outputs the results in comparison to the ground truth
Lets have 3 query terms. Also lets see if we can reduce the evaluation set to only 10 files
Query Format:- uses; outputs; solves
each of the terms in uses, outputs and solves should be separated by a comma
1. A high level one like 'neural network'
2. A high level one like 'neural network;Computer Vision;'
2. A high level one like 'neural network, discrete probability;Computer Vision;'
'''
import re
import os

rulePatt = re.compile("// \d.?\d*\s*paper\w*\(a1\) <=> query\w*\(a1\)")
folderPath = '../QueryEngine/test'
files = os.listdir(folderPath)
queryResults = open('queryResult', 'w')
for i,f in enumerate(files):
    if '.mln' in f:
        inputFilePath = os.path.join(folderPath, f)
        with open(inputFilePath, "r") as openfile:
            lines = openfile.readlines()
            relevantLines = filter(lambda x: rulePatt.search(x), lines)
            scores = map(lambda x: float(x.split('pa')[0].strip().split('//')[1].strip()), relevantLines)
            print 'For file', str(f), 'Rules found', len(relevantLines)
            if len(relevantLines) > 0:
                totalScore = reduce(lambda x, y: x+y, scores)
                queryResults.write(str(f) + ' : ' + str(totalScore/len(relevantLines)) + '\n')
queryResults.close()
