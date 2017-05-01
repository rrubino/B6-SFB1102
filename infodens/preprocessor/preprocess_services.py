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
import subprocess
import os
import time


class Preprocess_Services:

    def __init__(self, srilmBinaries="", lang="eng"):
        self.srilmBinaries = srilmBinaries
        self.operatingLanguage = lang

    def preprocessBySentence(self, inputFile):
        """Load the input file which was specified at Init of object."""
        lines = []
        with codecs.open(inputFile, encoding='utf-8') as f:
            lines = f.readlines()
        return lines

    def preprocessByBlock(self, fileName, blockSize):
        pass

    def preprocessClassID(self, inputClasses):
        """ Extract from each line the integer for class ID. Requires init with Classes file."""
        with codecs.open(inputClasses, encoding='utf-8') as f:
            lines = f.readlines()
        ids = [int(id) for id in lines]
        return ids

    def getFileTokens(self, fileOfTokens):
        """Return tokens from file"""
        return [nltk.word_tokenize(sent) for sent in self.preprocessBySentence(fileOfTokens)]

    def dumpTokensTofile(self, dumpFile, tokenSents):
        """ Dump tokens into file"""
        if not os.path.isfile(dumpFile):
            outFile = open(dumpFile, 'w')
            for sent in tokenSents:
                outFile.write("%s\n" % " ".join(sent))
            outFile.close()
        return dumpFile

    def tagPOSfromFile(self, filePOS):
        """ Return POS tagged sentences from given File """
        taggedPOSSents = []
        print("POS tagging..")
        tagPOSSents = nltk.pos_tag_sents(self.getFileTokens(filePOS),lang=self.operatingLanguage)
        for i in range(0, len(tagPOSSents)):
            taggedPOSSents.append([wordAndTag[1] for wordAndTag in tagPOSSents[i]])
        print("POS tagging done.")
        return taggedPOSSents

    def languageModelBuilder(self, ngram, corpus, langModelFile, kndiscount=True):
        """Build a language model from given corpus."""

        binaryLib = ("\"{0}ngram-count\"".format(self.srilmBinaries))
        discount = ""

        if kndiscount:
            discount = " -kndiscount"

        #print(langModelFile)
        # ./ngram-count -text [corpus] -lm [output_language_model] -order 3 -write [output_ngram_file_path]
        commandToRun = "{0} -text {1} -lm {2} -order {3}{4}".format(binaryLib, corpus,
                                                                                 langModelFile, ngram, discount)

        print("Building Language Model..")
        #print(commandToRun)
        subprocess.call(commandToRun, shell=True)
        print("Language Model done.")

        return langModelFile

    def trainWord2Vec(self, vecSize, corpus, threadsCount):
        import gensim
        print("Training Word2Vec model...")

        class SentIterator(object):
            def __init__(self, corpus):
                self.corpus = corpus

            def __iter__(self):
                with codecs.open(self.corpus, encoding='utf-8') as corpusFile:
                    for line in corpusFile:
                        yield nltk.word_tokenize(line)

        tokenizedCorpus = SentIterator(corpus)

        model = gensim.models.Word2Vec(tokenizedCorpus, size=vecSize, min_count=1, workers=threadsCount)
        print("Word2Vec model done.")

        return model

    def ngramMinFreq(self, anNgram, freq):
        indexOfngram = 0
        finalNgram = {}
        """Return anNgram with entries that have frequency greater or equal freq"""
        for k in anNgram.keys():
            if anNgram[k] >= freq:
                finalNgram[k] = indexOfngram
                indexOfngram += 1

        return finalNgram, indexOfngram
