
import unittest
import importlib
import imp, os
import sys, inspect
from os import path
import difflib


sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )
fileName, pathname, description = imp.find_module('infodens')



prep = imp.load_source('preprocess', pathname+'/preprocessor/preprocess.py')
prepObj = prep.Preprocess('testFile.txt')
from infodens.featurextractor import surfaceFeatures
surfObj = surfaceFeatures.SurfaceFeatures(prepObj)







class Test_surfaceFeatures(unittest.TestCase):

    def test_averageWordLength(self):
        c = [2.5, 3.25, 2.75, 3.5]
        ch = surfObj.averageWordLength('argString')
        self.assertListEqual(c,ch)
        
    def test_sentenceLength(self):
        c = [4, 4, 4, 4]
        ch = surfObj.sentenceLength('argString')
        self.assertListEqual(c,ch)
    
    def test_syllableRatio(self):
        c = [0.75, 1.0, 0.75, 1.25]
        ch = surfObj.syllableRatio('argString')
        self.assertListEqual(c,ch)
        
    
        
    
        
    
        
if __name__ == '__main__':
    unittest.main()