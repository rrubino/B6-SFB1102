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
        # Set the parameters by cross-validation
        # specify parameters and distributions to sample from
        param_dist = {"max_depth": [3, None],
                          "max_features": random.randint(1, 11),
                          "min_samples_split": random.randint(1, 11),
                          "min_samples_leaf": random.randint(1, 11),
                          "bootstrap": [True, False],
                          "criterion": ["gini", "entropy"]}
        clf = tree.DecisionTreeClassifier()
        n_iter_search = 20

        #clf = RandomizedSearchCV(clf, n_iter=n_iter_search, n_jobs=self.threadCount)
            
        clf.fit(self.Xtrain, self.ytrain)
            
        self.model = clf
