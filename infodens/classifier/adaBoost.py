'''
Created on Aug 24, 2016

@author: admin
'''
from classifier import Classifier
from sklearn.model_selection import RandomizedSearchCV
from sklearn.ensemble import AdaBoostClassifier


class AdaBoost(Classifier):
    '''
    classdocs
    '''
   
    classifierName = 'Adaboost'
    n_estimators = 20

    def train(self):
        
        if self.n_foldCV <= 0:
            print ('No cross validation required. If required set the parameter to a positive number')
            clf = AdaBoostClassifier(n_estimators=20)
            clf.fit(self.Xtrain, self.ytrain)
        else:
            #not yet implemented, so does the same thing as without cv
            clf = AdaBoostClassifier(n_estimators=20)
            clf.fit(self.Xtrain, self.ytrain)
            
        self.model = clf
