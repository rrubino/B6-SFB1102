'''
Created on Aug 23, 2016

@author: admin
'''
from classifier import Classifier
from sklearn.ensemble import VotingClassifier, RandomForestClassifier


class Ensemble(Classifier):

    classifierName = 'Ensemble'

    def train(self):

        #TODO: Define ensemble
        cl1 = RandomForestClassifier(random_state=1)
        listOfClassifiers = [("randomForest", cl1)]

        if self.n_foldCV <= 0:
            print ('No cross validation required. If required set the parameter to a positive number')
            clf = VotingClassifier(estimators=listOfClassifiers, voting='hard')
            clf.fit(self.Xtrain, self.ytrain)
        else:
            #Not yet implemented
            clf = VotingClassifier(estimators=listOfClassifiers, voting='hard')
            
            clf.fit(self.Xtrain, self.ytrain)
            
        self.model = clf
