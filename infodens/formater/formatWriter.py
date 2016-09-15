# -*- coding: utf-8 -*-
"""
Created on Thu Sep 15 08:39:18 2016

@author: admin
"""

class FormatWriter:
    
    def __init__(self):
        self.className = 'format Writer'
        
        
    def libsvmwriteToFile(self, theList, theFile):
        thefile = open(theFile, 'w')
        
        for item in theList:
            for it in item:
                thefile.write(str(it)+' ')
            thefile.write('\n')
        

    def arrfwriteToFile(self, theList, theFile):
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