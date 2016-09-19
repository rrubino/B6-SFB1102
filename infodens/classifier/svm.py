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
        
    def shuffle(self):
        indices = [i for i in range(len(self.y))]
        random.shuffle(indices)
        newX = np.zeros(self.X.shape)
        newy = np.zeros(self.y.shape)
        if len(self.X.shape) == 1:
            for i in range(len(self.y)):
                newX[i] = self.X[indices[i]]
                newy[i] = self.y[indices[i]]
                
        else:
            for i in range(len(self.y)):
                newX[i, :] = self.X[indices[i],:]
                newy[i] = self.y[indices[i]]
        self.X = newX
        self.y = newy

    def splitTrainTest(self):
        self.Xtrain, self.Xtest, self.ytrain, self.ytest = cross_validation.train_test_split(self.X, self.y, 
                                                                                            test_size=self.splitPercent,
                                                                                            random_state=0)
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
            
            
    def saveModel(self, location, saveAs):
        if os.path.exists(location):
            with open(location+'/'+saveAs, 'wb') as output:
                pickle.dump(self.model, output, pickle.HIGHEST_PROTOCOL)
        else:
            print ('Please enter a valid directory')
            
    def loadModel(self, location, savedAs):
        if os.path.exists(location):
            if os.path.isfile(location+'/'+savedAs):
                with open(location+'/'+savedAs, 'rb') as input:
                    self.model = pickle.load(input)
            else:
                print ('file does not exist')
        else:
            print ('Please enter a valid directory')
    

    def predict(self):
        return self.model.predict(self.Xtest)

    def evaluate(self):
        y_pred = self.predict()
        print ('Accuracy: ', accuracy_score(self.ytest, y_pred))
        #print ('Precision: ', average_precision_score(self.ytest, y_pred))
        print ('Recall: ', recall_score(self.ytest, y_pred))
        print ('F-score: ', f1_score(self.ytest, y_pred))
        

def startModel(classifierType, X, y):
    models = []
    if classifierType == 'svm':
        
        return SVM(X, y)
    elif classifierType == 'rf':
        return randomForest(X, y)
    elif classifierType == 'dt':
        return decisionTree(X, y)
    elif classifierType == 'nn':
        return neuralNetwork(X, y)
    elif classifierType == 'ab':
        return adaBoost(X,y)
    elif classifierType == 'ensemble':
        pass
    
    
        
from sklearn import datasets
import classifier
import adaBoost
import svm
import neuralNetwork
import randomForest
import ensemble
import decisionTree

if __name__ == '__main__':
    clfType = 'svm'    
    iris = datasets.load_iris()
    iris_X = iris.data
    iris_y = iris.target
    
    model = startModel(clfType, iris_X, iris_y)
    
    model.splitTrainTest()
    model.train()
    model.evaluate()