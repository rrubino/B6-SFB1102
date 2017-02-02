'''
Created on Aug 23, 2016

@author: admin
'''
from classifier import Classifier
import random
from sklearn.model_selection import RandomizedSearchCV
from sklearn import tree


class DecisionTree(Classifier):

    classifierName = 'Decision Tree'
    n_estimators = 20

    def train(self):

        estimatorClass = tree.DecisionTreeClassifier()
        estimatorClass.fit(self.Xtrain, self.ytrain)
        self.model = estimatorClass
