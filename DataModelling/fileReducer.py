#Reduce the ground truth terms
'''
As the only lines which were included contains the words "our" or "we", we can safely assume
that the realtions or terms only contains knowledge about the paper and nothing else.
Surely we will miss out on knowledge which we can probably work on later.

The aim of this script is to programitically reduce the rules generated from the Information
Extraction tool and map these rules to a fixed set of relations

How to go about it
1. We can probably create a mapping of sort to maps relations or that which are close sematically
    probably by the realtion word's vector representation
2. The problem is also to reduce huge terms in the relation like: the discrete probability of the raw pixel values

The relations in which we are interested are:
1. Ouputs: The outputs or results obtained in the paper
2. Solves: What problem does the paper Solves
3. Uses: What all techniques are used in the paper

'''

from collections import defaultdict
outputRelationTerms = ['present', 'presents', 'design', 'designed', 'provide', 'describe']
usesRelationTerms = ['models', 'model', 'encode', 'encodes', 'using', 'uses', 'use', 'advance', 'apply', 'consider']
#There might be some special work required for this this
solvesRelationTerms = ['aims', 'aims to', 'solves', 'goal', 'aim', 'solve', 'solved', 'propose']

def reduceRule(rule):
    parts = map(lambda x: x.strip().lower(), rule.split(';'))
    if len(parts) < 3:
        return ''
    #Checking for outputs type relation
    if any(t in parts[1] for t in outputRelationTerms):
        parts[0] = 'The paper'
        parts[1] = 'outputs'
        return ';'.join(parts)
    elif any(t in parts[1] for t in usesRelationTerms):
        parts[0] = 'The paper'
        parts[1] = 'uses'
        return ';'.join(parts)
    elif any(t in parts[1] for t in solvesRelationTerms):
        parts[0] = 'The paper'
        parts[1] = 'solves'
        return ';'.join(parts)

    #Handling cases for solves type of relation
    solvesSpecialVerbs = ['is', 'was']
    paperIdentifier = [' us ', ' we ', ' our ']
    startingTerms = ['we', 'our']
    if parts[1] in solvesSpecialVerbs:
        if (any(t in parts[0] for t in paperIdentifier) or any(parts[0].startswith(st) for st in startingTerms))and (any(t in parts[0] for t in solvesRelationTerms) or any(t in ' '.join(parts[2:]) for t in solvesRelationTerms)):
            parts[0] = 'The paper'
            parts[1] = 'solves'
            return ';'.join(parts)
    return ''

def reduceRuleGroup(rule):
    lines = rule.split('\n')
    #this means there was no information generated for the sentence
    if len(lines) < 2:
        return ''
    return '\n'.join(map(reduceRule, lines[1:]))

inFilePath = 'PixelInformationExtraction_reduced.txt'
inputFile = open(inFilePath)
rules = inputFile.read().split('\n\n')
reducedRules = filter(lambda x: len(x.strip()) > 2, map(reduceRuleGroup, rules))

outFile = open('PixelInformationExtraction_last.txt', 'w')
#Considering only those lines whose length is more than 4
outFile.writelines('\n'.join(reducedRules))
outFile.close()
