# -*- coding: utf-8 -*-
"""
Created on Tue Aug 30 15:19:12 2016

@author: admin
"""
import codecs
import nltk

class Preprocess:
    
    fileName = ''
    
    def __init__(self):
        pass

    def preprocessBySentence(self, fileName):

        with codecs.open(fileName, encoding='utf-8') as f:
            lines = f.read().splitlines()
        return lines

    def preprocessClassID(self, fileName):
        """ Extract from each line the integer for class ID."""
        
        with codecs.open(fileName, encoding='utf-8') as f:
            lines = f.read().splitlines()
        ids = [int(id) for id in lines]
        
        return ids

    def preprocessByBlock(self,fileName, blockSize):
        pass

    def nltkPOStag(self, sentencesList):
        """ Tag given sentences with POS of nltk. """

        tokenSent = [nltk.word_tokenize(sent) for sent in sentencesList]
        taggedSents = [nltk.pos_tag(tokens) for tokens in tokenSent]

        return taggedSents
