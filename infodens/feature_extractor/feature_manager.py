import importlib
import imp, os
import sys, inspect
from os import path
from joblib import Parallel, delayed
import itertools
from scipy import sparse


def runFeatureMethod(mtdCls, featureID,
                     preprocessor,featureName, featureArgs, preprocessReq=0):
    """ Run the given feature extractor. """
    instance = mtdCls(preprocessor)
    methd = getattr(instance, featureName)
    feat = methd(featureArgs, preprocessReq)
    feateX = "Extracted feature: " + str(featureID) + " - " + str(featureName)
    if not preprocessReq:
        print(feateX)
    return feat

class Feature_manager:
    """ Validate the config feature requests,
    And call the necessary feature extractors.
    """

    def __init__(self, sentCount, featureIDs, featureArgs, preprocessed, threadsCount):
        self.featureIDs = featureIDs
        self.featureArgs = featureArgs
        self.preprocessor = preprocessed
        self.threads = threadsCount
        self.sentCount = sentCount
        '''
        Import the featurextraction package at this point. It will be needed by most of the methods.
        '''
        
        sys.path.append(path.dirname( path.dirname( path.abspath(__file__) ) ) )
        self.fileName, self.pathname, self.description = imp.find_module('feature_extractor')

        self.idClassmethod, self.allFeatureIds = self.idClassDictionary()

    def checkFeatValidity(self):
        ''' Check if requested feature exists. '''
        for featID in self.featureIDs:
            if featID not in self.allFeatureIds:
                print(featID)
                return 0
        return 1

    def methodsWithDecorator(self, cls, decoratorName):
        '''
        find all methods decorated in class cls with decoratorname and has id in idsToSelect
        
        '''
        theMethods = {}
        sourceFile = inspect.getsourcefile(cls)
        f = open(sourceFile, 'r')
        sourcelines = f.readlines()

        for i,line in enumerate(sourcelines):
            line = line.strip()
            if line.split('(')[0].strip() == '@'+decoratorName:
                theId = int(line.split('(')[1].split(')')[0])
                nextLine = sourcelines[i+1]
                name = nextLine.split('def')[1].split('(')[0].strip()
                theMethods[theId] = name

        return theMethods

    def idClassDictionary(self):
        '''
        for every id chosen, find the class that has the method and pair them in a dictionary.
        '''
        possFeatureClasses = set([os.path.splitext(module)[0]
                                  for module in os.listdir(self.pathname) if module.endswith('.py')])
        possFeatureClasses.discard('feature_extractor')
        possFeatureClasses.discard('__init__')
        possFeatureClasses.discard('feature_manager')

        # All feature Ids
        allFeatureIds = {};  featureIds = {};  idClassmethod = {}
        
        for eachName in possFeatureClasses:
            
            modd = __import__('feature_extractor.'+eachName)
            modul = getattr(modd, eachName)
            clsmembers = inspect.getmembers(modul, inspect.isclass)

            if len(clsmembers) > 0:
                clsmembers = [m for m in clsmembers if m[1].__module__.startswith('feature_extractor') and
                             m[0] is not 'Feature_Extractor']
                for i in range(0, len(clsmembers)):
                    featureIds = self.methodsWithDecorator(clsmembers[i][1], 'featid')
                    allFeatureIds.update(featureIds)
                    idClassmethod.update({k: clsmembers[i][1] for k in featureIds.keys()})

        return idClassmethod, allFeatureIds

    def getfeatVectorLen(self, featuresExtracted):

        featsCount = 0
        for i in range(len(self.featureIDs)):
           featsCount += featuresExtracted[i].get_shape()[1]

        return featsCount

    def callExtractors(self):
        '''Extract all feature Ids and names.  '''

        # Gather preprocessor requests first
        for i in range(len(self.featureIDs)):
            runFeatureMethod(self.idClassmethod[self.featureIDs[i]],
                             self.featureIDs[i], self.preprocessor,
                             self.allFeatureIds[self.featureIDs[i]],
                             self.featureArgs[i], preprocessReq=1)

        # Use the minimum of threads and number of requested features
        # Don't allocate unneeded processes
        threadsToUse = len(self.featureIDs) if len(self.featureIDs) < self.threads else self.threads
        featuresExtracted = Parallel(n_jobs=threadsToUse, mmap_mode='r')(delayed(runFeatureMethod)(
                                                        self.idClassmethod[self.featureIDs[i]],
                                                        self.featureIDs[i],
                                                        self.preprocessor,
                                                        self.allFeatureIds[self.featureIDs[i]],
                                                        self.featureArgs[i])
                                                       for i in range(len(self.featureIDs)))

        print("All features extracted. ")

        #Format into scikit format (Each row is a sen)
        output = sparse.hstack(featuresExtracted, "lil")

        featCount = output.get_shape()[1]
        featVec = "Feature vector dimensions: " + str(self.sentCount) + "x" + str(featCount)
        print(featVec)

        print("Ready to Classify. ")

        return output
