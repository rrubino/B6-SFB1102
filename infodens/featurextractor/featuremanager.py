import importlib
import imp, os
import sys, inspect
from os import path
from utils import featid, idsOfMethods

# Remove when callExtractors is implemented
from .surfaceFeatures import SurfaceFeatures


class FeatureManager:
    """ Validate the config feature requests,
    And call the necessary feature extractors.
    """

    def __init__(self, featureIDs, featureArgs):
        self.featureIDs = featureIDs
        self.featureArgs = featureArgs

    def checkFeatValidity(self):
        """TODO: Check if features requested are valid. """

        print("Inside checkFeatValidity. ")
        return 1

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
        #surfaceFeats = SurfaceFeatures(self.featureArgs[0])
        # call the needed function
        #print(surfaceFeats.averageWordLength())

        #print("Called features")
        '''
        extract all feature Ids and names
        
        '''
        if __package__ is None:
            sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )
        file, pathname, description = imp.find_module('featurextractor')

        possFeatureClasses = set([os.path.splitext(module)[0] for module in os.listdir(pathname) if module.endswith('.py')])
        
        modules  = []
        featureIds = {}  #All feature Ids
        
        for eachName in possFeatureClasses:
            if eachName.startswith('__'):
                pass
            else:
                modd = __import__('featurextractor.'+eachName)
                modules.append(getattr(modd, eachName))        
        
        for modul in modules:
            clsmembers = inspect.getmembers(modul, inspect.isclass)
            for i in range(len(clsmembers)):        
                featureIds = idsOfMethods(clsmembers[i][1], 'featid', featureIds)
        

        '''
        extract feature Ids and names chosen by user
        
        '''        
        featIDByUser = {} #fid selected by user + names of methods
        for fid in self.featureIDs:
            if fid in featureIds.keys():
                featIDByUser[fid] = featureIds[fid]
        
        
        
        '''
        extract all feature Ids and classes and methods in a dictionary
        
        '''
        idClassmethod = {}
        for fid in self.featureIDs:
            idClassmethod[fid] = []
            
        for modul in modules:
            clsmembers = inspect.getmembers(modul, inspect.isclass)
            for i in range(len(clsmembers)):        
                fIDs = idsOfMethods(clsmembers[i][1], 'featid', {})
                for key in fIDs:
                    if key in self.featureIDs:
                        idClassmethod[key].append(clsmembers[i][1])
                        mtds = inspect.getmembers(clsmembers[i][1], predicate=inspect.ismethod)
                        for method in mtds:
                            if method[0] in featIDByUser.values() and method[0] == featIDByUser[key]:
                                idClassmethod[key].append(method[1])
                            break
        ##dictionary = {id: [class, method]}
                            
                            
        '''
        extract features
        
        '''
        featuresExtracted = []
        for i in range(len(self.featureIDs)):
            mtdCls = idClassmethod[self.featureIDs[i]]
            instance = mtdCls[0](self.featureArgs[i])
            methd = getattr(instance, featureIds[self.featureIDs[i]])
            featuresExtracted.append(methd())
            
        return featuresExtracted
            
        
                                
                    
            
        
                
        