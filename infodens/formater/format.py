# -*- coding: utf-8 -*-
"""
Created on Wed Aug 31 12:32:17 2016

@author: admin
"""
from .formatWriter import FormatWriter
        

class Format:

    def __init__(self, fsX, fsy):
        self.X = fsX
        self.Y = fsy
        
    def libsvmFormat(self, fileName):
        aformater = FormatWriter()
        aformater.libsvmwriteToFile(self.X, self.Y, fileName)

    def arrfFormat(self, fileName):
        writer = FormatWriter()
        writer.arrfwriteToFile(self.X, self.Y, fileName)

    def outFormat(self, fileName, formatType):
        if formatType == "libsvm":
            self.libsvmFormat(fileName)
        elif formatType == "arrf":
            self.arrfFormat(fileName)
        else:
            self.libsvmFormat(fileName)
            print("Defaulting to libsvm format.")

