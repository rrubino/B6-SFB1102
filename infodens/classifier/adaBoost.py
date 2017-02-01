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

        clf = AdaBoostClassifier(n_estimators=20)
        clf.fit(self.Xtrain, self.ytrain)
            
        self.model = clf
