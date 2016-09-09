# -*- coding: utf-8 -*-
"""
Created on Sun Sep 04 14:12:49 2016

@author: admin
"""
from .utils import featid
from ..preprocessor.preprocess import Preprocess


class SurfaceFeatures:

    def __init__(self, argumentString, listOfSent=None):
        """Gets list of sentences to process """
        self.listOfSentences = listOfSent
        self.featArg = argumentString
    
    @featid(1)    
    def averageWordLength(self):
        """Find average word length of every sentence and return list. """
        aveWordLen = []
        for sentence in self.listOfSentences:
            sentence = sentence.strip()
            sentence = sentence.split()
            length = sum([len(s) for s in sentence])
            aveWordLen.append(float(length)/ len(sentence))
            
        return aveWordLen
        
   