'''
Created on Aug 23, 2016

@author: admin
'''
import scipy
import numpy as np
import sklearn
import random
from sklearn.svm import SVC
from sklearn import cross_validation
from sklearn.grid_search import GridSearchCV, RandomizedSearchCV
import os
import pickle
from sklearn.metrics import precision_recall_fscore_support
from sklearn.ensemble import RandomForestClassifier
#from scipy.stats import randint as sp_randint
from sklearn.metrics import average_precision_score, precision_score, classification_report
from sklearn.metrics import accuracy_score
from sklearn.metrics import f1_score, recall_score


class Classifier(object):
    '''
    classdocs
    '''
        
    X = []
    y = []
       
    Xtrain = []
    ytrain = []
       
    Xtest = []
    ytest = []
       
    splitPercent = 0.3
       
    model = []
       
    n_foldCV = 0  # how many folds cross validation

    def __init__(self, dataX, datay):
        self.X = dataX
        self.y = datay

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
        classifReport = 'Accuracy: '+ str(accuracy_score(self.ytest, y_pred))
        classifReport += '\nPrecision: ' + str(precision_score(self.ytest, y_pred))
        classifReport +='\nRecall: ' + str(recall_score(self.ytest, y_pred))
        classifReport += '\nF-score: ' + str(f1_score(self.ytest, y_pred))
        classifReport += '\nClassification Report:\n ' + str(classification_report(self.ytest, y_pred))
        #print(classifReport)
        return classifReport, accuracy_score(self.ytest, y_pred), precision_score(self.ytest, y_pred), recall_score(self.ytest, y_pred), f1_score(self.ytest, y_pred) 
        
    def runClassifier(self):
        """ Run the provided classifier."""
        acc = []; pre = []; rec = []; fsc = []
        clRep = 0
        if self.X.shape[0] < 100000:
            for i in range(10):
                self.shuffle()
                self.splitTrainTest()
                self.train()
                self.predict()
                clRep, accu, prec, reca, fsco =  self.evaluate()
                acc.append(accu)
                pre.append(prec)
                rec.append(reca)
                fsc.append(fsco)
        
            print ('average Accuracy: ', np.mean(acc))
            print ('average Precision: ', np.mean(pre))
            print ('average Recall: ', np.mean(rec))
            print('average F1_score: ', np.mean(fsc))
            
        else:
            self.shuffle()
            self.splitTrainTest()
            self.train()
            self.predict()
            clRep, accu, prec, reca, fsco =  self.evaluate()
            #print ('Classification Report: ', clRep)
        return clRep
