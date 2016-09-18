# -*- coding: utf-8 -*-
"""
Created on Thu Sep 15 11:16:36 2016

@author: admin
"""
import nltk
from .utils import featid

class LexicalFeatures:
    
    def __init__(self, lof):
        self.lof = lof
    
    def computeDensity(self, taggedSentence):
        #jnrv = ['J', 'N', 'R', 'V'] # nouns, adjectives, adverbs or verbs. 
        
        jnrv = [word[1] for word in taggedSentence if word[1].startswith('J') or word[1].startswith('N') or word[1].startswith('R') or word[1].startswith('V')]
        
        return float(len(taggedSentence) - len(jnrv)) / len(taggedSentence)

    @featid(3)        
    def lexicalDensity(self, argString):
        '''
        The frequency of tokens that are not nouns, adjectives, adverbs or verbs. 
        This is computed by dividing the number of tokens tagged with POS tags 
        that do not open with J, N, R or V by the number of tokens in the chunk
        '''
        
        taggedSents = [nltk.pos_tag(self.lof[i]) for i in range(len(self.lof))]
        density = [self.computeDensity(sentence) for sentence in taggedSents]
        return density
        
        