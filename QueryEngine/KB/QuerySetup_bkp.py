#This file setups the KB for each of the paper
'''
Sample Query:
sparql.setQuery("""
    prefix dbpr: <http://dbpedia.org/resource/>

    select ?Predicate ?Object where {
      ?Subject ?Predicate ?Object
      filter(?Subject = dbpr:Deep_learning && !isLiteral(?Object))
    }
""")
'''
from SPARQLWrapper import SPARQLWrapper, JSON
import os
import sys

ERR_FILE = open('ERR_FILE', 'a')
ruleType = ['uses', 'outputs', 'solves']

sparql = SPARQLWrapper("http://dbpedia.org/sparql")
queryTerms = [x.strip() for x in sys.argv[1].split(';')]
expandedTerms = [map(lambda z: z.strip(), y) for y in [x.split(',') for x in queryTerms]]

impOneWord = ['lstm', 'svm', 'ensemble', 'ann', 'softmax', 'nlp', 'srl', 'corpora', 'dropout', 'encoder', 'nmt',
              'cnn', 'rnn', 'charcnn', 'oov', 'oob', 'dpg', 'net2net', 'imagenet', 'iclr','rmsprop', 'dqn',
              'amn', 'epoch', 'conv', 'nms', 'jaccard', 'ssd', 'grams', 'sgd', 'image', 'sound', 'voice',
              'segmentation', 'roi', 'sds', 'entropy', 'correlation', 'subnet', 'pixel', 'photo', 'k3', 'video',
              'fcn', 'pascal', 'nyudv2', 'googlenet', 'torch', 'adam', 'cnmem', 'dni', 'bptt', 'cdni', 'gan', 'auc',
              'sigmoid']

print "Gathering the expansions from DBPedia"
for i,q in enumerate(expandedTerms):
    for term in q:
        try:
            entityName = '_'.join(q.replace(',', ' ').capitalize().split(' '))
            #Does a simple DBpedia lookup to get the resources
            sparql.setQuery("""
                prefix dbpr: <http://dbpedia.org/resource/>

                select ?Predicate ?Object where {
                ?Subject ?Predicate ?Object
                filter(?Subject = dbpr:%s && !isLiteral(?Object))
                }
            """%entityName.replace('\'',''))
            sparql.setReturnFormat(JSON)
            results = sparql.query().convert()
            #We are saving the url as a unique identifier, the terms in the query also needs to expanded in a similar fashion
            for result in results["results"]["bindings"]:
                expandedTerms.append(result["Object"]["value"].encode('utf-8'))
        except Exception as e:
            #Allowing a silent fail as the script output is to used by the bash script calling it.
            print term
            ERR_FILE.write('There was an error in processing ' + term + ' ' + e.message)
print "Terms fetched"

expandedTerms = [map(lambda z: 'query'+ruleType[i]+'("'+ z.replace('-','_') +'")\n', y) for i, y in enumerate(expandedTerms)]
#Flatteting the output
expandedTerms = [item for sublist in expandedTerms for item in sublist]

print "Setting the KBs"
DIR = os.getcwd()
KB_DIR = "KB"
TMP_DIR = "tmp2"
RED_RULE_DIR = os.path.join(DIR, KB_DIR, "ReducedRuleFiles")

CommonKB = open(os.path.join(DIR, KB_DIR, "CommonKBFiltered.txt"))
commonRules = map(lambda x: x.replace('-','_'), CommonKB.readlines())
CommonKB.close()

paperRules = set()
files = os.listdir(RED_RULE_DIR)
for i,f in enumerate(files):
    if '.DS_Store' in f:
        continue
    input_file_path = os.path.join(RED_RULE_DIR, f)
    inputFile = open(input_file_path)
    output_file_path = os.path.join(DIR, KB_DIR, TMP_DIR, f+'.db')
    outputFile = open(output_file_path, 'w')
    outputFile.writelines(commonRules)

    for line in inputFile.readlines():
        linePart = line.split(' | ')

        if (len(linePart[2].split(' ')) < 2 and not any(x in linePart[2].lower() for x in impOneWord)) or '=' in linePart[2] or len(linePart[2].split(' ')) > 3:
            continue
        ruleToWrite = 'paper'+linePart[1].strip()+'(P'+ f.replace('.','_') +', "'+linePart[2].strip().replace('-','_')+'")\n'
        if ruleToWrite not in paperRules:
            outputFile.write(ruleToWrite)
            paperRules.add(ruleToWrite)
    inputFile.close()
    outputFile.writelines(expandedTerms)
    outputFile.close()
