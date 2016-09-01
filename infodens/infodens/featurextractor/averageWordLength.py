# -*- coding: utf-8 -*-
"""
Created on Tue Aug 30 15:54:31 2016

@author: admin
"""

class AverageWordLength:
    
    listOfSentences = ''
    
    def __init__(self, lof):
        self.listOfSentences = lof
        
    def findAveWordLen(self):
        aveWordLen = []
        for sentence in self.listOfSentences:
            length = sum([len(s) for s in sentence])
            aveWordLen.append(float(length)/ len(sentence))
            
        return aveWordLen