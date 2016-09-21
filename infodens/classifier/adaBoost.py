'''
Created on Aug 24, 2016

@author: admin
'''
#from trans.classifier import classifier
import classifier
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
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier

from sklearn.metrics import average_precision_score
from sklearn.metrics import accuracy_score
from sklearn.metrics import f1_score, recall_score


class AdaBoost:
    '''
    classdocs
    '''
   
    classifierName = 'Adaboost'
    n_estimators=20

    def __init__(self, X, y):
        '''
        Constructor
        ''' 
        classifier.__init__(self, X, y)
    

    def train(self):
        
        if self.n_foldCV <= 0:
            print ('No cross validation required. If required set the parameter to a positive number')
            clf = clf = AdaBoostClassifier(n_estimators=20)
            clf.fit(self.Xtrain, self.ytrain)
        else:
            #not yet implemented, so does the same thing as without cv                  
            clf.fit(self.Xtrain, self.ytrain)
            
        self.model = clf    
    