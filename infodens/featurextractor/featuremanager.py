import importlib
import imp, os
import sys, inspect
from os import path


class FeatureManager:
    """ Validate the config feature requests,
    And call the necessary feature extractors.
    """

    def __init__(self, featureIDs, featureArgs, preprocessed):
        self.featureIDs = featureIDs
        self.featureArgs = featureArgs
        self.preprocessor = preprocessed
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
            if line.split('(')[0].strip() == '@'+decoratorName:
                theId = int(line.split('(')[1].split(')')[0])
                
                #if theId in idsToSelect:
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

        #print(possFeatureClasses)
        # All feature Ids
        allFeatureIds = {};  featureIds = {};  idClassmethod = {}
        
        for eachName in possFeatureClasses:
            
            modd = __import__('featurextractor.'+eachName)
            modul = getattr(modd, eachName)
            clsmembers = inspect.getmembers(modul, inspect.isclass)

            if len(clsmembers) > 0:
                #print ('module name: ', clsmembers[0][1].__module__)
                clsmembers = [m for m in clsmembers if m[1].__module__.startswith('featurextractor') and
                             m[0] is not 'FeatureExtractor']
                for i in range(0, len(clsmembers)):
                    featureIds = self.methodsWithDecorator(clsmembers[i][1], 'featid', self.featureIDs)
                    allFeatureIds.update(featureIds)
                    idClassmethod.update({k:clsmembers[i][1] for k in featureIds.keys()})

        return idClassmethod, allFeatureIds
        
    def callExtractors(self):
        '''Extract all feature Ids and names.  '''

        featuresExtracted = []
        
        for i in range(len(self.featureIDs)):
            mtdCls = self.idClassmethod[self.featureIDs[i]]
            instance = mtdCls(self.preprocessor)
            methd = getattr(instance, self.allFeatureIds[self.featureIDs[i]])
            feat = methd(self.featureArgs[i])
            if type(feat[0]) is list:
                featuresExtracted.extend(feat)
            else:
                featuresExtracted.append(feat)
            feateX = "Extracted feature:" + str(self.featureIDs[i])
            print(feateX)

        print("Called features")
        return featuresExtracted
