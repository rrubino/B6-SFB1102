# -*- coding: utf-8 -*-
"""
Created on Thu Sep 15 11:16:36 2016

@author: admin
"""
from .featureExtraction import featid, FeatureExtractor
from infodens.preprocessor import preprocess

class LexicalFeatures(FeatureExtractor):
    
    def computeDensity(self,taggedSentences, jnrv):
        densities = []
        #jnrv = ['J', 'N', 'R', 'V'] # nouns, adjectives, adverbs or verbs.

        for sent in taggedSentences:
            if(len(sent) is 0):
                densities.append(0)
            else:
                jnrvList = [tagPOS for tagPOS in sent if tagPOS in jnrv]
                densities.append(float(len(sent) - len(jnrvList)) / len(sent))
        
        return densities

    @featid(3)        
    def lexicalDensity(self, argString):
        jnrv = argString.split(',')
        '''
        The frequency of tokens that are not nouns, adjectives, adverbs or verbs. 
        This is computed by dividing the number of tokens tagged with POS tags 
        that do not start with J, N, R or V by the number of tokens in the chunk
        '''
        taggedSents = self.preprocessor.nltkPOStag()

        return self.computeDensity(taggedSents, jnrv)

    @featid(11)
    def lexicalRichness(self, argString):
        '''
        The ratio of unique tokens in the sentence over the sentence length.
        '''

        #TODO : Lemmatize tokens?
        sentRichness = []
        for sentence in self.preprocessor.gettokenizeSents():
            if len(sentence) is 0:
                sentRichness.append(0)
            else:
                sentRichness.append(float(len(set(sentence)))/len(sentence))

        return sentRichness

    @featid(12)
    def lexicalToTokens(self, argString):
        '''
        The ratio of lexical words to tokens in the sentence.
        '''
        nonLexicalTags = argString.split(',')

        lexicalTokensRatio = []
        for sentence in self.preprocessor.nltkPOStag():
            lexicalCount = 0
            for tagPOS in sentence:
                if tagPOS not in nonLexicalTags:
                    lexicalCount += 1
            if len(sentence) is 0:
                lexicalTokensRatio.append(0)
            else:
                lexicalTokensRatio.append(float(lexicalCount) / len(sentence))

        return lexicalTokensRatio
