'''
Created on Aug 23, 2016

@author: admin
'''
#from trans.classifier import classifier
from classifier import Classifier
import random
import numpy as np
from sklearn.model_selection import RandomizedSearchCV
from sklearn import tree


class DecisionTree(Classifier):

    classifierName = 'Decision Tree'
    n_estimators = 20

    def train(self):
        
        if self.n_foldCV <= 0:
            #print ('No cross validation required. If required set the parameter to a positive number')
            clf = tree.DecisionTreeClassifier()
            clf.fit(self.Xtrain, self.ytrain)
        else:
            
            # Set the parameters by cross-validation
            # specify parameters and distributions to sample from
            param_dist = {"max_depth": [3, None],
                          "max_features": random.randint(1, 11),
                          "min_samples_split": random.randint(1, 11),
                          "min_samples_leaf": random.randint(1, 11),
                          "bootstrap": [True, False],
                          "criterion": ["gini", "entropy"]}
                    
                    
            n_iter_search = 20
            clf = RandomizedSearchCV(clf, param_distributions=param_dist,
                                   n_iter=n_iter_search)
            
            clf.fit(self.Xtrain, self.ytrain)
            
        self.model = clf
