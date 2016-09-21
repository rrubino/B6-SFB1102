# -*- coding: utf-8 -*-
"""
Created on Sat Sep 17 09:24:16 2016

@author: admin
"""
import importlib
import imp, os
import sys, inspect
from os import path
from classifier import Classifier

class ClassifierManager:

    def __init__(self, ids, dSet, labs):
        self.classifierIDs = ids
        self.dataSet = dSet
        self.labels = labs
        sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )
        self.fileName, self.pathname, self.description = imp.find_module('classifier')
        self.availClassifiers = self.returnClassifiers()

    def checkValidClassifier(self):
        for classifID in self.classifierIDs:
            if classifID not in self.availClassifiers:
                return 0
        return 1

    def returnClassifiers(self):
        files = (os.listdir("infodens/classifier"))
        for file in files:
            if file.endswith(".py") and file is not "__init__.py":
                importlib.import_module("infodens.classifier."+file.replace(".py",''))
        return [cls.__name__ for cls in Classifier.__subclasses__()]
                            

    def callClassifiers(self):
        #possClassifierClasses = set([os.path.splitext(module)[0] for module in os.listdir(self.pathname)
        #                            if module.endswith('.py')])
        
        moduleNames = {name.lower() for name in self.classifierIDs}
        
        for classif in self.classifierIDs:
            classModule = importlib.import_module("infodens.classifier." +
                                                  classif.lower())
            class_ = getattr(classModule, classif)
            clf = class_(self.dataSet, self.labels)
            clf.runClassifier()
                
