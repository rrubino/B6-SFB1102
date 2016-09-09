# -*- coding: utf-8 -*-
"""
Created on Tue Aug 30 15:19:12 2016

@author: admin
"""

class Preprocess:
    
    fileName = ''
    
    def __init__(self, fn):
        self.fileName = fn
        
        
    def preprocessBySentence(self):
        with open(self.fileName) as f:
            lines = f.read().splitlines()
        
        return lines
        
        
    def preprocessByBlock(self, blockSize):
        pass