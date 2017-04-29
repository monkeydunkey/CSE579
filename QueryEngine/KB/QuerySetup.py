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

expandedTerms = [map(lambda z: 'query'+ruleType[i]+'("'+ z +'")\n', y) for i, y in enumerate(expandedTerms)]
#Flatteting the output
expandedTerms = [item for sublist in expandedTerms for item in sublist]

print "Setting the KBs"
DIR = os.getcwd()
KB_DIR = "KB"
TMP_DIR = "tmp"
RED_RULE_DIR = os.path.join(DIR, KB_DIR, "ReducedRuleFiles")

CommonKB = open(os.path.join(DIR, KB_DIR, "CommonKB.txt"))
commonRules = CommonKB.readlines();
CommonKB.close()
files = os.listdir(RED_RULE_DIR)
for i,f in enumerate(files):
    input_file_path = os.path.join(RED_RULE_DIR, f)
    output_file_path = os.path.join(DIR, KB_DIR, TMP_DIR, f+'.db')

    inputFile = open(input_file_path)
    outputFile = open(output_file_path, 'w')
    outputFile.writelines(commonRules)
    for line in inputFile.readlines():
        linePart = line.split(' | ')
        outputFile.write('paper'+linePart[1].strip()+'("'+linePart[2].strip()+'")\n')

    outputFile.writelines(expandedTerms)
    inputFile.close()
    outputFile.close()
