# -*- coding: utf-8 -*-
"""
Created on Wed Aug 31 12:32:17 2016

@author: admin
"""
import numpy as np

from formatWriter import FormatWriter
        
        
        
class Format:
    
   
    def __init__(self, fsX, fsy):
        self.featureSetX = fsX
        self.featureSety = fsy
        
        
    def libsvmFormat(self, fileName):
        writer = FormatWriter()
        libsvmOutput = []
        for i in range(len(self.featureSety)):
            output_i = []
            label = self.featureSety[i]
            output_i.append(label)
            for j in range(len(self.featureSetX[i])):
                output_i.append(str(j+1)+':'+str(self.featureSetX[i][j]))
            
                
            libsvmOutput.append(output_i)
            
        writer.libsvmwriteToFile(libsvmOutput, fileName)
        return libsvmOutput
        
        
        
    def arrfFormat(self, fileName):
        writer = FormatWriter()
        arrfOutput = []
        for i in range(len(self.featureSety)):
            output_i = []
            label = self.featureSety[i]
            
            for j in range(len(self.featureSetX[i])):
                output_i.append(self.featureSetX[i][j])
            output_i.append(label)
                
            arrfOutput.append(output_i)
        writer.arrfwriteToFile(arrfOutput, fileName)
        
        
        
    def scikitFormat(self):
        
        X = np.asarray(self.featureSetX); y = np.asarray(self.featureSety)
        return np.transpose(X), y
        