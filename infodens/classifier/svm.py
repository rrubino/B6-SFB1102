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
from sklearn.grid_search import GridSearchCV
import os
import pickle
from sklearn.metrics import precision_recall_fscore_support
from sklearn.ensemble import RandomForestClassifier
#from scipy.stats import randint as sp_randint
from sklearn.metrics import average_precision_score
from sklearn.metrics import accuracy_score
from sklearn.metrics import f1_score, recall_score
import time


class SVM(Classifier):
    '''
    classdocs
    '''

    classifierName = 'Support Vector Machine'
    C = 1.0
    k = 'linear'  #linear kernel
    max_iter = -1
    gamma = 'auto'

    def train(self):
        score = 'recall'
        tuned_parameters = [{'kernel': ['rbf'], 'gamma': [1e-3, 1e-4],
                 'C': [1, 10]},
                {'kernel': ['linear'], 'C': [1, 10, 100, 1000]}]
                
        print ('SVM Optimizing. This will take a while')
        start_time = time.time()
        clf = GridSearchCV(SVC(C=1), tuned_parameters,
                   scoring='%s_weighted' % score, n_jobs=self.threads)
        
        clf.fit(self.Xtrain, self.ytrain)
        print('Done with Optimizing. it took ', time.time() - start_time, ' seconds' )
                    
        self.model = clf
