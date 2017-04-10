# -*- coding: utf-8 -*-

import pandas as pd
import os
import numpy as np
import itertools
from scipy.spatial import distance


def euclideanMeasure(Matrix):
    for i in range(1,len(Matrix)):
        V1 = Matrix.iloc[i-1:i,1:len(Matrix.columns)]
        #print V1
        EuclideanMeasure = list()
        for j in range(1,len(Matrix)+1):
            V2 = Matrix.iloc[j-1:j,1:len(Matrix.columns)]
            dst = distance.euclidean(V1,V2)
            EuclideanMeasure.append(dst)
        break
    EuclideanMeasureDF = pd.DataFrame(EuclideanMeasure, index=None)
    Matrix = pd.concat([Matrix, EuclideanMeasureDF],ignore_index=True, axis = 1)
    return Matrix


def cosineMeasure(Matrix):
    for i in range(1,len(Matrix)):
        V1 = Matrix.iloc[i-1:i,1:len(Matrix.columns)]
        #print V1
        CosineMeasure = list()
        for j in range(1,len(Matrix)+1):
            V2 = Matrix.iloc[j-1:j,1:len(Matrix.columns)]
            dst = distance.cosine(V1,V2)
            CosineMeasure.append(dst)
        break
    CosineMeasureDF = pd.DataFrame(CosineMeasure, index=None)
    Matrix = pd.concat([Matrix, CosineMeasureDF],ignore_index=True, axis = 1)
    return Matrix

#Error in Mahalanobis
def mahalanobisMeasure(Matrix):
    for i in range(1,len(Matrix)):
        V1 = Matrix.iloc[i-1:i,1:len(Matrix.columns)]        
        V1 = np.array(V1).astype(np.float)
        V1 = list(itertools.chain(*V1))
        #print V1
        mahalanobisMeasure = list()
        for j in range(1,len(Matrix)+1):
            V2 = Matrix.iloc[j-1:j,1:len(Matrix.columns)]            
            V2 = np.array(V2).astype(np.float)
            V2 = list(itertools.chain(*V2))
            Z = zip(V1,V2)
            CovZ = np.cov(Z)
            m = 10^-6
            CovZ = CovZ + np.eye(CovZ.shape[1])*m
            try:
                INV = np.linalg.inv(CovZ)
                dst = distance.mahalanobis(V1,V2,INV)
            except KeyError:
                print "Inverse Not Possible!"
                print "Elements uncorrelated."
                dst = 9999
            
            mahalanobisMeasure.append(dst)
        break
    mahalanobisMeasureDF = pd.DataFrame(mahalanobisMeasure, index=None)
    Matrix = pd.concat([Matrix, mahalanobisMeasureDF],ignore_index=True, axis = 1)
    return Matrix



root = "E:/ASU_Sem_II/579_KRR/project/queryDocComparison\CSV"

for dirs in os.listdir(root): 
    Matrix = pd.read_csv(dirs)
    
    NewEuclideanMatrix = euclideanMeasure(Matrix)
    NewCosineMatrix = cosineMeasure(Matrix)
    #NewMahalanobisMatrix = mahalanobisMeasure(Matrix)

    del NewEuclideanMatrix[0]
    del NewCosineMatrix[0]
    #del NewMahalanobisMatrix[0]
    
    name = "cs.AI.Euclidean.csv"
    name2 = "cs.AI.Cosine.csv"  
    #name3 = "cs.AI.Mahalanobis.csv"
    
    NewEuclideanMatrix.to_csv(name)
    NewCosineMatrix.to_csv(name2)
    #NewMahalanobisMatrix.to_csv(name3)
    
    mostSimilar1  = np.array(NewEuclideanMatrix[301])
    mostSimilar2  = np.array(NewCosineMatrix[301])
    #mostSimilar3  = np.array(NewMahalanobisMatrix[301])
    
    TopMatchEuclidean = np.argsort(mostSimilar1)[:10]
    TopMatchCosine = np.argsort(mostSimilar2)[:10]
    #TopMatchMahalanobis = np.argsort(mostSimilar2)[:10]
    
    """
    DocList = pd.read_csv("DocList.cs.AI.csv")
    
    print "Similar Docs through Euclidean Measure"
    for index in TopMatchEuclidean:
        print(DocList[index])
    
    print "Similar Docs through Cosine Measure"
    for index in TopMatchEuclidean:
        print(DocList[index])
    """
    
    