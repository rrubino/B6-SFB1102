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
from joblib import Parallel, delayed
import multiprocessing


def runClassifier(classifierToRun):
    classifReport = str(type(classifierToRun).__name__)
    classifReport += ":\n"
    classifReport += classifierToRun.runClassifier()
    classifReport += "\n"
    return classifReport

class ClassifierManager:

    def __init__(self, ids, dSet, labs, threads=1):
        self.classifierIDs = ids
        self.dataSet = dSet
        self.labels = labs
        sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )
        self.fileName, self.pathname, self.description = imp.find_module('classifier')
        self.classifyModules = []
        self.threadsCount = threads
        self.returnClassifiers()
        #print(self.classifyModules)
        #print(self.availClassifiers)

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

        classifierObjs = []
        svmClass = 0
        for classif in self.classifierIDs:
            for module in self.classifyModules:
                if classif.lower() == module.lower():
                    break
            classModule = importlib.import_module("infodens.classifier."+module)
            class_ = getattr(classModule, classif)
            if "SVM" in classif:
                svmClass = class_(self.dataSet, self.labels, self.threadsCount)
            else:
                classifierObjs.append(class_(self.dataSet, self.labels, self.threadsCount))

        num_cores = multiprocessing.cpu_count()
        classifReports = Parallel(n_jobs=self.threadsCount)(delayed(runClassifier)(classif)
                                                    for classif in classifierObjs)
        if svmClass is not 0:
            classifReports.append(runClassifier(svmClass))

        return '\n'.join(classifReports)
