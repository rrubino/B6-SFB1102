# -*- coding: utf-8 -*-
"""
Created on Sun Sep 04 14:12:49 2016

@author: admin
"""
from .featureExtraction import featid, FeatureExtractor
from collections import Counter
from nltk import ngrams
import time


class BagOfNgrams(FeatureExtractor):

    def ngramArgumentCheck(self, argString):
        status = 1
        n = 0
        freq = 0

        argStringList = argString.split(',')
        if argStringList[0].isdigit():
            n = int(argStringList[0])
        else:
            print('Error: n should be an integer')
            status = 0
        if len(argStringList) > 1:
            if argStringList[1].isdigit():
                freq = int(argStringList[1])
            else:
                print('Error: frequency should be an integer')
                status = 0
        else:
            freq = 1
        return status, n, freq

    def ngramExtraction(self, type, argString):
        status, n, freq = self.ngramArgumentCheck(argString)
        if not status:
            # Error in argument.
            return

        ngramVoc = []
        listOfSentences = []
        if type is "plain":
            ngramVoc = self.preprocessor.buildTokenNgrams(n)
            listOfSentences = self.preprocessor.gettokenizeSents()
        elif type is "POS":
            ngramVoc = self.preprocessor.buildPOSNgrams(n)
            listOfSentences = self.preprocessor.nltkPOStag()
        elif type is "lemma":
            ngramVoc = self.preprocessor.buildLemmaNgrams(n)
            listOfSentences = self.preprocessor.getLemmatizedSents()
        elif type is "mixed":
            ngramVoc = self.preprocessor.buildMixedNgrams(n)
            listOfSentences = self.preprocessor.getMixedSents()

        finNgram = self.preprocessor.ngramMinFreq(ngramVoc, freq)
        allKeys = finNgram.keys()

        numberOfFeatures = len(allKeys)

        ngramFeatures = [[0 for j in range(len(listOfSentences))] for i in range(numberOfFeatures)]

        for i in range(len(listOfSentences)):
            ngramsVocab = Counter(ngrams(listOfSentences[i], n))
            for key in ngramsVocab:
                if key in allKeys:
                    counter_j = allKeys.index(key)
                    ngramFeatures[counter_j][i] = round(float(ngramsVocab[key]) / sum(ngramsVocab.values()), 2)

        return ngramFeatures

    @featid(4)
    def ngramBagOfWords(self, argString): 
        '''
        Extracts n-gram bag of words features.
        '''
        return self.ngramExtraction("plain", argString)

    @featid(5)
    def ngramPOSBagOfWords(self, argString): 
        '''
        Extracts n-gram POS bag of words features.
        '''
        return self.ngramExtraction("POS", argString)

    @featid(6)
    def ngramMixedBagOfWords(self, argString): 
        '''
        Extracts n-gram mixed bag of words features.
        '''
        return self.ngramExtraction("mixed", argString)
        
    @featid(7)
    def ngramLemmaBagOfWords(self, argString): 
        '''
        Extracts n-gram lemmatized bag of words features.
        '''
        return self.ngramExtraction("lemma", argString)
