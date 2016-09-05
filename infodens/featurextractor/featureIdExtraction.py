# -*- coding: utf-8 -*-
"""
Created on Sun Sep 04 18:15:17 2016

@author: admin
"""

import imp, os
import sys, inspect
from os import path
from utils import featid, methodsWithDecorator, writeDictionaryToFile, readFileToDictionary, idsOfMethods



class FeatureIdEtraction:
    
    def __init__(self):
        self.className = 'featureIdExtraction'
        
        
    def extractFeatureIds(self):
        if __package__ is None:
            sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )
        file, pathname, description = imp.find_module('featurextractor')

        possFeatureClasses = set([os.path.splitext(module)[0] for module in os.listdir(pathname) if module.endswith('.py')])
        
        
        featureIds = readFileToDictionary(pathname+'/featureIds.txt')
        
        modules  = []
        
        for eachName in possFeatureClasses:
            if eachName.startswith('__'):
                pass
            else:
                modd = __import__('featurextractor.'+eachName)
                modules.append(getattr(modd, eachName))
                
        
        
        
        
        for modul in modules:
            clsmembers = inspect.getmembers(modul, inspect.isclass)
            for i in range(len(clsmembers)):        
                featureIds = idsOfMethods(clsmembers[i][1], 'featid', featureIds)
        
        
        writeDictionaryToFile(featureIds, pathname+'/featureIds.txt')





 


        