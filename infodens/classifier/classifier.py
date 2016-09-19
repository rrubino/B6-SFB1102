'''
Created on Aug 23, 2016

@author: admin
'''
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


class Classifier:
    '''
    classdocs
    '''
        
    X = []
    y = []
       
    Xtrain = []
    ytrain = []
       
    Xtest = []
    ytest = []
       
    splitPercent = 0.25
    shuffle = True
       
    model = []
       
    n_foldCV = 0  # how many folds cross validation
    
    def __init__(self, dataX = None, datay = None):
        if ( dataX == []):
            self.model = []
        else:
            self.X = dataX
            self.y = datay

    def shuffle(self):
        pass   