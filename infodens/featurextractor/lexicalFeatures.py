# -*- coding: utf-8 -*-
"""
Created on Thu Sep 15 11:16:36 2016

@author: admin
"""
from .featureExtraction import featid, FeatureExtractor
from infodens.preprocessor import preprocess

class LexicalFeatures(FeatureExtractor):
    
    def computeDensity(self,taggedSentences):
        densities = []
        jnrv = ['J', 'N', 'R', 'V'] # nouns, adjectives, adverbs or verbs.

        for sent in taggedSentences:
            jnrvList = [word[0] for word in sent if word[0] in jnrv]
            densities.append(float(len(sent) - len(jnrvList)) / len(sent))
        
        return densities

    @featid(3)        
    def lexicalDensity(self, argString):
        '''
        The frequency of tokens that are not nouns, adjectives, adverbs or verbs. 
        This is computed by dividing the number of tokens tagged with POS tags 
        that do not start with J, N, R or V by the number of tokens in the chunk
        '''
        taggedSents = self.preprocessor.nltkPOStag()

        return self.computeDensity(taggedSents)

    @featid(11)
    def lexicalRichness(self, argString):
        '''
        The ratio of unique tokens in the sentence over the sentence length.
        '''

        #TODO : Lemmatize tokens?
        sentRichness = []
        for sentence in self.preprocessor.gettokenizeSents():
            sentRichness.append(float(len(set(sentence)))/len(sentence))

        return sentRichness

    @featid(12)
    def lexicalToTokens(self, argString):
        '''
        The ratio of lexical words to tokens in the sentence.
        '''

        # TODO : Check if should be argument.
        nonLexicalTags = ['CC', 'DT', 'WDT' 'IN', 'PDT']
        # Coordinating conjunction, Determiner, Wh-determiner ,
        #  Preposition or subordinating conjunction, Predeterminer

        lexicalTokensRatio = []
        for sentence in self.preprocessor.nltkPOStag():
            lexicalCount = 0
            for word in sentence:
                if word[1] not in nonLexicalTags:
                    lexicalCount += 1
            lexicalTokensRatio.append(float(lexicalCount) / len(sentence))

        return lexicalTokensRatio
