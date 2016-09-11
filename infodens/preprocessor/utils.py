# -*- coding: utf-8 -*-
"""
Created on Sun Sep 04 14:42:43 2016

@author: admin
"""
import inspect

def featid(fid):
    def tags_decorator(func):
        def func_wrapper(*args, **kwargs):
            return func(*args, **kwargs)
        return func_wrapper
    return tags_decorator
    
    
    
def methodWithDecorator(cls, decoratorName):
    sourcelines = inspect.getsourcelines(cls)[0]
    for i,line in enumerate(sourcelines):
        line = line.strip()
        if line.split('(')[0].strip() == '@'+decoratorName: # leaving a bit out
            nextLine = sourcelines[i+1]
            name = nextLine.split('def')[1].split('(')[0].strip()
            yield(name)
            
            
            
def idsOfMethods(cls, decoratorName, theMethods):
    
    sourceFile = inspect.getsourcefile(cls)
    f = open(sourceFile, 'r')
    sourcelines = f.readlines()
    
    for i,line in enumerate(sourcelines):
        
        line = line.strip()
        if line.split('(')[0].strip() == '@'+decoratorName: # leaving a bit out
            theId = int(line.split('(')[1].split(')')[0])
            nextLine = sourcelines[i+1]
            name = nextLine.split('def')[1].split('(')[0].strip()
            
            theMethods[theId] = name
            
    return theMethods
            
def methodsWithDecorator(cls, decoratorName):
    #sourcelines = inspect.getsourcelines(cls)[0]
    sourceFile = inspect.getsourcefile(cls)
    f = open(sourceFile, 'r')
    sourcelines = f.readlines()
    theMethods = []
    for i,line in enumerate(sourcelines):
        
        line = line.strip()
        if line.split('(')[0].strip() == '@'+decoratorName: # leaving a bit out
            nextLine = sourcelines[i+1]
            name = nextLine.split('def')[1].split('(')[0].strip()
            
            theMethods.append(name)
            
    return theMethods
            
def writeDictionaryToFile(theDict, theFile):
    f = open(theFile, 'w')
    for key in theDict:
        
        f.write(str(key) + ' ' + theDict[key] + '\n')
        
def readFileToDictionary(theFile):
    f = open(theFile, 'r')
    fileContents = f.readlines()
    theDict = {}
    for content in fileContents:
        
        theDict[int(content.strip().split()[0])] = content.strip().split()[1]
    return theDict



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