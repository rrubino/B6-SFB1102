# -*- coding: utf-8 -*-
"""
Created on Sun Sep 04 14:12:49 2016

@author: admin
"""
from .featureExtraction import featid, FeatureExtractor
import numpy as np
from scipy import sparse
import scipy.io


class SurfaceFeatures(FeatureExtractor):
    
    @featid(20)
    def momentavgWord(self, argString):
        '''Find average word length of every sentence and return list. '''
        maxSent = 0
        for sentence in self.preprocessor.gettokenizeSents():
            if len(sentence) > maxSent:
                maxSent = len(sentence)

        momentsLen = sparse.lil_matrix((self.preprocessor.getSentCount(), 5))
        moments00 = sparse.lil_matrix((self.preprocessor.getSentCount(), 1))
        i = 0
        for sentence in self.preprocessor.gettokenizeSents():
            moments00[i] = sum([len(s) for s in sentence])
            i += 1

        i = 0
        for sentence in self.preprocessor.gettokenizeSents():
            for j in range(0, 5):
                #momentSum = 0
                momentSum = 1
                for k in range(0, len(sentence)):
                    #momentSum += pow(k+1, j)*(len(sentence[k])/moments00[i, 0])
                    momentSum += np.log( pow(k + 1, j) * (len(sentence[k]) / moments00[i, 0]) )
                momentsLen[i, j] = momentSum
            i += 1
            if i % 100 == 0:
                print(i)

        return momentsLen
