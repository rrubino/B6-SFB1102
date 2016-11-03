# -*- coding: utf-8 -*-
"""
Created on Fri Oct 28 11:47:06 2016

@author: admin
"""

# -*- coding: utf-8 -*-
"""
Created on Fri Oct 28 11:47:06 2016

@author: admin
"""

import unittest
import importlib
import imp, os
import sys, inspect
from os import path
import difflib
import time


sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )
fileName, pathname, description = imp.find_module('infodens')



prep = imp.load_source('preprocess', pathname+'/preprocessor/preprocess.py')
prepObj = prep.Preprocess('testFile.txt')

class Test_preprocess(unittest.TestCase):

    def test_preprocessBySentence(self):
        s = ['This is a boy', 'His name is Audu', 'This is a girl', 'Her name is Sarah']
        ps = prepObj.preprocessBySentence()
        self.assertListEqual(s,ps)
        
    def test_getPlainSentences(self):
        s = ['This is a boy', 'His name is Audu', 'This is a girl', 'Her name is Sarah']
        ps = prepObj.getPlainSentences()
        self.assertListEqual(s,ps)
        
    def test_gettokenizeSents(self):
        s = [['This', 'is', 'a', 'boy'], ['His', 'name', 'is', 'Audu'], ['This', 'is', 'a', 'girl'], ['Her', 'name', 'is', 'Sarah']]
        ps = prepObj.gettokenizeSents()
        self.assertListEqual(s,ps)
        
    def test_nltkPOStag(self):
        s = [[('This', 'DT'), ('is', 'VBZ'), ('a', 'DT'), ('boy', 'NN')], [('His', 'PRP$'), ('name', 'NN'), ('is', 'VBZ'), ('Audu', 'NNP')], [('This', 'DT'), ('is', 'VBZ'), ('a', 'DT'), ('girl', 'NN')], [('Her', 'PRP$'), ('name', 'NN'), ('is', 'VBZ'), ('Sarah', 'NNP')]]
        ps = prepObj.nltkPOStag()
        self.assertListEqual(s,ps)
        
    def test_getLemmatizedSents(self):
        s = [['This', 'is', 'a', 'boy'], ['His', 'name', 'is', 'Audu'], ['This', 'is', 'a', 'girl'], ['Her', 'name', 'is', 'Sarah']]
        ps = prepObj.getLemmatizedSents()
        self.assertListEqual(s,ps)
        
    def test_getMixedSents(self):
        s = [['This', 'VBZ', 'a', 'NN'], ['His', 'NN', 'VBZ', 'NNP'], ['This', 'VBZ', 'a', 'NN'], ['Her', 'NN', 'VBZ', 'NNP']]
        ps = prepObj.getMixedSents()
        self.assertListEqual(s,ps)
        
    def test_buildTokenNgrams(self):
        s = {('a', 'boy'): 1, ('name', 'is'): 2, ('a', 'girl'): 1, ('This', 'is'): 2, ('is', 'a'): 2, ('is', 'Sarah'): 1, ('is', 'Audu'): 1, ('Her', 'name'): 1, ('His', 'name'): 1}
        ps = prepObj.buildTokenNgrams(2)
        self.assertDictEqual(s, ps)
        
    def test_buildPOSNgrams(self):
        s = {('VBZ', 'DT'): 2, ('NN', 'VBZ'): 2, ('PRP$', 'NN'): 2, ('VBZ', 'NNP'): 2, ('DT', 'NN'): 2, ('DT', 'VBZ'): 2}
        ps = prepObj.buildPOSNgrams(2)
        self.assertDictEqual(s, ps)
        
    def test_buildLemmaNgrams(self):
        s = {('a', 'boy'): 1, ('name', 'is'): 2, ('a', 'girl'): 1, ('This', 'is'): 2, ('is', 'a'): 2, ('is', 'Sarah'): 1, ('is', 'Audu'): 1, ('Her', 'name'): 1, ('His', 'name'): 1}
        ps = prepObj.buildLemmaNgrams(2)
        self.assertDictEqual(s, ps) 
        
    def test_buildMixedNgrams(self):
        s = {('This', 'VBZ'): 2, ('a', 'NN'): 2, ('NN', 'VBZ'): 2, ('His', 'NN'): 1, ('VBZ', 'NNP'): 2, ('Her', 'NN'): 1, ('VBZ', 'a'): 2}
        ps = prepObj.buildMixedNgrams(2)
        self.assertDictEqual(s, ps) 
        
    def test_ngramMinFreq(self):
        s = {('This', 'VBZ'): 2, ('a', 'NN'): 2, ('NN', 'VBZ'): 2, ('VBZ', 'a'): 2, ('VBZ', 'NNP'): 2}
        ss = {('This', 'VBZ'): 2, ('a', 'NN'): 2, ('NN', 'VBZ'): 2, ('His', 'NN'): 1, ('VBZ', 'NNP'): 2, ('Her', 'NN'): 1, ('VBZ', 'a'): 2}
        ps = prepObj.ngramMinFreq(ss, 2)
        self.assertDictEqual(s, ps) 
        
if __name__ == '__main__':
    unittest.main()
    




