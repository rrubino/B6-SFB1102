# -*- coding: utf-8 -*-
"""
Created on Sun Sep 04 14:12:49 2016

@author: admin
"""
from .utils import featid
from collections import Counter


class SurfaceFeatures:
    
    
    def __init__(self, preprocessed):
        '''
        Initializes the class with a preprocessor. '''
        self.preprocessor = preprocessed
        self.listOfSentences = []
        for sentence in self.preprocessor.getPlainSentences():
            sentence = sentence.strip()
            self.listOfSentences.append(sentence.split())
    
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
        
    
    def ngrams(self, input, n):
      output = []
      for i in range(len(input)-n+1):
        output.append(input[i:i+n])
      return [' '.join(x) for x in output]
    
    
    def ngramsAllVoc(self, input, n):      
        ngramsList = []
        for eachInput in input:
            ngramsList.append(self.ngrams(eachInput, n))
          
        ngramsExtend = []
        for eachNgram in ngramsList:
            ngramsExtend.extend(eachNgram)
            
        vocabulary = Counter(ngramsExtend)
        return vocabulary
    
      
      
    
        
    
    @featid(4)
    def ngramBagOfWords(self, argString): 
        if argString.isdigit():
            n = int(argString)
        else:
            print('Error: n should be an integer')
            return
        #oneToNgramList = [] 
        oneToNgramVoc = [self.ngramsAllVoc(self.listOfSentences, i+1) for i in range(n)]#Will hold unigram, bigram ...ngram Vocabulary
        allKeys = []
        
        for vocab in oneToNgramVoc:
            allKeys.extend(vocab.keys())
        
        totalNumber = len(allKeys)
        ngramFeatures = [[0 for j in range(len(self.listOfSentences))] for i in range(totalNumber)]
        for i in range(len(self.listOfSentences)):
            sent_i = self.listOfSentences[i]
            allNgramsForSent_i = [self.ngrams(sent_i, k+1) for k in range(n)]
            ngramsVocab = [Counter(ng) for ng in allNgramsForSent_i]
            for j in range(len(ngramsVocab)):
                keys_j = ngramsVocab[j].keys()
                for key in keys_j:
                    counter_j = allKeys.index(key)
                    ngramFeatures[counter_j][i] = float(ngramsVocab[j][key]) / sum(ngramsVocab[j].values())
        return ngramFeatures
        
   