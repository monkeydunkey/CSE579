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
from nltk import word_tokenize
from nltk import pos_tag
import re
import os

from collections import defaultdict
outputRelationTerms = ['present', 'presents', 'design', 'designed', 'provide', 'describe', 'achieve', 'introduce', 'report', 'create', 'construct', 'define', 'demonstrate', 'produce', 'publish']
usesRelationTerms = ['models', 'model', 'encode', 'encodes', 'using', 'uses', 'use', 'advance', 'apply', 'consider', 'fit', 'employ', 'incorporate', 'examine', 'utilize', 'found', 'require']
#There might be some special work required for this this
solvesRelationTerms = ['aims', 'aims to', 'solves', 'goal', 'aim', 'solve', 'solved', 'propose', 'build', 'hypothesis']
#Simpler regex: ((JJ.?)+\s)?(NN.?)+\s?
ADJ_NN_patt = re.compile("((JJ.?)+\s?)*((NN.?)+\s?)+((JJ.?)+\s?)*")

def reduceRule(rule):
    parts = map(lambda x: x.strip().lower(), rule.split(';'))
    if len(parts) < 3:
        return ''
    inAny = False
    #Checking for outputs type relation
    if any(t in parts[1] for t in outputRelationTerms):
        parts[1] = 'outputs'
        inAny = True
    elif any(t in parts[1] for t in usesRelationTerms):
        parts[1] = 'uses'
        inAny = True
    elif any(t in parts[1] for t in solvesRelationTerms):
        parts[1] = 'solves'
        inAny = True

    if inAny:
        parts[0] = 'The paper'
        parts[2] = '; '.join(parts[2:])
        return ' $ '.join(parts[:3])
    #Handling cases for solves type of relation
    solvesSpecialVerbs = ['is', 'was']
    paperIdentifier = [' us ', ' we ', ' our ']
    startingTerms = ['we', 'our']
    if parts[1] in solvesSpecialVerbs:
        if (any(t in parts[0] for t in paperIdentifier) or any(parts[0].startswith(st) for st in startingTerms))and (any(t in parts[0] for t in solvesRelationTerms) or any(t in ' '.join(parts[2:]) for t in solvesRelationTerms)):
            parts[0] = 'The paper'
            parts[1] = 'solves'
            parts[2] = '; '.join(parts[2:])
            parts[2] = parts[2].replace('to ', '')
            return ' $ '.join(parts[:3])
    return ''

def getInd(string, ind):
    prevSt = string[:ind].strip()
    if prevSt == "":
        return 0
    return len(string[:ind].strip().split(' '))

def matchPatt(patt, string, iterFlag = True):
    if iterFlag:
        iterTag = patt.finditer(string)
        indices = [(m.start(0), m.end(0)) for m in iterTag]
        return indices
    else:
        return patt.search(string)

def breakRulesPOS(rule):
    output = []
    if len(rule) == 0:
        return []
    parts = rule.split('$')
    #using the last part for breaking up the rule
    tokens = word_tokenize(parts[-1])
    posTags = [x[1] for x in pos_tag(tokens)]
    posTagsString = " ".join(posTags)
    indices = matchPatt(ADJ_NN_patt, posTagsString)
    minStart, maxEnd = len(rule), 0
    for indice in indices:
        st, end = indice
        stWord = getInd(posTagsString, st)
        minStart = min(minStart, stWord)
        endWord = getInd(posTagsString, end)
        maxEnd = max(maxEnd, endWord)
        term = " ".join(tokens[stWord: endWord])
        output.append(" | ".join([parts[0], parts[1], term]))
    if len(indices) > 1:
        term = " ".join(tokens[minStart: maxEnd])
        output.append(" | ".join([parts[0], parts[1], term]))
    return output

def resolvePropositions(rules, ind, rulesToResolve, ruleParts):
    # pattern to find and remove rules of the form L:, T:
    # This just basically identify some more meta information about the thing at hand
    #Older pattern " \w:"
    tagPatt = re.compile(" \w\s?:")
    #TODO we will find all the errors and corner cases only after the whole thing is run on a sizeable dataset
    resolvedRule = ""
    for r in rulesToResolve:
        terms = r.strip().split(" ")
        if len(terms) > 1 or tagPatt.search(r):
            if tagPatt.search(r) is None:
                resolvedRule += r
        else:
            r_pos = pos_tag([r.strip()])
            if "PRP" in r_pos[0][1]: #the tag is a proposition
                #Looping through the previous rules
                ruleFound = False
                for i in xrange(ind - 1, -1, -1):
                    tokens = word_tokenize(rules[i].split('$')[-1])
                    posTagsString = " ".join([x[1] for x in pos_tag(tokens)])
                    iterTag = matchPatt(ADJ_NN_patt, posTagsString, False)
                    if iterTag is not None:
                        stWord = getInd(posTagsString, iterTag.start(0))
                        endWord = getInd(posTagsString, iterTag.end(0))
                        resolvedRule += " ".join(tokens[stWord: endWord])
                        ruleFound = True
                        break
                if not ruleFound:
                    print 'There were no subsitute found for the proposition. Rule', rules[ind]
            elif "NN" in r_pos[0][1]: #the tag is a noun and their was more info encoded in respect to the noun that get affected by the action
                resolvedRule += r
            else:
                print 'The rule found does not satisfy the constraints', rules[ind]
    ruleParts[-1] = resolvedRule
    return "$".join(ruleParts)


def reduceRuleGroup(rule):
    lines = rule.split('\n')
    #this means there was no information generated for the sentence
    if len(lines) < 2:
        return ''
    reducedRules = map(reduceRule, lines[1:])
    return "\n".join(reducedRules)

DIR = "/Users/shashankbhushan/Documents/Github/cse579"
inFolder = "DataModelling/RuleFiles"
outFolder = "DataModelling/ReducedRuleFiles"
files = os.listdir(os.path.join(DIR, inFolder))
for i,f in enumerate(files):
    if "DS_Store" in f:
        continue
    print 'Reducing rules for file', f
    input_file_path = os.path.join(DIR, inFolder, f)
    output_file_path = os.path.join(DIR, outFolder,f)
    inputFile = open(input_file_path)
    rules = inputFile.read().split('\n\n')
    RuleGroups = filter(lambda x: len(x.strip()) > 2, map(reduceRuleGroup, rules))
    reducedRules = []
    for rules in RuleGroups:
        reducedRules.extend(rules.split("\n"))

    #Map Propositions to nouns
    for i in range(len(reducedRules)):
        ruleParts = reducedRules[i].split('$')
        lastRule = ruleParts[-1].strip().split(';')
        if len(lastRule) > 1:
            reducedRules[i] = resolvePropositions(reducedRules, i, lastRule, ruleParts)

    #POS tag based entity identification
    rules = []
    for rule in reducedRules:
        rules.extend(breakRulesPOS(rule))

    outFile = open(output_file_path, 'w')
    #Considering only those lines whose length is more than 4
    outFile.writelines('\n'.join(rules))
    outFile.close()
