'''
Created on Aug 23, 2016

@author: admin
'''

from .classifier import Classifier
from sklearn.svm import SVC
from sklearn.model_selection import GridSearchCV
import numpy as np

import time


class SVC_linear(Classifier):
    '''
    classdocs
    '''

    classifierName = 'Support Vector Machine'
    k = 'linear'  # linear kernel
    max_iter = -1
    gamma = 'auto'
    C = np.logspace(-5.0, 5.0, num=10, endpoint=True, base=2)

    def train(self):

        score = 'f1'
        tuned_parameters = [{'kernel': ['linear'], 'C': self.C}]

        print ('SVM Optimizing. This will take a while')
        start_time = time.time()
        clf = GridSearchCV(SVC(), tuned_parameters,
                           n_jobs=self.threadCount, cv=self.n_foldCV)

        clf.fit(self.Xtrain, self.ytrain)
        print('Done with Optimizing. it took ', time.time() -
              start_time, ' seconds')

        self.model = clf.best_estimator_
