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

    @featid(4)
    def ngramBagOfWords(self, argString): 
        '''
        Extracts n-gram bag of words features from listOf Sentences
        argString: is read off the config file and converted to integer if it is digit. If it is not a digit, an error is returned
        
        '''
        argStringList = argString.split(',')
        if argStringList[0].isdigit():
            n = int(argStringList[0])
        else:
            print('Error: n should be an integer')
            return
        if len(argStringList) > 1:
            if argStringList[1].isdigit():
                freq = int(argStringList[1])
            else:
                print('Error: frequency should be an integer')
                return
        else:
            freq = 1
        #oneToNgramList = []
            
        ngramVoc = self.preprocessor.buildTokenNgrams(n)
        finNgram = self.preprocessor.ngramMinFreq(ngramVoc, freq)
        allKeys = finNgram.keys()
        
        listOfSentences = self.preprocessor.gettokenizeSents() 
             
        totalNumber = len(allKeys)

        ngramFeatures = [[0 for j in range(len(listOfSentences))] for i in range(totalNumber)]
        
        start_time = time.time()
        for i in range(len(listOfSentences)):            
            ngramsVocab = Counter(ngrams(listOfSentences[i], n))            
            for key in ngramsVocab:
                if key in allKeys:
                    counter_j = allKeys.index(key)
                    ngramFeatures[counter_j][i] = float(ngramsVocab[key]) / sum(ngramsVocab.values())
        
        print('Extracted Ngram, took ', (time.time() - start_time), ' seconds' )
        
        return ngramFeatures   

    @featid(5)
    def ngramPOSBagOfWords(self, argString): 
        '''
        Extracts n-gram bag of words features from listOf Sentences
        argString: is read off the config file and converted to integer if it is digit. If it is not a digit, an error is returned
        
        '''
        argStringList = argString.split(',')
        if argStringList[0].isdigit():
            n = int(argStringList[0])
        else:
            print('Error: n should be an integer')
            return
        if len(argStringList) > 1:
            if argStringList[1].isdigit():
                freq = int(argStringList[1])
            else:
                print('Error: frequency should be an integer')
                return
        else:
            freq = 1
        #oneToNgramList = []
            
        ngramVoc = self.preprocessor.buildPOSNgrams(n)
        finNgram = self.preprocessor.ngramMinFreq(ngramVoc, freq)
        allKeys = finNgram.keys()
        
        listOfSentences = self.preprocessor.gettokenizeSents() 
             
        totalNumber = len(allKeys)

        ngramFeatures = [[0 for j in range(len(listOfSentences))] for i in range(totalNumber)]
        
        print ('Extracting features from all sentences ')
        start_time = time.time()
        for i in range(len(listOfSentences)):            
            ngramsVocab = Counter(ngrams(listOfSentences[i], n))            
            for key in ngramsVocab:
                if key in allKeys:
                    counter_j = allKeys.index(key)
                    ngramFeatures[counter_j][i] = float(ngramsVocab[key]) / sum(ngramsVocab.values())
        
        print('Done Extracting features from all sentences it took ', (time.time() - start_time), ' seconds' )

        return ngramFeatures   

    @featid(6)
    def ngramMixedBagOfWords(self, argString): 
        '''
        Extracts n-gram bag of words features from listOf Sentences
        argString: is read off the config file and converted to integer if it is digit. If it is not a digit, an error is returned
        
        '''
        argStringList = argString.split(',')
        if argStringList[0].isdigit():
            n = int(argStringList[0])
        else:
            print('Error: n should be an integer')
            return
        if len(argStringList) > 1:
            if argStringList[1].isdigit():
                freq = int(argStringList[1])
            else:
                print('Error: frequency should be an integer')
                return
        else:
            freq = 1
        #oneToNgramList = []
            
        ngramVoc = self.preprocessor.buildMixedNgrams(n)
        finNgram = self.preprocessor.ngramMinFreq(ngramVoc, freq)
        allKeys = finNgram.keys()
        
        listOfSentences = self.preprocessor.gettokenizeSents() 
             
        totalNumber = len(allKeys)

        ngramFeatures = [[0 for j in range(len(listOfSentences))] for i in range(totalNumber)]

        print ('Extracting features from all sentences ')
        start_time = time.time()
        for i in range(len(listOfSentences)):            
            ngramsVocab = Counter(ngrams(listOfSentences[i], n))            
            for key in ngramsVocab:
                if key in allKeys:
                    counter_j = allKeys.index(key)
                    ngramFeatures[counter_j][i] = float(ngramsVocab[key]) / sum(ngramsVocab.values())
        
        print('Done Extracting features from all sentences it took ', (time.time() - start_time), ' seconds' )

        return ngramFeatures   
        
    @featid(7)
    def ngramLemmaBagOfWords(self, argString): 
        '''
        Extracts n-gram bag of words features from listOf Sentences
        argString: is read off the config file and converted to integer if it is digit. If it is not a digit, an error is returned
        
        '''
        argStringList = argString.split(',')
        if argStringList[0].isdigit():
            n = int(argStringList[0])
        else:
            print('Error: n should be an integer')
            return
        if len(argStringList) > 1:
            if argStringList[1].isdigit():
                freq = int(argStringList[1])
            else:
                print('Error: frequency should be an integer')
                return
        else:
            freq = 1
        #oneToNgramList = []
            
        ngramVoc = self.preprocessor.buildLemmaNgrams(n)
        finNgram = self.preprocessor.ngramMinFreq(ngramVoc, freq)
        allKeys = finNgram.keys()
        
        listOfSentences = self.preprocessor.gettokenizeSents() 
             
        totalNumber = len(allKeys)

        ngramFeatures = [[0 for j in range(len(listOfSentences))] for i in range(totalNumber)]

        print('Extracting features from all sentences ')
        start_time = time.time()
        for i in range(len(listOfSentences)):            
            ngramsVocab = Counter(ngrams(listOfSentences[i], n))            
            for key in ngramsVocab:
                if key in allKeys:
                    counter_j = allKeys.index(key)
                    ngramFeatures[counter_j][i] = float(ngramsVocab[key]) / sum(ngramsVocab.values())
        
        print('Done Extracting features from all sentences it took ', (time.time() - start_time), ' seconds' )
               
        return ngramFeatures
