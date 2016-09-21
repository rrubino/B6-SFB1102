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

    
        
    
    def findMethodsWithASuperClass(self, source, superClass):
        f = open(source, 'r')
        sourcelines = f.readlines()
        
        for i,line in enumerate(sourcelines):
            className = ''
            line = line.strip()
            if line.find('#'):
                line = line.split('#')[0]
            if line.find('"""'):
                line = line.split('"""')[0]
            if line.startswith('class') and line.endswith(':'):
                classNameAndArgs = line.split(' ')
                classNameAndArgs = [val for val in classNameAndArgs if val != ' ']
                
                className = line.split(' ')[1].split("(")[0]
                if classNameAndArgs[1].find('(') > -1:
                    
                    if line.split(' ')[1].split("(")[1].split(")")[0].strip() == superClass:
                        return className, True 
                    else:
                        return className, False
                else:
                    return className, False
                
        return className, False
        
    
    def findClassifiers(self):
        sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )
        fileName, pathname, description = imp.find_module('classifier')
        possClassifierClasses = set([os.path.splitext(module)[0] for module in os.listdir(pathname) if module.endswith('.py')])
        allClassifiers = []
        for possibleClass in possClassifierClasses:
            className, TorF = self.findMethodsWithASuperClass(self.pathname+'/'+possibleClass+'.py', 'Classifier')
            if TorF:
                allClassifiers.append(className)
        return allClassifiers
            
                                   
                        
                            
        
        
        
        
    def callClassifiers(self):
        possClassifierClasses = set([os.path.splitext(module)[0] for module in os.listdir(self.pathname)
                                     if module.endswith('.py')])
        
        classnames = {name.lower():name for name in self.classifierIDs}
        
        for eachName in possClassifierClasses:            
            if eachName.lower() in classnames.keys():                
                modd = __import__('classifier.'+eachName)
                modul = getattr(modd, eachName)                
                class_ = getattr(modul, classnames[eachName.lower()])
                clf = class_(self.dataSet, self.labels)
                clf.runClassifier()
                
