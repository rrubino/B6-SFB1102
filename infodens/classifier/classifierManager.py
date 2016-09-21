# -*- coding: utf-8 -*-
"""
Created on Sat Sep 17 09:24:16 2016

@author: admin
"""
import importlib
import imp, os
import sys, inspect
from os import path
from .classifier import Classifier
import difflib

class ClassifierManager:

    def __init__(self, ids, dSet, labs):
        self.classifierIDs = ids
        self.dataSet = dSet
        self.labels = labs
        sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )
        self.fileName, self.pathname, self.description = imp.find_module('classifier')
        self.classifyModules = []
        self.returnClassifiers()
        print(self.classifyModules)
        print(self.availClassifiers)

    def checkValidClassifier(self):
        for classifID in self.classifierIDs:
            if classifID not in self.availClassifiers:
                return 0
        return 1

    def returnClassifiers(self):
        files = (os.listdir("infodens/classifier"))
        for file in files:
            if file.endswith(".py") and file is not "__init__.py":
                file = file.replace(".py",'')
                module = "infodens.classifier."+ file
                importlib.import_module(module)
                self.classifyModules.append(file)
        self.availClassifiers = [cls.__name__ for cls in Classifier.__subclasses__()]
                            

    def callClassifiers(self):

        for classif in self.classifierIDs:
            for module in self.classifyModules:
                if classif.lower() == module.lower():
                    break
            print(module)
            classModule = importlib.import_module("infodens.classifier."+module)
            class_ = getattr(classModule, classif)
            clf = class_(self.dataSet, self.labels)
            clf.runClassifier()
                
