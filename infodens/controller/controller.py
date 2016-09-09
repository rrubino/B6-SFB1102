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
        statusOK = 1
        inputFile = 0

        # First line is input file
        # TODO: Change to search and find input file
        # inputFile = config.readline()
        # inputFile = inputFile.strip()
        #preprocessor = preprocess.Preprocess(inputFile)
        #self.listOfSent = preprocessor.preprocessBySentence()


        # Extract featureID and feature Argument string
        for line in config:
            line = line.strip()
            if len(line) < 1:
                #Line is empty
                continue
            elif line[0] is '#':
                #Line is comment
                continue
            elif "input" in line:
                startInp = line.index(':')
                line =  line[startInp+1:]
                inputFile = line.strip()
                #print(inputFile)
            else:
                params = line.split()
                if len(params) == 2:
                    if params[0].isdigit():
                        self.featureIDs.append(params[0])
                        self.featargs.append(params[1])
                    else:
                        statusOK = 0
                        print("Feature ID is not a Number")
                else:
                    # Incorrect number/value of params
                    statusOK = 0
                    print("Incorrect number of params, should be only 2")

        if inputFile is 0:
            print("Error, Input file not found. ")
            statusOK = 0
        else:
            preprocessor = preprocess.Preprocess(inputFile)
            self.listOfSent = preprocessor.preprocessBySentence()

        config.close()

        return statusOK, self.featureIDs, self.featargs, self.listOfSent

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

