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

    def arrfwriteToFile(self, X, Y, theFile):
        #TODO: Clean up
        dims = X.get_shape()
        thefile = open(theFile, 'w')
        thefile.write('@relation translationese')
        thefile.write('\n')
        thefile.write('\n')
        for i in range(dims[1]):
            thefile.write('@attribute no'+str(i+1)+' real')
            thefile.write('\n')
        thefile.write('\n')
        thefile.write('@data')
        thefile.write('\n')
        for i in range(dims[0]):
            for j in range(dims[1]):
                thefile.write(str(X[i, j])+',')
            thefile.write(str(Y[i]))
            thefile.write('\n')
        thefile.close()



