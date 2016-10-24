# -*- coding: utf-8 -*-
"""
Created on Sun Sep 04 14:12:49 2016

@author: admin
"""
from .featureExtraction import featid, FeatureExtractor
from collections import Counter
from nltk import ngrams
import time


class SurfaceFeatures(FeatureExtractor):
    
    @featid(1)    
    def averageWordLength(self, argString):
        '''Find average word length of every sentence and return list. '''

        aveWordLen = []
        for sentence in self.preprocessor.gettokenizeSents():
            if len(sentence) is 0:
                aveWordLen.append(0)
            else:
                length = sum([len(s) for s in sentence])
                aveWordLen.append(float(length) / len(sentence))

        return aveWordLen

    @featid(10)
    def sentenceLength(self, argString):
        '''Find length of every sentence and return list. '''

        sentLen = []
        for sentence in self.preprocessor.gettokenizeSents():
            sentLen.append(len(sentence))

        return sentLen

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
        sylRatios = []
        for sentence in self.preprocessor.gettokenizeSents():
            sylCount = 0
            for word in sentence:
                word2List = list(word)
                for i in range(len(word2List)-1):
                    if word2List[i] in vowels and word2List[i+1] not in vowels:
                        sylCount += 1

            if len(sentence) is 0:
                sylRatios.append(0)
            else:
                sylRatios.append(float(sylCount)/len(sentence))

        return sylRatios

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
        
        print ('Extracting features from all sentences ')
        start_time = time.time()
        for i in range(len(listOfSentences)):            
            ngramsVocab = Counter(ngrams(listOfSentences[i], n))            
            for key in ngramsVocab:
                if key in allKeys:
                    counter_j = allKeys.index(key)
                    ngramFeatures[counter_j][i] = float(ngramsVocab[key]) / sum(ngramsVocab.values())
        
        print ('Done Extracting features from all sentences it took ', (time.time() - start_time), ' seconds' )
        
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
