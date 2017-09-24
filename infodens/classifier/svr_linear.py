'''
Created on Aug 23, 2016

@author: admin
'''

from infodens.classifier.classifier import Classifier
from sklearn.svm import LinearSVR
from sklearn.model_selection import GridSearchCV
import numpy as np
from sklearn.metrics import mean_squared_error

import time


class SVR_linear(Classifier):
    '''
    classdocs
    '''

    classifierName = 'Support Vector Regressor'
    C = np.logspace(-5.0, 5.0, num=10, endpoint=True, base=2)

    def evaluate(self):

        """ Overriding default evaluate"""
        y_pred = self.predict()
        return mean_squared_error(self.ytest, y_pred)

    def train(self):

        tuned_parameters = [{'C': self.C}]

        print ('SVR Optimizing. This will take a while')
        start_time = time.time()
        clf = GridSearchCV(LinearSVR(), tuned_parameters,
                           n_jobs=self.threadCount, cv=5)

        clf.fit(self.Xtrain, self.ytrain)
        print('Done with Optimizing. it took ', time.time() -
              start_time, ' seconds')

        self.model = clf.best_estimator_

    def runClassifier(self):
        """ Overriding default running"""
        mse = []
        #pre = []; rec = []; fsc = []

        for i in range(self.n_foldCV):
            self.shuffle()
            self.splitTrainTest()
            self.train()
            error = self.evaluate()
            mse.append(error)

        classifReport = 'Average MSE: ' + str(np.mean(mse))
        #classifReport += '\nAverage Precision: ' + str(np.mean(pre))
        #classifReport += '\nAverage Recall: ' + str(np.mean(rec))
        #classifReport += '\nAverage F-score: ' + str(np.mean(fsc))

        return classifReport