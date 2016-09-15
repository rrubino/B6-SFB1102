import importlib
import imp, os
import sys, inspect
from os import path
from .utils import featid, idsOfMethods

# Remove when callExtractors is implemented
#from .surfaceFeatures import SurfaceFeatures


class FeatureManager:
    """ Validate the config feature requests,
    And call the necessary feature extractors.
    """

    def __init__(self, featureIDs, featureArgs, listOfSentences):
        self.featureIDs = featureIDs
        self.featureArgs = featureArgs
        self.lofs = listOfSentences
        '''
		Import the featurextraction package at this point. It will be needed by most of the methods.
        '''
        
        sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )
        self.fileName, self.pathname, self.description = imp.find_module('featurextractor')

    def checkFeatValidity(self):
        """TODO: Check if features requested are valid. """

        print("Inside checkFeatValidity. ")
        return 1


    def methodsWithDecorator(self, cls, decoratorName, idsToSelect):
        '''
        find all methods decorated in class cls with decoratorname and has id in idsToSelect
        
        '''
        theMethods = {}
        sourceFile = inspect.getsourcefile(cls)
        f = open(sourceFile, 'r')
        sourcelines = f.readlines()
        
        for i,line in enumerate(sourcelines):
            
            line = line.strip()
            if line.split('(')[0].strip() == '@'+decoratorName: # leaving a bit out
                theId = int(line.split('(')[1].split(')')[0])
                
                if theId in idsToSelect:
                    nextLine = sourcelines[i+1]
                    name = nextLine.split('def')[1].split('(')[0].strip()
                    
                    theMethods[theId] = name
                
        return theMethods
    
    def allMethodsWithDecorator(cls, decoratorName):
        '''
        find all methods decorated in class cls with decoratorname unconditionally
        
        '''
        theMethods = {}
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
        
    def idClassDictionary(self):
        '''
        for every id chosen, find the class that has the method and pair them in a dictionary.
        '''
        possFeatureClasses = set([os.path.splitext(module)[0] for module in os.listdir(self.pathname) if module.endswith('.py')])
        
        
        allFeatureIds = {};  featureIds = {};  idClassmethod = {}#All feature Ids        
        
        for eachName in possFeatureClasses:
            modd = __import__('featurextractor.'+eachName)
            modul = getattr(modd, eachName)
            clsmembers = inspect.getmembers(modul, inspect.isclass)
            if len(clsmembers) > 0:                
                featureIds = self.methodsWithDecorator(clsmembers[0][1], 'featid', self.featureIDs)                
                allFeatureIds.update(featureIds)
                idClassmethod.update({k:clsmembers[0][1] for k in featureIds.keys()})
                
        return idClassmethod, allFeatureIds
        
    def callExtractors(self):
        """TODO : Import and call feature extractors. """

        # Use the below code to do dynamic calls by feature Strings
        # Given the featureID to feature function string mapping.

        #modulePath = 'infodens.featurextractor.' + featureModuleIds[0]
        #modulePath = "infodens.featurextractor."+featureModuleIds[0]
        #m =  importlib.import_module(modulePath)
        #featToCall = getattr(m,featureIDs[0])
        #featToCall(featargs[0])

        #Testing feature and example.
        # Init the class with the corresponding argument
        #print (self.featureIDs)
        #print (self.featureArgs)
        #surfaceFeats = SurfaceFeatures(self.lofs,self.featureArgs[0])
        # call the needed function
        #print(surfaceFeats.averageWordLength())
        #print(surfaceFeats.syllableRatio())

        print("Called features")
        '''
        extract all feature Ids and names
        
        '''
        '''
        extract all feature Ids and names
        
        '''
        

        idClassmethod, allFeatureIds = self.idClassDictionary()
                
        
        featuresExtracted = []
        
        for i in range(len(self.featureIDs)):
            mtdCls = idClassmethod[self.featureIDs[i]]
            instance = mtdCls(self.lofs, self.featureArgs[i])
            methd = getattr(instance, allFeatureIds[self.featureIDs[i]])
            featuresExtracted.append(methd())
        print (featuresExtracted)    
        return featuresExtracted
            
        
                                
                    
            
        
                
        