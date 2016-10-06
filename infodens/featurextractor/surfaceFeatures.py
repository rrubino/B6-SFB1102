# -*- coding: utf-8 -*-
"""
Created on Sun Sep 04 14:12:49 2016

@author: admin
"""
from .featureExtraction import featid, FeatureExtractor
from collections import Counter


class SurfaceFeatures(FeatureExtractor):
    
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
        listOfSentences = []
        for sentence in self.preprocessor.getPlainSentences():
            sentence = sentence.strip()
            listOfSentences.append(sentence.split())
        oneToNgramVoc = [self.ngramsAllVoc(listOfSentences, i+1) for i in range(n)]#Will hold unigram, bigram ...ngram Vocabulary
        oneToNgramVocFreq = []
        for voc in oneToNgramVoc:
            oneToNgramVocFreq.append({k:v for k in voc.keys() for v in voc.values() if voc[k] == v if v >= freq})
        allKeys = []
        
        for vocab in oneToNgramVocFreq:
            allKeys.extend(vocab.keys())
        
        totalNumber = len(allKeys)
        ngramFeatures = [[0 for j in range(len(listOfSentences))] for i in range(totalNumber)]
        for i in range(len(listOfSentences)):
            sent_i = listOfSentences[i]
            allNgramsForSent_i = [self.ngrams(sent_i, k+1) for k in range(n)]
            ngramsVocab = [Counter(ng) for ng in allNgramsForSent_i]
            for j in range(len(ngramsVocab)):
                keys_j = ngramsVocab[j].keys()
                for key in keys_j:
                    if key in allKeys:
                        counter_j = allKeys.index(key)
                        ngramFeatures[counter_j][i] = float(ngramsVocab[j][key]) / sum(ngramsVocab[j].values())
        return ngramFeatures
