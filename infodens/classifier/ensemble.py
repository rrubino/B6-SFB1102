'''
Created on Aug 23, 2016

@author: admin
'''
#from trans.classifier import classifier
from classifier import Classifier
import scipy

import random
import numpy as np
import sklearn
from sklearn.svm import SVC
from sklearn import cross_validation
from sklearn.grid_search import GridSearchCV, RandomizedSearchCV
import os
import pickle
from sklearn.metrics import precision_recall_fscore_support
from sklearn.ensemble import RandomForestClassifier, VotingClassifier

from sklearn.metrics import average_precision_score
from sklearn.metrics import accuracy_score
from sklearn.metrics import f1_score, recall_score
from sklearn import tree


class Ensemble(Classifier):

    classifierName = 'Ensemble'
    listOfClassifiers = []
    
    def __init__(self, clfs):
        self.listOfClassifiers = clfs

    def train(self):
        
        if self.n_foldCV <= 0:
            print ('No cross validation required. If required set the parameter to a positive number')
            clf = VotingClassifier(estimators=[(x.classifierName, x) for x in self.listOfClassifiers], voting='hard')
            clf.fit(self.Xtrain, self.ytrain)
        else:
            #Not yet implemented
            clf = VotingClassifier(estimators=[(x.classifierName, x) for x in self.listOfClassifiers], voting='hard')
            
            clf.fit(self.Xtrain, self.ytrain)
            
        self.model = clf
