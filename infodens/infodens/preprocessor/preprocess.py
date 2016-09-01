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
        f = open(self.fileName)
        lines = f.readlines()
        
        return lines
        
        
    def preprocessByBlock(self, blockSize):
        pass