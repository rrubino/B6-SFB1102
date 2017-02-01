'''
Created on Aug 23, 2016

@author: admin
'''
from classifier import Classifier

import random
import numpy as np
from sklearn.model_selection import RandomizedSearchCV
from sklearn.ensemble import RandomForestClassifier


class RandomForest(Classifier):
    
    classifierName = 'Random Forest'
    n_estimators = 20
        
    def train(self):

        clf = RandomForestClassifier(n_estimators=20, n_jobs=self.threadCount)
        # Set the parameters by cross-validation
        # specify parameters and distributions to sample from
        param_dist = {"max_depth": [3, None],
                          "max_features": random.randint(1, 11),
                          "min_samples_split": random.randint(1, 11),
                          "min_samples_leaf": random.randint(1, 11),
                          "bootstrap": [True, False],
                          "criterion": ["gini", "entropy"]}

        n_iter_search = 20
        #clf = RandomizedSearchCV(clf, param_distributions=param_dist,
        #                           n_iter=n_iter_search, n_jobs=self.threadCount)
            
        clf.fit(self.Xtrain, self.ytrain)
            
        self.model = clf
