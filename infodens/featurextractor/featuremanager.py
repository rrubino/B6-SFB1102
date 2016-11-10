import importlib
import imp, os
import sys, inspect
from os import path
from joblib import Parallel, delayed


def runFeatureMethod(mtdCls,featureID,
                     preprocessor,featureName,featureArgs):
    """ Run the given feature extractor. """
    instance = mtdCls(preprocessor)
    methd = getattr(instance, featureName)
    feat = methd(featureArgs)
    feateX = "Extracted feature: " + str(featureID) + " - " + str(featureName)
    print(feateX)
    return feat

class FeatureManager:
    """ Validate the config feature requests,
    And call the necessary feature extractors.
    """

    def __init__(self, featureIDs, featureArgs, preprocessed, threadsCount):
        self.featureIDs = featureIDs
        self.featureArgs = featureArgs
        self.preprocessor = preprocessed
        self.threads = threadsCount
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

        featuresExtracted = Parallel(n_jobs=self.threads)(delayed(runFeatureMethod)(
                                                        self.idClassmethod[self.featureIDs[i]],
                                                        self.featureIDs[i],
                                                        self.preprocessor,
                                                        self.allFeatureIds[self.featureIDs[i]],
                                                        self.featureArgs[i])
                                                       for i in range(len(self.featureIDs)))

        output = []
        for i in range(0, len(featuresExtracted)):
            if len(featuresExtracted[i]) > 0 and\
                    isinstance(featuresExtracted[i][0], list):
                output.extend(featuresExtracted[i])
            else:
                if len(featuresExtracted[i]) > 0:
                    output.append(featuresExtracted[i])

        print("Called features")
        #print(output)
        return output
