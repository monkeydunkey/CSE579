# -*- coding: utf-8 -*-
"""
# Result is in this format--
isa(<word-meaning from wordnet>,<word picked from document>)
"""
import os
from wordnet_match_27 import wordnet_match
    
dir = os.getcwd()#os.path.dirname(__file__)
print dir
path =  dir + '/ReducedRuleFiles'
outputPath = dir + '/CompleteKB'
isAKB = open(outputPath + "/CompleteKB.txt", 'w')
for filename in os.listdir(path):
    print (filename)      
    inFile = open(path + "/" + filename,'r')
    entities = [x.split(' | ')[2].strip() for x in inFile.readlines()]
    
    isAKB.write('Rules for file: ' + filename + '-\n \n')  
    for entity in entities:
        #print (entity)
        try :
            priory_meaning_match = wordnet_match(entity)
        except IndexError:
            continue 
        except UnicodeDecodeError:
            continue
        #writting terms to txt-file
        for item in priory_meaning_match[0]:
            names = item.lemma_names()
            for meaning in names:
                #print (meaning,names[0])
                isAKB.write('isa(' + meaning.encode('utf-8') + ',' + names[0].encode('utf-8') + ',' + entity.encode('utf-8') + ')\n')
    isAKB.write('\n')
    inFile.close()
    #break

#query = raw_input("search query:")
#print (priory_meaning_match)

isAKB.close()

    
