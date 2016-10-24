# -*- coding: utf-8 -*-
"""
Created on Tue Aug 30 15:19:12 2016

@author: admin
"""
import codecs
import time
import nltk
from pattern.en import parsetree
from nltk import ngrams
from collections import Counter
from nltk.stem.porter import PorterStemmer
porter_stemmer = PorterStemmer()



class Preprocess:
    
    fileName = ''
    
    def __init__(self,fileName,corpusLM=0,language=0):
        self.inputFile = fileName
        self.corpusForLM = corpusLM
        self.operatingLanguage = language
        self.plainLof = []
        self.tokenSents = []
        self.parseTrees = []
        self.nltkPOSSents = []
        self.lemmatizedSents = []
        self.mixedSents = []
        self.ngramsTokDict = {}
        self.ngramsLemmaDict = {}
        self.ngramsPOSDict = {}
        self.ngramsMixedDict = {}

    def getLanguageMode(self):
        return self.operatingLanguage

    def setLanguageMode(self, lang):
        self.operatingLanguage = lang

    def preprocessBySentence(self):
        with codecs.open(self.inputFile, encoding='utf-8') as f:
            lines = f.read().splitlines()
        return lines

    def preprocessClassID(self):
        """ Extract from each line the integer for class ID."""

        with codecs.open(self.inputFile, encoding='utf-8') as f:
            lines = f.read().splitlines()
        ids = [int(id) for id in lines]
        
        return ids

    def preprocessByBlock(self, fileName, blockSize):
        pass

    def getPlainSentences(self):
        if not self.plainLof:
            self.plainLof = self.preprocessBySentence()
        return self.plainLof

    def gettokenizeSents(self):
        if not self.tokenSents:
            self.tokenSents = [nltk.word_tokenize(sent) for sent in self.getPlainSentences()]
        return self.tokenSents

    def getParseTrees(self):
        if not self.parseTrees:
            self.parseTrees = [parsetree(sent) for sent in self.getPlainSentences()]
        return

    def buildLanguageModel(self):
        if not self.corpusForLM:
            print("Corpus for Language model not defined.")

    def nltkPOStag(self):
        """ Tag given sentences with POS of nltk. """
        if not self.nltkPOSSents:
            self.nltkPOSSents = [nltk.pos_tag(tokens) for tokens in self.gettokenizeSents()]
        return self.nltkPOSSents
        
    def getLemmatizedSents(self):
        if not self.plainLof:
            self.plainLof = self.preprocessBySentence()
        lemmatized = [porter_stemmer.stem(a) for a in self.plainLof]   
        self.lemmatizedSents = [nltk.word_tokenize(tokens) for tokens in lemmatized]
        return self.lemmatizedSents
        
    def getMixedSents(self):        
        if not self.plainLof:
            self.plainLof = self.preprocessBySentence()
        if not self.tokenSents:
            self.gettokenizeSents()
        self.nltkPOSSents = self.nltkPOStag()
        
        for i in range(len(self.tokenSents)):
            sent = []
            for j in range(len(self.tokenSents[i])):
                if self.nltkPOSSents[i][j].startswith('J') or \
                        self.nltkPOSSents[i][j].startswith('N') or \
                        self.nltkPOSSents[i][j].startswith('V') or \
                        self.nltkPOSSents[i][j].startswith('R'):
                    sent.append(self.nltkPOSSents[i][j])
                else:
                    sent.append(self.tokenSents[i][j])
            self.mixedSents.append(sent)
            
        return self.mixedSents

    def buildTokenNgrams(self, n):
        print('Building token Ngrams')
        start_time = time.time()
        if not self.tokenSents:
            self.gettokenizeSents()        
        ngramsToksList = [list(ngrams(self.tokenSents[i], n)) for i in range(len(self.tokenSents))]
        ngramsToks = [item for sublist in ngramsToksList for item in sublist] #flatten the list
        self.ngramsTokDict[n] = Counter(ngramsToks)
        print('Done building token Ngrams, it took ', time.time() - start_time, ' seconds')
        return self.ngramsTokDict[n]

    def buildPOSNgrams(self, n):
        print('Building POS Ngrams')
        start_time = time.time()
        if not self.nltkPOSSents:
            self.nltkPOStag()        
        ngramsPOSList = [list(ngrams(self.nltkPOSSents[i], n)) for i in range(len(self.nltkPOSSents))]
        ngramsPOS = [item for sublist in ngramsPOSList for item in sublist] #flatten the list
        self.ngramsPOSDict[n] = Counter(ngramsPOS)
        print('Done building POS Ngrams, it took ', time.time() - start_time, ' seconds')
        return self.ngramsPOSDict[n]

    def buildLemmaNgrams(self, n):
        print('Building Lemma Ngrams')
        start_time = time.time()
        if not self.lemmatizedSents:
            self.getLemmatizedSents()        
        ngramsLemmaList = [list(ngrams(self.lemmatizedSents[i], n)) for i in range(len(self.lemmatizedSents))]
        ngramsLemma = [item for sublist in ngramsLemmaList for item in sublist] #flatten the list
        self.ngramsLemmaDict[n] = Counter(ngramsLemma)
        print('Done building Lemma Ngrams, it took ', time.time() - start_time, ' seconds')
        return self.ngramsLemmaDict[n]
        
    def buildMixedNgrams(self, n):
        print('Building Mixed Ngrams')
        start_time = time.time()
        if not self.mixedSents:
            self.getMixedSents()        
        ngramsMixedList = [list(ngrams(self.mixedSents[i], n)) for i in range(len(self.mixedSents))]
        ngramsMixed = [item for sublist in ngramsMixedList for item in sublist] #flatten the list
        self.ngramsMixedDict[n] = Counter(ngramsMixed)
        print ('Done building Mixed Ngrams, it took ', time.time() - start_time, ' seconds')
        return self.ngramsMixedDict[n]
        
    def ngramMinFreq(self, anNgram, freq):
        print('Getting ngram with minimum frequency')
        start_time = time.time()
        finalNgram = dict((k, anNgram[k]) for k in anNgram.keys() if anNgram[k] >= freq)
        print('Done ngram with minimum frequency, it took ', time.time() - start_time, ' seconds')
        return finalNgram
