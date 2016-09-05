# -*- coding: utf-8 -*-
"""
Created on Sun Sep 04 14:12:49 2016

@author: admin
"""
from utils import featid


class SurfaceFeatures:
    
    
    def __init__(self, lof=None):
        '''
        Initializes the class with a list of sentences (or blocks)
        
        '''
        self.listOfSentences = lof
    
    @featid(1)    
    def averageWordLength(self):
        '''
        Finds avreage word length of every sentence (or block)
        by counting the length of every word divided by the number of words in the sentence
        
        '''
        aveWordLen = []
        for sentence in self.listOfSentences:
            length = sum([len(s) for s in sentence])
            aveWordLen.append(float(length)/ len(sentence))
            
        return aveWordLen
        
   