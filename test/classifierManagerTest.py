
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

class Test_classifierManager(unittest.TestCase):

    def test_returnClassifiers(self):        
        clfMgrObj.returnClassifiers()
        clfs = clfMgrObj.availClassifiers
        chClfs = ['DecisionTree', 'Ensemble', 'NeuralNetwork', 'RandomForest', 'SVM']
        self.assertListEqual(chClfs,clfs)
        
    
        
    def test_checkValidClassifier(self):        
        c = 1
        idCMs, allIds = featMgrObj.idClassDictionary()
        ch = clfMgrObj.checkValidClassifier()
        self.assertEquals(c,ch)
        
    def test_checkValidClassifierNeg(self):
        clfMgrObj2 = classifierManager.ClassifierManager(['dt', 'RandomForest', 'SVM'], X, y)        
        c = 0
        idCMs, allIds = featMgrObj.idClassDictionary()
        ch = clfMgrObj2.checkValidClassifier()
        self.assertEquals(c,ch)
    
        
    
        
    
        
    
        
    
        
    
        
if __name__ == '__main__':    
    
    unittest.main()