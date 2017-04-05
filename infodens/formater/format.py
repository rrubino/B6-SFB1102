# -*- coding: utf-8 -*-
"""
Created on Wed Aug 31 12:32:17 2016

@author: admin
"""
from .format_writer import Format_Writer
        

class Format:

    def __init__(self, fsX, fsy):
        self.X = fsX
        self.Y = fsy
        
    def libsvmFormat(self, fileName):
        aformater = Format_Writer()
        aformater.libsvmwriteToFile(self.X, self.Y, fileName)

    def arffFormat(self, fileName):
        writer = Format_Writer()
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


