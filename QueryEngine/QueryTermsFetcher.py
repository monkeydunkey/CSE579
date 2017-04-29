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
import sys

sparql = SPARQLWrapper("http://dbpedia.org/sparql")
queryTerms = [x.strip() for x in sys.argv[0].split(',')]
expandedTerms = [].extend(queryTerms)
for i,q in enumerate(queryTerms):
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
print expandedTerms
