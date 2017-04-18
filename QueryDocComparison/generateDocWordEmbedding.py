# -*- coding: utf-8 -*-
# Using WORD2VEC Approach

import gensim
import re
import os
import csv
import pandas as pd

from nltk.corpus import stopwords

def embedding_matrix(path):
    
    s=set(stopwords.words('english'))
    embeddingMatrixDF = pd.DataFrame()

    for filename in os.listdir(path):
        DocMatrix = pd.DataFrame()
        f = open(path+"/"+filename,'r')
        content = f.read()
        contentWords = re.compile('\w+').findall(content)
        #removing englishwords
        contentWords = filter(lambda w: not w in s,contentWords)
        for word in contentWords:
            try:
                wordVector = model[word].reshape((1, 300))
                TempDF = pd.DataFrame(wordVector, index=None)    
                DocMatrix = pd.concat([DocMatrix,TempDF], axis=0, ignore_index=True)
            except KeyError:
                #print "not found word!", word
                continue
        centroid = DocMatrix.mean(axis=0)
        embeddingMatrixDF = pd.concat([embeddingMatrixDF,centroid.transpose()], axis=1, ignore_index=True)
    return embeddingMatrixDF   
    #300 X N matrix

#loading pretrained word2vec model
model = gensim.models.KeyedVectors.load_word2vec_format('E:/ASU_Sem_II/579_KRR/project/GoogleNews-vectors-negative300.bin/GoogleNews-vectors-negative300.bin', binary=True)

root = "E:/ASU_Sem_II/579_KRR/project/DataGrabber/data/txt"

# ITERATING OVER CATEGORICAL DIRS
for dirs in os.listdir(root):
    path = root+"/"+dirs
    #generates word embeddings for all documents in each folder and writes to csv
    Matrix = embedding_matrix(path)
    name = dirs+".csv"  
    MatrixTranspose = Matrix.transpose()
    MatrixTranspose.to_csv(name);    
    break #just for cs.AI papers
    
DocList = []
for dirs in os.listdir(root):
    path = root+"/"+dirs
    for filename in os.listdir(path):
        DocList.append(filename)
    break #just for cs.AI papers

#saving list of all docs in each folder 
#implemented just for cs.AI
myfile = open("DocList.cs.AI.csv", 'wb') 
wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
wr.writerow(DocList)

