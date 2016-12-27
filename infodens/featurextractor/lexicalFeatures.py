# -*- coding: utf-8 -*-
"""
Created on Thu Sep 15 11:16:36 2016

@author: admin
"""
from .featureExtraction import featid, FeatureExtractor
from infodens.preprocessor import preprocess
import numpy as np

class LexicalFeatures(FeatureExtractor):
    
    def computeDensity(self, taggedSentences, jnrv):
        densities = np.zeros(self.preprocessor.getSentCount())
        #jnrv = ['J', 'N', 'R', 'V'] # nouns, adjectives, adverbs or verbs.

        i = 0
        for sent in taggedSentences:
            if(len(sent) is 0):
                densities[i] = 0
            else:
                jnrvList = [tagPOS for tagPOS in sent if tagPOS in jnrv]
                densities[i] = (float(len(sent) - len(jnrvList)) / len(sent))
            i += 1

        return densities

    @featid(3)        
    def lexicalDensity(self, argString, featOrder):
        jnrv = argString.split(',')
        '''
        The frequency of tokens that are not nouns, adjectives, adverbs or verbs. 
        This is computed by dividing the number of tokens tagged with POS tags 
        that do not start with J, N, R or V by the number of tokens in the chunk
        '''
        taggedSents = self.preprocessor.nltkPOStag()

        fileName = "3-" + str(featOrder) + ".npy"
        np.save(fileName, self.computeDensity(taggedSents, jnrv))
        return fileName

    @featid(11)
    def lexicalRichness(self, argString, featOrder):
        '''
        The ratio of unique tokens in the sentence over the sentence length.
        '''

        #TODO : Lemmatize tokens?
        sentRichness = np.zeros(self.preprocessor.getSentCount())

        i = 0
        for sentence in self.preprocessor.gettokenizeSents():
            if len(sentence) is 0:
                sentRichness[i] = 0
            else:
                sentRichness[i] = (float(len(set(sentence)))/len(sentence))
            i += 1

        fileName = "11-" + str(featOrder) + ".npy"
        np.save(fileName, sentRichness)
        return fileName

    @featid(12)
    def lexicalToTokens(self, argString, featOrder):
        '''
        The ratio of lexical words to tokens in the sentence.
        '''
        nonLexicalTags = argString.split(',')

        lexicalTokensRatio = np.zeros(self.preprocessor.getSentCount())
        i = 0
        for sentence in self.preprocessor.nltkPOStag():
            lexicalCount = 0
            for tagPOS in sentence:
                if tagPOS not in nonLexicalTags:
                    lexicalCount += 1
            if len(sentence) is 0:
                lexicalTokensRatio[i] = 0
            else:
                lexicalTokensRatio[i] = (float(lexicalCount) / len(sentence))
            i += 1

        fileName = "12-" + str(featOrder) + ".npy"
        np.save(fileName, lexicalTokensRatio)
        return fileName
