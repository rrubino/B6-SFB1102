# -*- coding: utf-8 -*-
"""
Created on Sun Sep 04 14:12:49 2016

@author: admin
"""
from .featureExtraction import featid, FeatureExtractor
import numpy as np


class SurfaceFeatures(FeatureExtractor):
    
    @featid(1)    
    def averageWordLength(self, argString):
        '''Find average word length of every sentence and return list. '''
        aveWordLen = np.zeros(self.preprocessor.getSentCount())
        i = 0
        for sentence in self.preprocessor.gettokenizeSents():
            if len(sentence) is 0:
                aveWordLen[i] = 0
            else:
                length = sum([len(s) for s in sentence])
                aveWordLen[i] = (float(length) / len(sentence))
            i += 1

        return aveWordLen.tolist()

    @featid(10)
    def sentenceLength(self, argString):
        '''Find length of every sentence and return list. '''

        sentLen = np.zeros(self.preprocessor.getSentCount())
        i = 0
        for sentence in self.preprocessor.gettokenizeSents():
            sentLen[i] = (len(sentence))
            i += 1

        return sentLen.tolist()

    @featid(8)
    def parseTreeDepth(self, argString):
        '''Find depth of every sentence's parse tree and return list. '''
        self.preprocessor.getParseTrees()

    @featid(2)
    def syllableRatio(self, argString):
        '''
        We approximate this feature by counting the number of vowel-sequences
        that are delimited by consonants or space in a word, normalized by the number of tokens
        in the chunk
        
        '''

        vowels = ['a', 'e', 'i', 'o', 'u']
        sylRatios = np.zeros(self.preprocessor.getSentCount())
        i = 0
        for sentence in self.preprocessor.gettokenizeSents():
            sylCount = 0
            for word in sentence:
                word2List = list(word)
                for i in range(len(word2List)-1):
                    if word2List[i] in vowels and word2List[i+1] not in vowels:
                        sylCount += 1

            if len(sentence) is 0:
                sylRatios[i] = 0
            else:
                sylRatios[i] = (float(sylCount)/len(sentence))
            i += 1

        return sylRatios.tolist()
