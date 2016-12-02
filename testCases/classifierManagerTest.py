
import unittest
import importlib
import imp, os
import sys, inspect
from os import path
import difflib




class Test_classifierManager(unittest.TestCase):
    
    def setUp(self):
        sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )
        fileName, pathname, description = imp.find_module('infodens')
        
        from infodens.preprocessor import preprocess
        self.prepObj = preprocess.Preprocess('testFile.txt')
        from infodens.formater import format
        
        from infodens.controller import controller
        self.conObj = controller.Controller('testconfig.txt')
        ch, ids, cl = self.conObj.loadConfig()
        
        from infodens.featurextractor import featureManager
        self.featMgrObj = featureManager.FeatureManager(self.conObj.featureIDs, self.conObj.featargs, self.prepObj)
        
        self.conObj2 = controller.Controller('testconfig2.txt')
        self.conObj2.loadConfig()
        self.prepObj2 = preprocess.Preprocess('testFile.txt')
        self.featMgrObj2 = featureManager.FeatureManager(self.conObj2.featureIDs, self.conObj2.featargs, self.prepObj2)
        
        self.features = self.featMgrObj2.callExtractors()
        self.prepObj3 = preprocess.Preprocess('labelFile.txt')
        self.labels = self.prepObj3.preprocessClassID()
        self.fmtObj = format.Format(self.features, self.labels)
        self.X, self.y = self.fmtObj.scikitFormat()
        
        from infodens.classifier import classifierManager
        self.clfMgrObj = classifierManager.ClassifierManager(self.conObj2.classifiersList,self.X, self.y)

    def test_returnClassifiers(self):        
        self.clfMgrObj.returnClassifiers()
        clfs = self.clfMgrObj.availClassifiers
        chClfs = ['DecisionTree', 'Ensemble', 'NeuralNetwork', 'RandomForest', 'SVM']
        self.assertListEqual(chClfs,clfs)
        
    
        
    def test_checkValidClassifier(self):        
        c = 1
        idCMs, allIds = self.featMgrObj.idClassDictionary()
        ch = self.clfMgrObj.checkValidClassifier()
        self.assertEquals(c,ch)
        
    def test_checkValidClassifierNeg(self):
        from infodens.classifier import classifierManager
        self.clfMgrObj2 = classifierManager.ClassifierManager(['dt', 'RandomForest', 'SVM'], self.X, self.y)        
        c = 0
        idCMs, allIds = self.featMgrObj.idClassDictionary()
        ch = self.clfMgrObj2.checkValidClassifier()
        self.assertEquals(c,ch)
    
        
    
        
    
        
    
        
    
        
    
        
if __name__ == '__main__':    
    
    unittest.main()