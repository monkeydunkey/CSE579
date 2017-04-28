#is a rule builder
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

COMMON_KB_DIR = "CommonKB.txt"
REDUCE_RULE_DIR = "DataModelling/ReducedRuleFiles"
DIR = "/Users/shashankbhushan/Documents/Github/cse579"

#TODO: Right now the common KB is built from scratch each time. Probably need to update it.
isAKB = open(COMMON_KB_DIR, 'w')
sparql = SPARQLWrapper("http://dbpedia.org/sparql")

files = os.listdir(os.path.join(DIR, REDUCE_RULE_DIR))
for i,f in enumerate(files):
    input_file_path = os.path.join(DIR, REDUCE_RULE_DIR, f)
    inFile = open(input_file_path)
    entities = [x.split(' | ')[2].strip() for x in inFile.readlines()]

    for entity in entities:
        print 'querying for entity', entity
        try:
            entityName = '_'.join(entity.replace(',', ' ').capitalize().split(' '))
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
                isAKB.write(entity + ' isa ' + result["Object"]["value"].encode('utf-8') + '\n')
        except Exception as e:
            print 'There was an error in parsing the query', e.message
isAKB.close()
