from nltk.corpus import wordnet as wn
from collections import Counter

query = raw_input("search query:")
query_terms = query.split()
involved_terms = Counter(query_terms)
involved_meanings = []
priory_meanings = []

print(involved_terms)

for term in involved_terms:
    involved_meanings = involved_meanings + wn.synsets(term)
    priory_meanings.append(wn.synsets(term))

#priory_meanings.remove([])

print(involved_meanings)
print(priory_meanings)

cleared_term = []
while not len(priory_meanings) == 1:
    max_simi = -1
    max_pair = []
    max_meanings = []
    for term1 in priory_meanings:
        for term2 in priory_meanings:
            if not term1 is term2:
                max_term_simi = -1
                max_term_pair = []
                for meaning1 in term1:
                    for meaning2 in term2:
                        if max_term_simi < meaning1.path_similarity(meaning2):
                            max_term_simi = meaning1.path_similarity(meaning2)
                            max_term_pair = [term1, term2]
                            max_meaning_pair = [meaning1, meaning2]

                if max_simi < max_term_simi:
                    max_simi = max_term_simi
                    max_pair = max_term_pair
                    max_meanings = max_meaning_pair


    print (max_pair)
    print (max_meanings)

    if max_pair[0] in cleared_term and max_pair[1] in cleared_term:
        new_term = max_pair[0] + max_pair[1]
        cleared_term.remove(max_pair[0])
        cleared_term.remove(max_pair[1])
    elif max_pair[0] in cleared_term:
        max_pair[0].extend(max_meanings[1])
        new_term = max_pair[0]
        cleared_term.remove(max_pair[0])
    elif  max_pair[1] in cleared_term:
        max_pair[1].extend(max_meanings[0])
        new_term = max_pair[1]
        cleared_term.remove(max_pair[1])
    else:
        new_term = max_meanings
    cleared_term.append(new_term)
    priory_meanings.remove(max_pair[0])
    priory_meanings.remove(max_pair[1])
    priory_meanings.append(new_term)
    print(cleared_term)
    print(priory_meanings)
















