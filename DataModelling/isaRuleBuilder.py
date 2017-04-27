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


inFile = open("PixelInformationExtraction_POS_test.txt")
entities = [x.split(' | ')[2].strip() for x in inFile.readlines()]
isAKB = open("CommonKB.txt", 'w')

sparql = SPARQLWrapper("http://dbpedia.org/sparql")
for entity in entities:
    print 'querying for entity', entity
    entityName = '_'.join(entity.replace(',', ' ').capitalize().split(' '))
    #Does a simple DBpedia lookup to get the resources
    sparql.setQuery("""
        prefix dbpr: <http://dbpedia.org/resource/>

        select ?Predicate ?Object where {
        ?Subject ?Predicate ?Object
        filter(?Subject = dbpr:%s && !isLiteral(?Object))
        }
    """%entityName)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    #We are saving the url as a unique identifier, the terms in the query also needs to expanded in a similar fashion
    for result in results["results"]["bindings"]:
        isAKB.write(entity + ' isa ' + result["Object"]["value"].encode('utf-8') + '\n')
isAKB.close()
