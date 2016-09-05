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
        f.write(key)
        f.write(' ')
        f.write(theDict[key])
        
        f.write('\n')
        
def readFileToDictionary(theFile):
    f = open(theFile, 'r')
    fileContents = f.readlines()
    theDict = {}
    for content in fileContents:
        
        theDict[int(content.strip().split()[0])] = content.strip().split()[1]
    return theDict
