# -*- coding: utf-8 -*-
"""
Created on Sun Sep 04 14:12:49 2016

@author: admin
"""
from .featureExtraction import featid, FeatureExtractor
from collections import Counter
from nltk import ngrams
import numpy as np
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

        print("Ngrams built.")

        finNgram, numberOfFeatures = self.preprocessor.ngramMinFreq(ngramVoc, freq)

        print("Cut off done. ")

        if numberOfFeatures == 0:
            print("Cut-off too high, no ngrams passed it.")
            return []

        ngramFeatures = np.zeros((len(listOfSentences), numberOfFeatures))

        print("Extracting ngram feats.")

        for i in range(len(listOfSentences)):
            ngramsVocab = Counter(ngrams(listOfSentences[i], n))
            lenSent = len(listOfSentences[i])
            for ngramEntry in ngramsVocab:
                ## Keys
                ngramIndex = finNgram.get(ngramEntry, -1)
                if ngramIndex >= 0:
                    ngramFeatures[i][ngramIndex] = round((float(ngramsVocab[ngramEntry]) / lenSent), 2)

        print("Finished ngram features.")
        ngramLength = "Ngram feature vector length: " + str(numberOfFeatures)
        print(ngramLength)

        return ngramFeatures.tolist()

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
