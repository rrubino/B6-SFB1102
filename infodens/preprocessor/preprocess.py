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
from nltk.stem.wordnet import WordNetLemmatizer

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

    def getLanguageMode(self):
        """Return the current language mode."""
        return self.operatingLanguage

    def setLanguageMode(self, lang):
        """Set language mode for preprocessing operations."""
        self.operatingLanguage = lang

    def preprocessBySentence(self):
        """Load the input file which was specified at Init of object."""
        lines = []
        if self.inputFile:
            with codecs.open(self.inputFile, encoding='utf-8') as f:
                lines = f.read().splitlines()
        return lines

    def preprocessByBlock(self, fileName, blockSize):
        pass

    def preprocessClassID(self):
        """ Extract from each line the integer for class ID. Requires init with Classes file."""
        with codecs.open(self.inputFile, encoding='utf-8') as f:
            lines = f.read().splitlines()
        ids = [int(id) for id in lines]
        return ids

    def getPlainSentences(self):
        """Return sentences as read from file."""
        if not self.plainLof:
            self.plainLof = self.preprocessBySentence()
        return self.plainLof

    def gettokenizeSents(self):
        """Return tokenized sentences."""
        if not self.tokenSents:
            self.tokenSents = [nltk.word_tokenize(sent) for sent in self.getPlainSentences()]
        return self.tokenSents

    def getParseTrees(self):
        """Return parse trees of each sentence."""
        if not self.parseTrees:
            self.parseTrees = [parsetree(sent) for sent in self.getPlainSentences()]
        return

    def buildLanguageModel(self):
        """Build a language model from given corpus."""
        if not self.corpusForLM:
            print("Corpus for Language model not defined.")

    def nltkPOStag(self):
        """ Return POS tagged sentences. """
        if not self.nltkPOSSents:
            tagPOSSents = nltk.pos_tag_sents(self.gettokenizeSents())
            for i in range(0, len(tagPOSSents)):
                self.nltkPOSSents.append([wordAndTag[1] for wordAndTag in tagPOSSents[i]])
        return self.nltkPOSSents
        
    def getLemmatizedSents(self):
        """Lemmatize and return sentences."""
        if not self.lemmatizedSents:
            self.gettokenizeSents()
            lemmatizer = WordNetLemmatizer()
            for i in range(0,len(self.tokenSents)):
                lemmatized = [lemmatizer.lemmatize(a) for a in self.tokenSents[i]]
                self.lemmatizedSents.append(lemmatized)

        return self.lemmatizedSents
        
    def getMixedSents(self):
        """Build and return mixed sentences (POS for J,N,V, or R)"""
        if not self.mixedSents:
            self.nltkPOStag()
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

    def buildNgramsType(self, type, n):
        """Build and return given type of ngram."""
        if type is "plain":
            self.gettokenizeSents()
            ngramsList = [list(ngrams(self.tokenSents[i], n)) for i in range(len(self.tokenSents))]
        elif type is "POS":
            self.nltkPOStag()
            ngramsList = [list(ngrams(self.nltkPOSSents[i], n)) for i in range(len(self.nltkPOSSents))]
        elif type is "lemma":
            self.getLemmatizedSents()
            ngramsList = [list(ngrams(self.lemmatizedSents[i], n)) for i in range(len(self.lemmatizedSents))]
        elif type is "mixed":
            self.getMixedSents()
            ngramsList = [list(ngrams(self.mixedSents[i], n)) for i in range(len(self.mixedSents))]

        ngramsOutput = [item for sublist in ngramsList for item in sublist]  # flatten the list

        return Counter(ngramsOutput)

    def buildTokenNgrams(self, n):
        return self.buildNgramsType("plain",n)

    def buildPOSNgrams(self, n):
        return self.buildNgramsType("POS",n)

    def buildLemmaNgrams(self, n):
        return self.buildNgramsType("lemma",n)
        
    def buildMixedNgrams(self, n):
        return self.buildNgramsType("mixed",n)
        
    def ngramMinFreq(self, anNgram, freq):
        """Return anNgram with entries that have frequency greater or equal freq"""
        finalNgram = dict((k, anNgram[k]) for k in anNgram.keys() if anNgram[k] >= freq)
        return finalNgram
