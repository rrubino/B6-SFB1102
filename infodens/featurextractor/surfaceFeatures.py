# -*- coding: utf-8 -*-
"""
Created on Sun Sep 04 14:12:49 2016

@author: admin
"""
from utils import featid


class SurfaceFeatures:
    
    
    def __init__(self, lof):
        '''
        Initializes the class with a list of sentences (or blocks)
        
        '''
        self.listOfSentences = lof
    
    @featid(1)    
    def averageWordLength(self):
        '''
        Finds average word length of every sentence (or block)
        by counting the length of every word divided by the number of words in the sentence
        
        '''
        aveWordLen = []
        for sentence in self.listOfSentences:
            length = sum([len(s) for s in sentence])
            aveWordLen.append(float(length)/ len(sentence))
            
        return aveWordLen
        
    @featid(2)    
    def syllableRatio(self):
        '''
        We approximate this feature by counting the number of vowel-sequences
        that are delimited by consonants or space in a word, normalized by the number of tokens
        in the chunk
        
        '''
        vowels = ['a', 'e', 'i', 'o', 'u']
        sylRatios = []
        for sentence in self.listOfSentences:
            sylCount = 0
            for word in sentence:
                word2List = list(word)
                for i in range(len(word2List)-1):
                    if word2List[i] in vowels and word2List[i+1] not in vowels:
                        sylCount += 1
            
            sylRatios.append(float(sylCount)/ len(sentence))
            
        return sylRatios
        
   