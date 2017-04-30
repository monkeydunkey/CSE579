# -*- coding: utf-8 -*-
"""
# Result is in this format--
isa(<word picked from document>,<word-meaning from wordnet>)
"""
import os
from wordnet_match_27 import wordnet_match
    
dir = os.getcwd()#os.path.dirname(__file__)
print dir
path =  dir + '/ReducedRuleFiles'
outputPath = dir + '/CompleteKB'
isAKB = open(outputPath + "/CompleteKB_WN.txt", 'w')
for filename in os.listdir(path):
    print (filename)      
    inFile = open(path + "/" + filename,'r')
    entities = [x.split(' | ')[2].strip() for x in inFile.readlines()]    
    #isAKB.write('Rules for file: ' + filename + '-\n \n')
    for entity in entities:
        try :
            priory_meaning_match = wordnet_match(entity)
        except IndexError:
            continue 
        except UnicodeDecodeError:
            continue
        #writting terms to txt-file
        meaningList = list()
        for item in priory_meaning_match[0]:
            names = item.lemma_names()
            meaningList.append(names[0])
        
        #formatting
        meaningList = [x.encode('utf-8') for x in meaningList]
        seen = set()
        result = []
        for i in meaningList:
            if i not in seen:
                seen.add(i)
                result.append(i)        
        #print result
        #break
        meaningList = result
        meaningList = " ".join(str(x) for x in meaningList)
        
        #print (meaningList)
        isAKB.write('isa(' + unicode(entity, "utf-8") + ',' + meaningList + ')\n')
        #isAKB.write('\n')
        inFile.close()
        

isAKB.close()

    
