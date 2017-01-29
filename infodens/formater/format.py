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

    def arffFormat(self, fileName):
        writer = FormatWriter()
        writer.arffwriteToFile(self.X, self.Y, fileName)

    def outFormat(self, fileName, formatType):
        print("Writing features to file.")
        if formatType == "libsvm":
            self.libsvmFormat(fileName)
        elif formatType == "arff":
            self.arffFormat(fileName)
        else:
            self.libsvmFormat(fileName)
            print("Defaulting to libsvm format.")
        print("Feature file written.")


