# -*- coding: utf-8 -*-
"""
Created on Wed Aug 31 12:32:17 2016

@author: admin
"""
from .formatWriter import FormatWriter
        

class Format:

    def __init__(self, fsX, fsy):
        self.X = fsX.tolist()
        self.Y = fsy.tolist()
        
    def libsvmFormat(self, fileName):

        writer = FormatWriter()
        libsvmOutput = []
        for i in range(len(self.Y)):
            output_i = []
            label = self.Y[i]
            output_i.append(label)            
            for j in range(len(self.X[i])):
                output_i.append(str(j+1)+':'+str(self.X[i][j]))
                
            libsvmOutput.append(output_i)
            
        writer.libsvmwriteToFile(libsvmOutput, fileName)
        return libsvmOutput

    def arrfFormat(self, fileName):

        writer = FormatWriter()
        arrfOutput = []
        for i in range(len(self.Y)):
            output_i = []
            label = self.Y[i]
            
            for j in range(len(self.X[i])):
                output_i.append(self.X[i][j])
            output_i.append(label)
                
            arrfOutput.append(output_i)
        writer.arrfwriteToFile(arrfOutput, fileName)
        return arrfOutput

    def outFormat(self, fileName, formatType):
        if formatType == "libsvm":
            self.libsvmFormat(fileName)
        elif formatType == "arrf":
            self.arrfFormat(fileName)
        else:
            self.libsvmFormat(fileName)
            print("Defaulting to libsvm format.")

