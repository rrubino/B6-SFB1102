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
        self.prepObj = preprocess.Preprocess('testFile.txt', 'labelFile.txt')
        from infodens.featurextractor import infodensFeatures
        self.ngramsSupObj = infodensFeatures.InfodensFeatures(self.prepObj)
        

    
    def test_ngramCBSurprisal(self):
        c = [[2.584962500721156, 0.0, 2.584962500721156, 2.584962500721156, 0.0, 0.0, 0.0, 0.0, 2.584962500721156, 0.0, 2.584962500721156, 0.0], [0.0, 2.584962500721156, 0.0, 0.0, 2.584962500721156, 2.584962500721156, 2.584962500721156, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 2.584962500721156, 2.584962500721156, 0.0, 0.0, 0.0, 2.584962500721156, 2.584962500721156, 0.0, 2.584962500721156, 0.0], [0.0, 2.584962500721156, 0.0, 0.0, 0.0, 0.0, 2.584962500721156, 0.0, 0.0, 2.584962500721156, 0.0, 2.584962500721156]]
        ch = self.ngramsSupObj.ngramCBSurprisal('2,1')
        self.assertListEqual(c,ch)
        
    def test_ngramPOSCBSurprisal(self):
        c = [[0.0, 0.0, 2.584962500721156, 0.0, 2.584962500721156, 2.584962500721156, 0.0, 0.0, 2.584962500721156, 0.0, 2.584962500721156, 2.584962500721156], [2.584962500721156, 2.584962500721156, 0.0, 2.584962500721156, 0.0, 0.0, 2.584962500721156, 2.584962500721156, 0.0, 2.584962500721156, 0.0, 0.0], [0.0, 0.0, 2.584962500721156, 0.0, 2.584962500721156, 2.584962500721156, 0.0, 0.0, 2.584962500721156, 0.0, 2.584962500721156, 2.584962500721156], [2.584962500721156, 2.584962500721156, 0.0, 2.584962500721156, 0.0, 0.0, 2.584962500721156, 2.584962500721156, 0.0, 2.584962500721156, 0.0, 0.0]]
        ch = self.ngramsSupObj.ngramPOSCBSurprisal('2,1')
        self.assertListEqual(c,ch)
        
    def test_ngramSurprisal(self):
        c = [[3.3923174227787602, 0.0, 0.0, 2.807354922057604, 0.0, 2.807354922057604, 0.0, 0.0, 0.0], [0.0, 2.807354922057604, 0.0, 0.0, 0.0, 0.0, 3.3923174227787602, 0.0, 3.3923174227787602], [0.0, 0.0, 3.3923174227787602, 2.807354922057604, 0.0, 2.807354922057604, 0.0, 0.0, 0.0], [0.0, 2.807354922057604, 0.0, 0.0, 3.3923174227787602, 0.0, 0.0, 3.3923174227787602, 0.0]]
        ch = self.ngramsSupObj.ngramSurprisal('2,1')
        self.assertListEqual(c,ch)
        
    def test_ngramPOSSurprisal(self):
        c = [[0.0, 0.0, 2.584962500721156, 0.0, 2.584962500721156, 2.584962500721156], [2.584962500721156, 2.584962500721156, 0.0, 2.584962500721156, 0.0, 0.0], [0.0, 0.0, 2.584962500721156, 0.0, 2.584962500721156, 2.584962500721156], [2.584962500721156, 2.584962500721156, 0.0, 2.584962500721156, 0.0, 0.0]]
        ch = self.ngramsSupObj.ngramPOSSurprisal('2,1')
        self.assertListEqual(c,ch)
        
    def test_lengthSurprisal(self):
        c = [[2.807354922057604, 2.070389327891398, 2.3923174227787602, 1.5849625007211563, 0.0], [0.0, 2.070389327891398, 2.3923174227787602, 1.5849625007211563, 0.0], [2.807354922057604, 2.070389327891398, 0.0, 1.5849625007211563, 0.0], [0.0, 2.070389327891398, 2.3923174227787602, 1.5849625007211563, 3.3923174227787602]]
        ch = self.ngramsSupObj.lengthSurprisal('')
        self.assertListEqual(c,ch)
        
    
        
    
        
if __name__ == '__main__':    
    unittest.main()