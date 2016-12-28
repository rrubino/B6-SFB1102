# -*- coding: utf-8 -*-
"""
Created on Mon Nov 07 11:07:20 2016

@author: admin
"""


import unittest
import importlib
import imp, os
import sys, inspect
from os import path
import difflib



class Test_infodens(unittest.TestCase):
    
    def setUp(self):
        sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )
        fileName, pathname, description = imp.find_module('infodens')
        from infodens.preprocessor import preprocess
        self.prepObj = preprocess.Preprocess('testFile.txt')
        from infodens.featurextractor import bagOfNgrams
        self.ngramsObj = bagOfNgrams.BagOfNgrams(self.prepObj)
        

    
    def test_ngramCBSurprisal(self):
        c = [[0.25, 0.0, 0.0, 0.25, 0.0, 0.25, 0.0, 0.0, 0.0], [0.0, 0.25, 0.0, 0.0, 0.0, 0.0, 0.25, 0.0, 0.25], [0.0, 0.0, 0.25, 0.25, 0.0, 0.25, 0.0, 0.0, 0.0], [0.0, 0.25, 0.0, 0.0, 0.25, 0.0, 0.0, 0.25, 0.0]]
        ch = self.ngramsObj.ngramBagOfWords('2,1')
        self.assertListEqual(c,ch)
        
    def test_ngramPOSCBSurprisal(self):
        c = [[0.0, 0.25, 0.25], [0.25, 0.0, 0.0], [0.0, 0.25, 0.25], [0.25, 0.0, 0.0]]
        ch = self.ngramsObj.ngramBagOfWords('2,2')
        self.assertListEqual(c,ch)
        
    def test_ngramSurprisal(self):
        c = [[0.0, 0.0, 0.25, 0.0, 0.25, 0.25], [0.25, 0.25, 0.0, 0.25, 0.0, 0.0], [0.0, 0.0, 0.25, 0.0, 0.25, 0.25], [0.25, 0.25, 0.0, 0.25, 0.0, 0.0]]
        ch = self.ngramsObj.ngramPOSBagOfWords('2,1')
        self.assertListEqual(c,ch)
        
    def test_ngramPOSSurprisal(self):
        c = [[0.25, 0.0, 0.0, 0.0, 0.25, 0.25, 0.0], [0.0, 0.25, 0.0, 0.25, 0.0, 0.0, 0.25], [0.25, 0.0, 0.0, 0.0, 0.25, 0.25, 0.0], [0.0, 0.25, 0.25, 0.25, 0.0, 0.0, 0.0]]
        ch = self.ngramsObj.ngramMixedBagOfWords('2,1')
        self.assertListEqual(c,ch)
        
    def test_lengthSurprisal(self):
        c = [[0.25, 0.0, 0.0, 0.25, 0.0, 0.25, 0.0, 0.0, 0.0], [0.0, 0.25, 0.0, 0.0, 0.0, 0.0, 0.25, 0.0, 0.25], [0.0, 0.0, 0.25, 0.25, 0.0, 0.25, 0.0, 0.0, 0.0], [0.0, 0.25, 0.0, 0.0, 0.25, 0.0, 0.0, 0.25, 0.0]]
        ch = self.ngramsObj.ngramLemmaBagOfWords('2,1')
        self.assertListEqual(c,ch)
        
    
        
    
        
if __name__ == '__main__':
    unittest.main()