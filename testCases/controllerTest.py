
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
from infodens.controller import controller
conObj = controller.Controller('testconfig.txt')
conObj2 = controller.Controller('testconfig2.txt')







class Test_controller(unittest.TestCase):

    def test_parseOutputLine(self):
        conObj = controller.Controller('testconfig.txt')
        c = 1
        ch = conObj.parseOutputLine('output classifier: report1.txt')
        self.assertEquals(c,ch)
        
    def test_parseOutputLine2(self):
        conObj = controller.Controller('testconfig.txt')
        c = 1
        ch = conObj.parseOutputLine('output features: feats.txt format')
        self.assertEquals(c,ch)
        
    def test_parseOutputLine3(self):
        conObj = controller.Controller('testconfig.txt')
        c = 0
        ch = conObj.parseOutputLine('output features: feats.txt')
        self.assertEquals(c,ch)
        
    def test_loadConfig(self):
        conObj = controller.Controller('testconfig.txt')
        c = 1
        ch, ids = conObj.loadConfig()
        self.assertEquals(c,ch)
        
        fids = conObj.featureIDs
        chfids = [1,2,4,4,5,6,7,10,11]
        self.assertListEqual(fids,chfids)
        
        clfList = conObj.classifiersList
        chclfList = ['DecisionTree', 'RandomForest', 'SVM']
        self.assertListEqual(clfList,chclfList)
        
        featArgs = [[], [], '1,10', '2,5', '1,10', '1,10', '1,10', [], []]
        chfeatArgs = conObj.featargs
        self.assertListEqual(featArgs, chfeatArgs)
    
    def test_classesSentsMismatch(self):
        conObj = controller.Controller('testconfig.txt')
        prepObj = preprocess.Preprocess('testFile.txt')
        c = False
        ch = conObj.classesSentsMismatch(prepObj)
        self.assertEquals(c,ch)
        
    def test_manageFeatures(self):
        conObj = controller.Controller('testconfig2.txt')
        ch, ids = conObj.loadConfig()
        c = 1
        ch = conObj.manageFeatures()
        self.assertEquals(c,ch)
        
    
        
    
        
    
        
    
        
if __name__ == '__main__':   
    unittest.main()