import importlib
import imp, os
import sys, inspect
from os import path
from joblib import Parallel, delayed
import itertools
import numpy as np


def runFeatureMethod(mtdCls, featureID,
                     preprocessor,featureName, featureArgs, featOrder):
    """ Run the given feature extractor. """
    instance = mtdCls(preprocessor)
    methd = getattr(instance, featureName)
    feat = methd(featureArgs, featOrder)
    feateX = "Extracted feature: " + str(featureID) + " - " + str(featureName)
    print(feateX)
    return feat


class FeatureManager:
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
        self.fileName, self.pathname, self.description = imp.find_module('featurextractor')

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
        possFeatureClasses.discard('featureExtraction')
        possFeatureClasses.discard('__init__')
        possFeatureClasses.discard('featuremanager')

        # All feature Ids
        allFeatureIds = {};  featureIds = {};  idClassmethod = {}
        
        for eachName in possFeatureClasses:
            
            modd = __import__('featurextractor.'+eachName)
            modul = getattr(modd, eachName)
            clsmembers = inspect.getmembers(modul, inspect.isclass)

            if len(clsmembers) > 0:
                clsmembers = [m for m in clsmembers if m[1].__module__.startswith('featurextractor') and
                             m[0] is not 'FeatureExtractor']
                for i in range(0, len(clsmembers)):
                    featureIds = self.methodsWithDecorator(clsmembers[i][1], 'featid')
                    allFeatureIds.update(featureIds)
                    idClassmethod.update({k: clsmembers[i][1] for k in featureIds.keys()})

        return idClassmethod, allFeatureIds

    def callExtractors(self):
        '''Extract all feature Ids and names.  '''

        #If number of cores is One, resort to iterative call to take advantage of
        # Preprocessor storing operations.

        featuresExtracted = Parallel(n_jobs=self.threads, mmap_mode='r')(delayed(runFeatureMethod)(
                                                        self.idClassmethod[self.featureIDs[i]],
                                                        self.featureIDs[i],
                                                        self.preprocessor,
                                                        self.allFeatureIds[self.featureIDs[i]],
                                                        self.featureArgs[i], i)
                                                       for i in range(len(self.featureIDs)))

        print("All features extracted. ")

        output = []

        #Format into scikit format (Each row is a sentence's feature Vector)

        mmapFeats = []
        for i in range(len(self.featureIDs)):
            mmapFeats.append(np.load(featuresExtracted[i], mmap_mode='r'))

        for j in range(0, self.sentCount):
            sentFeats = []
            for i in range(len(self.featureIDs)):
                featX = mmapFeats[i]
                #if Ngram feature take the whole feature vector
                if 4 <= self.featureIDs[i] <= 7 :
                    sentFeats.extend(featX[j, :])
                else:
                    sentFeats.append(featX[j])
                featX = 0
            output.append(sentFeats)
        mmapFeats = 0

        featVec = "Feature Vector Length: " + str(len(output)) + "x" + str(len(output[0]))
        print(featVec)

        print("Ready to Classify. ")

        for afile in featuresExtracted:
            os.remove(afile)

        return np.asarray(output)
