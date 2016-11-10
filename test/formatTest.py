# -*- coding: utf-8 -*-
"""
Created on Thu Nov 03 12:53:28 2016

@author: admin
"""

import unittest
import importlib
import imp, os
import sys, inspect
from os import path
import difflib


sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )
fileName, pathname, description = imp.find_module('infodens')

from infodens.preprocessor import preprocess
prepObj = preprocess.Preprocess('testFile.txt')
from infodens.formater import format

from infodens.controller import controller
conObj = controller.Controller('testconfig.txt')
ch, ids = conObj.loadConfig()

from infodens.featurextractor import featuremanager
featMgrObj = featuremanager.FeatureManager(conObj.featureIDs, conObj.featargs, prepObj)

conObj2 = controller.Controller('testconfig2.txt')
conObj2.loadConfig()
prepObj2 = preprocess.Preprocess('testFile.txt')
featMgrObj2 = featuremanager.FeatureManager(conObj2.featureIDs, conObj2.featargs, prepObj2)

features = featMgrObj2.callExtractors()
prepObj3 = preprocess.Preprocess('labelFile.txt')
labels = prepObj3.preprocessClassID()
fmtObj = format.Format(features, labels)
X, y = fmtObj.scikitFormat()

from infodens.classifier import classifierManager
clfMgrObj = classifierManager.ClassifierManager(conObj2.classifiersList, X, y)

class Test_lexicalFeatures(unittest.TestCase):

    def test_scikitFormat(self):
        chX = [[2.5, 0.75], [3.25, 1.0], [2.75, 0.75], [3.5, 1.25]]
        chy = [1, 1, 2, 2]
        X, y = fmtObj.scikitFormat()
        Xlist = X.tolist()
        ylist = y.tolist()
        self.assertListEqual(chX,Xlist)
        self.assertListEqual(chy,ylist)
        
        
    def test_libsvmFormat(self):
        c = [[1, '1:2.5', '2:0.75'], [1, '1:3.25', '2:1.0'], [2, '1:2.75', '2:0.75'], [2, '1:3.5', '2:1.25']]
        ch = ch = fmtObj.libsvmFormat('libfmt.txt')
        self.assertListEqual(c,ch)
    
    def test_lexicalToTokens(self):
        c = [[2.5, 0.75, 1], [3.25, 1.0, 1], [2.75, 0.75, 2], [3.5, 1.25, 2]]
        ch = fmtObj.arrfFormat('arrffmt.txt')
        self.assertListEqual(c,ch)
        
   
        
    
        
    
        
if __name__ == '__main__':       
    unittest.main()