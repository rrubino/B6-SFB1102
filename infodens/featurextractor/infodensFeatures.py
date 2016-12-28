from __future__ import division
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 15 11:16:36 2016

@author: admin
"""
from .featureExtraction import featid, FeatureExtractor
from infodens.preprocessor import preprocess
import numpy as np

from collections import Counter
from nltk import ngrams

class InfodensFeatures(FeatureExtractor):
    
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
    
    
    @featid(13)        
    def ngramCBSurprisal(self, argString):
        '''
        We compute how surprising it is to see a word for each class
        '''
        status, n, freq = self.ngramArgumentCheck(argString)
        if not status:
            # Error in argument.
            return
        
        CBS = self.preprocessor.buildClassBasedNgrams('plain', n)        
        listOfSentences = self.preprocessor.gettokenizeSents()
        wordMinFreq = {}; numFeats = {};
        features = {}
        for key in CBS:
            wordMinFreq[key], numFeats[key] = self.preprocessor.ngramMinFreq(CBS[key], freq)            
            
            #features[key] = np.zeros((len(listOfSentences), numFeats[key]))
            feats = np.zeros((len(listOfSentences), numFeats[key]))
            
            i=0;
            for sentence in listOfSentences:
                ngramsVocab = Counter(ngrams(sentence, n))
                
                for eachunigram in ngramsVocab:
                    ngramIndex = wordMinFreq[key].get(eachunigram, -1)                    
                    if ngramIndex >= 0:                       
                        result = CBS[key][eachunigram] + 1
                        result /= (sum(CBS[key].values()) + len(CBS[key]))
                        result = -1 * np.log2(result)
                        
                        feats[i][ngramIndex] = result
                i += 1           
            features[key] = feats
        
        keys = features.keys()
        finalFeatures = features[keys[0]]
        for i in range(1,len(keys)):
            finalFeatures = np.concatenate((finalFeatures, features[keys[i]]), axis=1)
            
        return finalFeatures.tolist()
        
        
    @featid(14)        
    def ngramPOSCBSurprisal(self, argString):
        '''
        We compute how surprising it is to see a word for each class
        '''
        
        status, n, freq = self.ngramArgumentCheck(argString)
        if not status:
            # Error in argument.
            return
        CBS = self.preprocessor.buildClassBasedNgrams('POS', n)
        listOfSentences = self.preprocessor.nltkPOStag()
        wordMinFreq = {}; numFeats = {};
        features = {}
        for key in CBS:
            wordMinFreq[key], numFeats[key] = self.preprocessor.ngramMinFreq(CBS[key], freq)
            #features[key] = np.zeros((len(listOfSentences), numFeats[key]))
            feats = np.zeros((len(listOfSentences), numFeats[key]))
            
            i=0;
            for sentence in listOfSentences:
                ngramsVocab = Counter(ngrams(sentence, 2))
                for eachunigram in ngramsVocab:
                    ngramIndex = wordMinFreq[key].get(eachunigram, -1)
                    
                    if ngramIndex >= 0:
                        result = CBS[key][eachunigram] + 1
                        result /= (sum(CBS[key].values()) + len(CBS[key]))
                        result = -1 * np.log2(result)
                        feats[i][ngramIndex] = result
                i += 1           
            features[key] = feats
        
        keys = features.keys()
        finalFeatures = features[keys[0]]
        for i in range(1,len(keys)):
            finalFeatures = np.concatenate((finalFeatures, features[keys[i]]), axis=1)
            
        return finalFeatures.tolist()
                    
    
        
    @featid(15)        
    def ngramSurprisal(self, argString):
        '''
        We compute how surprising it is to see a word for each class
        '''
        status, n, freq = self.ngramArgumentCheck(argString)
        if not status:
            # Error in argument.
            return
        
        CBS = self.preprocessor.buildNgramsType('plain', n)
        listOfSentences = self.preprocessor.gettokenizeSents()
                
        wordMinFreq, numFeats = self.preprocessor.ngramMinFreq(CBS, freq)
        #features[key] = np.zeros((len(listOfSentences), numFeats[key]))
        feats = np.zeros((len(listOfSentences), numFeats))
        
        i=0;
        for sentence in listOfSentences:
            ngramsVocab = Counter(ngrams(sentence, n))
            for eachunigram in ngramsVocab:
                ngramIndex = wordMinFreq.get(eachunigram, -1)
                
                if ngramIndex >= 0:
                    result = CBS[eachunigram] + 1
                    result /= (sum(CBS.values()) + len(CBS))
                    result = -1 * np.log2(result)
                    feats[i][ngramIndex] = result
            i += 1           
        features = feats
        
                    
        return features.tolist()
        
        
    @featid(16)        
    def ngramPOSSurprisal(self, argString):
        '''
        We compute how surprising it is to see a word for each class
        '''
        status, n, freq = self.ngramArgumentCheck(argString)
        if not status:
            # Error in argument.
            return
        
        CBS = self.preprocessor.buildNgramsType('POS', n)
        listOfSentences = self.preprocessor.nltkPOStag()
                
        wordMinFreq, numFeats = self.preprocessor.ngramMinFreq(CBS, freq)
        #features[key] = np.zeros((len(listOfSentences), numFeats[key]))
        feats = np.zeros((len(listOfSentences), numFeats))
        
        i=0;
        for sentence in listOfSentences:
            ngramsVocab = Counter(ngrams(sentence, n))
            for eachunigram in ngramsVocab:
                ngramIndex = wordMinFreq.get(eachunigram, -1)
                
                if ngramIndex >= 0:
                    result = CBS[eachunigram] + 1
                    result /= (sum(CBS.values()) + len(CBS))
                    result = -1 * np.log2(result)
                    feats[i][ngramIndex] = result
            i += 1           
        features = feats
        
                    
        return features.tolist()
        
        
    @featid(17)        
    def lengthSurprisal(self, argString):
        '''
        We compute how surprising it is to see a word for each class
        '''
        
        CBS = self.preprocessor.buildLengthBasedDict()
        listOfSentences = self.preprocessor.gettokenizeSents()                
        numFeats = len(CBS)
        featsIndex = sorted(CBS.keys())
        #features[key] = np.zeros((len(listOfSentences), numFeats[key]))
        feats = np.zeros((len(listOfSentences), numFeats))
        
        i=0;
        for sentence in listOfSentences:
            
            for token in sentence:
                ngramIndex = featsIndex.index(len(token))                
                if ngramIndex >= 0:
                    result = CBS[len(token)] + 1
                    result /= (sum(CBS.values()) + len(CBS))
                    result = -1 * np.log2(result)
                    feats[i][ngramIndex] = result
            i += 1           
        features = feats
        
                    
        return features.tolist()
            
        
        

    