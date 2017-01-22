# -*- coding: utf-8 -*-
"""
Created on Thu Sep 15 08:39:18 2016

@author: admin
"""

import sklearn

class FormatWriter:
    
    def __init__(self):
        self.className = 'format Writer'

    def libsvmwriteToFile(self, X, Y, theFile):
        sklearn.datasets.dump_svmlight_file(X, Y, theFile)

    def arffwriteToFile(self, X, Y, theFile):
        #TODO: Use liac-arff
        dims = X.get_shape()
        thefile = open(theFile, 'w')
        bufferStr = "@relation translationese\n\n"
        thefile.write(bufferStr)
        for i in range(dims[1]):
            thefile.write('@attribute no'+str(i+1)+' real' + '\n')
        thefile.write('\n'+'@data'+'\n')
        for i in range(dims[0]):
            bufferStr = ""
            for j in range(dims[1]):
                bufferStr += str(X[i, j])+','
            bufferStr += str(Y[i]) + '\n'
            thefile.write(bufferStr)
        thefile.close()



