'''
Created on Aug 25, 2016

@author: admin
'''

import os


import numpy as np


from sklearn import datasets
from classifier import Classifier
from adaBoost import AdaBoost
from svm import SVM
from neuralNetwork import NeuralNetwork
from randomForest import RandomForest
from ensemble import Ensemble
from decisionTree import DecisionTree
#from trans.svm import svm
#from trans.randomForest import RandomForest
#from trans.decisionTree import decisionTree
#from trans.neuralNetwork import neuralNetwork
#from trans.adaBoost import adaBoost




def startModel(classifierType, X, y):
    
    if classifierType == 'svm':        
        return SVM(X, y)
    elif classifierType == 'rf':
        return RandomForest(X, y)
    elif classifierType == 'dt':
        return DecisionTree(X, y)
    elif classifierType == 'nn':
        return NeuralNetwork(X, y)
    elif classifierType == 'ab':
        return AdaBoost(X,y)
    elif classifierType == 'ensemble':
        pass
    
    
        


if __name__ == '__main__':
    clfType = 'svm'    
    iris = datasets.load_iris()
    iris_X = iris.data
    iris_y = iris.target
    
    model = startModel(clfType, iris_X, iris_y)
    
    model.splitTrainTest()
    model.train()
    model.evaluate()