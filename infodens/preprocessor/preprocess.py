# -*- coding: utf-8 -*-
"""
Created on Tue Aug 30 15:19:12 2016

@author: admin
"""
import codecs
class Preprocess:
    
    fileName = ''
    
    def __init__(self, fn):
        self.fileName = fn

    def preprocessBySentence(self):
        with codecs.open(self.fileName, encoding='utf-8') as f:
            lines = f.read().splitlines()
            
        return lines

    def preprocessClassID(self):
        """ Extract from each line the integer for class ID."""
        
        with codecs.open(self.fileName, encoding='utf-8') as f:
            lines = f.read().splitlines()
        ids = [int(id) for id in lines]
        
        return ids
        
        
    def preprocessByBlock(self, blockSize):
        pass