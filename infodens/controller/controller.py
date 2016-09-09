from ..featurextractor import featuremanager as featman
from ..preprocessor import preprocess


class Controller:
    """Read the config file and init a FeatureManager. """

    def __init__(self, configFile =None):
        self.config = configFile
        self.featureIDs = []
        self.featargs = []
        self.listOfSent = []

    def loadConfig(self):
        """Read the config file, extract the featureIDs and
        their argument strings.
        """
        config = open(self.config, 'r')

        # First line is input file
        # TODO: Change to search and find input file
        inputFile = config.readline()
        inputFile = inputFile.strip()
        preprocessor = preprocess.Preprocess(inputFile)
        self.listOfSent = preprocessor.preprocessBySentence()


        # Extract featureID and feature Argument string
        for line in config:
            line = line.strip()
            if line[0] is '#':
                continue
            else:
                params = line.split()
                self.featureIDs.append(params[0])
                self.featargs.append(params[1])

        config.close()

        return self.featureIDs, self.featargs, self.listOfSent

    def manageFeatures(self):
        """Init and call a feature manager. """

        manageFeatures = featman.FeatureManager(self.featureIDs, self.featargs, self.listOfSent)
        validFeats = manageFeatures.checkFeatValidity()
        if validFeats:
            # Continue to call features
            manageFeatures.callExtractors()
            return 0
        else:
            # terminate
            print("Error in Config File, Please reformat. ")
            return -1

