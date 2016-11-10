
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
ch, ids = conObj.loadConfig()

from infodens.featurextractor import featuremanager
featMgrObj = featuremanager.FeatureManager(conObj.featureIDs, conObj.featargs, prepObj)

conObj2 = controller.Controller('testconfig2.txt')
conObj2.loadConfig()
prepObj2 = preprocess.Preprocess('testFile.txt')
featMgrObj2 = featuremanager.FeatureManager(conObj2.featureIDs, conObj2.featargs, prepObj2)



class Test_featureManager(unittest.TestCase):

    def test_idClassDictionary(self):        
        chALlIds = {1: 'averageWordLength', 2: 'syllableRatio', 3: 'lexicalDensity', 4: 'ngramBagOfWords', 5: 'ngramPOSBagOfWords', 6: 'ngramMixedBagOfWords', 7: 'ngramLemmaBagOfWords', 8: 'parseTreeDepth', 10: 'sentenceLength', 11: 'lexicalRichness', 12: 'lexicalToTokens'}
        ids, allIds = featMgrObj.idClassDictionary()
        self.assertDictEqual(chALlIds,allIds)
        
    def test_methodsWithDecorator(self):        
        chmwDec = {8: 'parseTreeDepth', 1: 'averageWordLength', 10: 'sentenceLength', 2: 'syllableRatio'}
        idCMs, allIds = featMgrObj.idClassDictionary()
        mwDec = featMgrObj.methodsWithDecorator(idCMs[1], 'featid')
        self.assertDictEqual(chmwDec,mwDec)
        
    def test_checkFeatValidity(self):        
        c = 1
        idCMs, allIds = featMgrObj.idClassDictionary()
        ch = featMgrObj.checkFeatValidity()
        self.assertEquals(c,ch)
        
    def test_callExtractors(self):        
        c = [[2.5, 3.25, 2.75, 3.5], [0.75, 1.0, 0.75, 1.25]]        
        ch = featMgrObj2.callExtractors()
        self.assertListEqual(c,ch)
        
    
        
    
        
    
        
    
        
    
        
if __name__ == '__main__':
    unittest.main()