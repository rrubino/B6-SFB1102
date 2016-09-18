# -*- coding: utf-8 -*-
"""
Created on Sat Sep 17 09:24:16 2016

@author: admin
"""
import importlib
import imp, os
import sys, inspect
from os import path

class ClassifierManager:

    def __init__(self, ids, dSet, labs):
        self.classifierIDs = ids
        self.dataSet = dSet
        self.labels = labs
        sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )
        self.fileName, self.pathname, self.description = imp.find_module('classifier')

    def checkValidClassifier(self, classifDict):
        #TODO: replace classifDict to be with self.classifDict
        for classifID in self.classifierIDs:
            if classifID not in classifDict:
                return 0
        return 1

    def runClassifier(self, clf):
        """ Run the provided classifier."""
        
        clf.shuffle()        
        clf.splitTrainTest()
        clf.train()
        clf.predict()
        clf.evaluate()
        
    def readClassifierDictionary(self, theFile):
        with open(theFile) as f:
            fileContents = f.read().splitlines()        
        theDict = {int(content.strip().split()[0]):content.strip().split()[1] for content in fileContents
                   if int(content.strip().split()[0]) in self.classifierIDs}
        return theDict
    
    def callClassifiers(self):
        possClassifierClasses = set([os.path.splitext(module)[0] for module in os.listdir(self.pathname)
                                     if module.endswith('.py')])
        
        classifierDictionary = self.readClassifierDictionary(self.pathname+'/classifierDictionary.txt')
        classnames = {name.lower():name for name in classifierDictionary.values()}
        
        for eachName in possClassifierClasses:            
            if eachName.lower() in classnames.keys():                
                modd = __import__('classifier.'+eachName)
                modul = getattr(modd, eachName)                
                class_ = getattr(modul, classnames[eachName.lower()])
                clf = class_(self.dataSet, self.labels)
                self.runClassifier(clf)
