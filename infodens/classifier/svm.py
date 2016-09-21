'''
Created on Aug 23, 2016

@author: admin
'''
#from trans.classifier import classifier
import random
from .classifier import Classifier
import scipy
import numpy as np
import sklearn
from sklearn.svm import SVC
from sklearn import cross_validation
from sklearn.grid_search import GridSearchCV, RandomizedSearchCV
import os
import pickle
from sklearn.metrics import precision_recall_fscore_support
from sklearn.ensemble import RandomForestClassifier
#from scipy.stats import randint as sp_randint
from sklearn.metrics import average_precision_score
from sklearn.metrics import accuracy_score
from sklearn.metrics import f1_score, recall_score


class SVM(Classifier):
    '''
    classdocs
    '''

    classifierName = 'Support Vector Machine'
    C = 1.0
    k = 'linear'  #linear kernel
    max_iter = -1
    gamma = 'auto'
    
    def __init__(self, X, y):
        '''
        initialized from its super class
        '''
        Classifier.__init__(self, X, y)
        
    
                                                                                      
    def train(self):
        
        if self.n_foldCV <= 0:
            print ('No cross validation required. If required set the parameter to a positive number')
            clf = SVC(decision_function_shape='ovo')
            clf.fit(self.Xtrain, self.ytrain)
        else:
            score = 'recall'
            # Set the parameters by cross-validation
            tuned_parameters = [{'kernel': ['rbf'], 'gamma': [1e-3, 1e-4],
                     'C': [1, 10, 100, 1000]},
                    {'kernel': ['linear'], 'C': [1, 10, 100, 1000]}]
                    
                    
            clf = GridSearchCV(SVC(C=1), tuned_parameters, cv=self.n_foldCV,
                       scoring='%s_weighted' % score)
            
            clf.fit(self.Xtrain, self.ytrain)
            
        self.model = clf
            
            
    