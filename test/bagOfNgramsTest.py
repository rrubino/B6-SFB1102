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






sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )
fileName, pathname, description = imp.find_module('infodens')
from infodens.preprocessor import preprocess
prepObj = preprocess.Preprocess('testFile.txt')
from infodens.featurextractor import bagOfNgrams
ngramsObj = bagOfNgrams.BagOfNgrams(prepObj)


class Test_surfaceFeatures(unittest.TestCase):

    
    def test_ngramBagOfWords(self):
        c = [[0, 0, 0, 0.33], [0, 0.33, 0, 0], [0.33, 0, 0.33, 0], [0.33, 0, 0, 0], [0, 0, 0.33, 0], [0, 0.33, 0, 0], [0, 0, 0, 0.33], [0.33, 0, 0.33, 0], [0, 0.33, 0, 0.33]]
        ch = ngramsObj.ngramBagOfWords('2,1')
        self.assertListEqual(c,ch)
        
    def test_ngramBagOfWords2(self):
        c = [[0.33, 0, 0.33, 0], [0.33, 0, 0.33, 0], [0, 0.33, 0, 0.33]]
        ch = ngramsObj.ngramBagOfWords('2,2')
        self.assertListEqual(c,ch)
        
    def test_ngramPOSBagOfWords(self):
        c = [[0.33, 0, 0.33, 0], [0.33, 0, 0.33, 0], [0, 0.33, 0, 0.33], [0, 0.33, 0, 0.33], [0.33, 0, 0.33, 0], [0, 0.33, 0, 0.33]]
        ch = ngramsObj.ngramPOSBagOfWords('2,1')
        self.assertListEqual(c,ch)
        
    def test_ngramMixedBagOfWords(self):
        c = [[0, 0, 0, 0.33], [0, 0.33, 0, 0], [0, 0.33, 0, 0.33], [0.33, 0, 0.33, 0], [0, 0.33, 0, 0.33], [0.33, 0, 0.33, 0], [0.33, 0, 0.33, 0]]
        ch = ngramsObj.ngramMixedBagOfWords('2,1')
        self.assertListEqual(c,ch)
        
    def test_ngramLemmaBagOfWords(self):
        c = [[0, 0, 0, 0.33], [0, 0.33, 0, 0], [0.33, 0, 0.33, 0], [0.33, 0, 0, 0], [0, 0, 0.33, 0], [0, 0.33, 0, 0], [0, 0, 0, 0.33], [0.33, 0, 0.33, 0], [0, 0.33, 0, 0.33]]
        ch = ngramsObj.ngramLemmaBagOfWords('2,1')
        self.assertListEqual(c,ch)
        
    
        
    
        
if __name__ == '__main__':
    unittest.main()