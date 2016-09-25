# -*- coding: utf-8 -*-
"""
Created on Sun Sep 04 14:12:49 2016

@author: admin
"""
from .utils import featid


class SurfaceFeatures:
    
    
    def __init__(self, preprocessed):
        '''
        Initializes the class with a preprocessor. '''
        self.preprocessor = preprocessed
    
    @featid(1)    
    def averageWordLength(self, argString):
        '''Find average word length of every sentence and return list. '''

        aveWordLen = []
        for sentence in self.preprocessor.getPlainSentences():
            sentence = sentence.strip()
            sentence = sentence.split()
            length = sum([len(s) for s in sentence])
            aveWordLen.append(float(length) / len(sentence))

        return aveWordLen

    @featid(2)
    def syllableRatio(self, argString):
        '''
        We approximate this feature by counting the number of vowel-sequences
        that are delimited by consonants or space in a word, normalized by the number of tokens
        in the chunk
        
        '''
        vowels = ['a', 'e', 'i', 'o', 'u']
        sylRatios = []
        for sentence in self.preprocessor.getPlainSentences():
            sentence = sentence.strip()
            sentence = sentence.split()
            sylCount = 0
            for word in sentence:
                word2List = list(word)
                for i in range(len(word2List)-1):
                    if word2List[i] in vowels and word2List[i+1] not in vowels:
                        sylCount += 1
            
            sylRatios.append(float(sylCount)/len(sentence))
            
        return sylRatios
        
   