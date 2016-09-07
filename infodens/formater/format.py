# -*- coding: utf-8 -*-
"""
Created on Wed Aug 31 12:32:17 2016

@author: admin
"""
import numpy as np
def libsvmwriteToFile(theList, theFile):
    thefile = open(theFile, 'w')
    
    for item in theList:
        for it in item:
            thefile.write(str(it)+' ')
        thefile.write('\n')
        

def arrfwriteToFile(theList, theFile):
    thefile = open(theFile, 'w')
    thefile.write('@relation translationese')
    thefile.write('\n')
    thefile.write('\n')
    for i in range(len(theList[0])):
        thefile.write('@attribute no'+str(i+1)+' real')
        thefile.write('\n')
    thefile.write('\n')
    thefile.write('@data')
    thefile.write('\n')
    for item in theList:
        counter = 0
        for it in item:
            counter += 1
            if counter == len(item):
                thefile.write(str(it))
            else:
                thefile.write(str(it)+',')
        thefile.write('\n')
        
        
        
        
        
        
class Format:
    
    featureSetX = ''
    featureSety = ''
    
    
    def __init__(self, fsX, fsy):
        self.featureSetX = fsX
        self.featureSety = fsy
        
        
    def libsvmFormat(self, fileName):
        
        libsvmOutput = []
        for i in range(len(self.featureSety)):
            output_i = []
            label = self.featureSety[i]
            output_i.append(label)
            for j in range(len(self.featureSetX[i])):
                output_i.append(str(j+1)+':'+str(self.featureSetX[i][j]))
            
                
            libsvmOutput.append(output_i)
            
        libsvmwriteToFile(libsvmOutput, fileName)
        return libsvmOutput
        
        
        
    def arrfFormat(self, fileName):
        arrfOutput = []
        for i in range(len(self.featureSety)):
            output_i = []
            label = self.featureSety[i]
            
            for j in range(len(self.featureSetX[i])):
                output_i.append(self.featureSetX[i][j])
            output_i.append(label)
                
            arrfOutput.append(output_i)
        arrfwriteToFile(arrfOutput, fileName)
        
    def scikitFormat(self):
        
        X = np.asarray(self.featureSetX); y = np.asarray(self.featureSety)
        return np.transpose(X), y
#        if len(X.shape) ==1:
#            return X.reshape(X.shape[0], 1), y
#        else:
#            return X, y