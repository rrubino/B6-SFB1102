import importlib

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
        surfaceFeats = SurfaceFeatures(self.featureArgs[0])
        # call the needed function
        print(surfaceFeats.averageWordLength())

        print("Called features")

