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
import gensim
from nltk.stem.wordnet import WordNetLemmatizer
import subprocess
import os
try:  # py3
    from shlex import quote
except ImportError:  # py2
    from pipes import quote

class Preprocess:
    
    fileName = ''
    
    def __init__(self, fileName, corpusLM=0, nthreads=1, language=0, srilmpath=os.getcwd()):
        self.inputFile = fileName
        self.corpusForLM = corpusLM
        self.operatingLanguage = language
        self.sentCount = 0
        self.threadsCount = nthreads
        self.plainLof = []
        self.tokenSents = []
        self.parseTrees = []
        self.taggedPOSSents = []
        self.lemmatizedSents = []
        self.mixedSents = []
        self.word2vecModel = {}
        self.langModelFiles = []
        self.srilmBinaries = srilmpath

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
                lines = f.readlines()
        return lines

    def preprocessByBlock(self, fileName, blockSize):
        pass

    def preprocessClassID(self):
        """ Extract from each line the integer for class ID. Requires init with Classes file."""
        with codecs.open(self.inputFile, encoding='utf-8') as f:
            lines = f.readlines()
        ids = [int(id) for id in lines]
        return ids

    def getSentCount(self):
        self.getPlainSentences()
        return self.sentCount

    def getInputFileName(self):
        return self.inputFile

    def getPlainSentences(self):
        """Return sentences as read from file."""
        if not self.plainLof:
            self.plainLof = self.preprocessBySentence()
            self.sentCount = len(self.plainLof)
        return self.plainLof

    def gettokenizeSents(self):
        """Return tokenized sentences."""
        if not self.tokenSents:
            #print("tokenizing")
            self.tokenSents = [nltk.word_tokenize(sent) for sent in self.getPlainSentences()]

        return self.tokenSents

    def getParseTrees(self):
        """Return parse trees of each sentence."""
        if not self.parseTrees:
            self.parseTrees = [parsetree(sent) for sent in self.getPlainSentences()]
        return

    def buildLanguageModel(self, ngram=3):
        """Build a language model from given corpus."""

        langModelFile = "{0}_langModel{1}".format(self.corpusForLM, ngram)
        #binaryLib = "{0}\\ngram-count".format(self.srilmBinaries)
        binaryLib = "ngram-count"
        # if "Linux" in platform.system():
        #    commandToRun += "./"
        if not self.corpusForLM:
            print("Corpus for Language model not defined.")
        elif langModelFile in self.langModelFiles:
            return langModelFile
        else:
            #corpusAbsolute = "{0}\\{1}".format(os.getcwd(), self.corpusForLM)
            #./ngram-count -text [corpus] -lm [output_language_model] -order 3 -write [output_ngram_file_path]
            commandToRun = "{0} -text {1} -lm {2} -order {3} -kndiscount".format(binaryLib, self.corpusForLM,
                                                                      langModelFile, ngram)
            print("Building Language Model..")
            #commandToRun = quote(commandToRun)
            #print(commandToRun)
            subprocess.call(commandToRun, shell=True)
            print("Language Model done.")
            self.langModelFiles.append(langModelFile)

            return langModelFile

    def getPOStagged(self, filePOS=0):
        """ Return POS tagged sentences. """
        if not self.taggedPOSSents:
            if not filePOS:
                print("POS tagging..")
                tagPOSSents = nltk.pos_tag_sents(self.gettokenizeSents())
                for i in range(0, len(tagPOSSents)):
                    self.taggedPOSSents.append([wordAndTag[1] for wordAndTag in tagPOSSents[i]])
                print("POS tagging done.")
            else:
                with codecs.open(filePOS, encoding='utf-8') as f:
                    lines = f.readlines()
                # POS from file is not stored but returned directly
                return [nltk.word_tokenize(sent) for sent in lines]

        return self.taggedPOSSents
        
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
            self.getPOStagged()
            for i in range(len(self.tokenSents)):
                sent = []
                for j in range(len(self.tokenSents[i])):
                    if self.taggedPOSSents[i][j].startswith('J') or \
                            self.taggedPOSSents[i][j].startswith('N') or \
                            self.taggedPOSSents[i][j].startswith('V') or \
                            self.taggedPOSSents[i][j].startswith('R'):
                        sent.append(self.taggedPOSSents[i][j])
                    else:
                        sent.append(self.tokenSents[i][j])
                self.mixedSents.append(sent)
            
        return self.mixedSents

    def trainWord2Vec(self, vecSize=100):
        print("Training Word2Vec model...")

        class SentIterator(object):
            def __init__(self, corpus):
                self.corpus = corpus

            def __iter__(self):
                with codecs.open(self.corpus, encoding='utf-8') as corpusFile:
                    for line in corpusFile:
                        yield nltk.word_tokenize(line)

        if not self.corpusForLM:
            tokenizedCorpus = SentIterator(self.gettokenizeSents())
        else:
            tokenizedCorpus = SentIterator(self.corpusForLM)

        model = gensim.models.Word2Vec(tokenizedCorpus, size=vecSize, min_count=1, workers=self.threadsCount)
        print("Word2Vec model done.")

        return model

    def getWord2vecModel(self, size=100):
        if size not in self.word2vecModel.keys():
            self.word2vecModel[size] = self.trainWord2Vec(size)
        return self.word2vecModel[size]

    def buildNgramsType(self, type, n, freq, filePOS=0):
        """Build and return given type of ngram."""
        if type is "plain":
            self.gettokenizeSents()
            ngramsList = [list(ngrams(self.tokenSents[i], n)) for i in range(len(self.tokenSents))]
        elif type is "POS":
            self.getPOStagged(filePOS)
            ngramsList = [list(ngrams(self.taggedPOSSents[i], n)) for i in range(len(self.taggedPOSSents))]
        elif type is "lemma":
            self.getLemmatizedSents()
            ngramsList = [list(ngrams(self.lemmatizedSents[i], n)) for i in range(len(self.lemmatizedSents))]
        elif type is "mixed":
            self.getMixedSents()
            ngramsList = [list(ngrams(self.mixedSents[i], n)) for i in range(len(self.mixedSents))]
        else:
            #treat as plain
            self.gettokenizeSents()
            ngramsList = [list(ngrams(self.tokenSents[i], n)) for i in range(len(self.tokenSents))]

        ngramsOutput = [item for sublist in ngramsList for item in sublist]  # flatten the list

        return self.ngramMinFreq(Counter(ngramsOutput), freq)

    def buildTokenNgrams(self, n, freq):
        return self.buildNgramsType("plain", n, freq)

    def buildPOSNgrams(self, n, freq, filePOS=0):
        return self.buildNgramsType("POS", n, freq, filePOS)

    def buildLemmaNgrams(self, n, freq):
        return self.buildNgramsType("lemma", n, freq)
        
    def buildMixedNgrams(self, n, freq):
        return self.buildNgramsType("mixed", n, freq)
        
    def ngramMinFreq(self, anNgram, freq):
        indexOfngram = 0
        finalNgram = {}
        """Return anNgram with entries that have frequency greater or equal freq"""
        for k in anNgram.keys():
            if anNgram[k] >= freq:
                finalNgram[k] = indexOfngram
                indexOfngram += 1

        return finalNgram, indexOfngram
