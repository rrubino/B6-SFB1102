# -*- coding: utf-8 -*-
"""
Created on Wed Aug 31 12:32:17 2016

@author: admin
"""
import numpy as np

from .formatWriter import FormatWriter
        

class Format:
    
   
    def __init__(self, fsX, fsy):
        self.featureSetX = fsX
        self.featureSety = fsy
        
    def libsvmFormat(self, fileName):
        X, y = self.scikitFormat()
        Xlist = X.tolist()
        ylist = y.tolist()
        writer = FormatWriter()
        libsvmOutput = []
        for i in range(len(ylist)):
            output_i = []
            label = ylist[i]
            output_i.append(label)            
            for j in range(len(Xlist[i])):
                output_i.append(str(j+1)+':'+str(Xlist[i][j]))            
                
            libsvmOutput.append(output_i)
            
        writer.libsvmwriteToFile(libsvmOutput, fileName)
        return libsvmOutput
        

    def arrfFormat(self, fileName):
        X, y = self.scikitFormat()
        Xlist = X.tolist()
        ylist = y.tolist()
        writer = FormatWriter()
        arrfOutput = []
        for i in range(len(ylist)):
            output_i = []
            label = ylist[i]
            
            for j in range(len(Xlist[i])):
                output_i.append(Xlist[i][j])
            output_i.append(label)
                
            arrfOutput.append(output_i)
        writer.arrfwriteToFile(arrfOutput, fileName)
        return arrfOutput

    def scikitFormat(self):
        
        X = np.asarray(self.featureSetX); y = np.asarray(self.featureSety)
        return np.transpose(X), y

    def outFormat(self, data, format):
        #TODO: Format according to format
        return data
        