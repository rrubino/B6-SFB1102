from ..featurextractor import featuremanager as featman
from ..preprocessor import preprocess
from ..classifier import classifierManager
from ..formater import format

class Controller:
    """Read the config file and init a FeatureManager. """

    def __init__(self, configFile =None):
        self.config = configFile
        self.featureIDs = []
        self.featargs = []
        self.listOfSent = []
        self.inputClasses = []
        self.classifiersList = []
        self.inputFile = 0
        self.classifReport = 0
        self.featOutput = 0
        self.featOutFormat = 0
        
        #array format of dataset and labels for classifying
        self.extractedFeats = []
        self.classesList = []

    def parseOutputLine(self, line):
        status = 1
        startInp = line.index(':')
        outputLine = line[startInp + 1:]
        outputLine = outputLine.strip().split()
        if "classif" in line and not self.classifReport:
            self.classifReport = outputLine[0]
        elif "feat" in line and not self.featOutput:
            if len(outputLine) == 2:
                self.featOutput = outputLine[0]
                self.featOutFormat = outputLine[1]
            else:
                status = 0
                print("Incorrect number of output params, should be exactly 2")
        else:
            print("Unsupported output type")
            status = 0

        return status

    def parseConfig(self, configFile):
        """Parse the config file lines.      """
        statusOK = 1

        for configLine in configFile:
            configLine = configLine.strip()
            if not statusOK:
                break
            if len(configLine) < 1:
                # Line is empty
                continue
            elif configLine[0] is '#':
                # Line is comment
                continue
            elif "input" in configLine:
                # Extract input files
                startInp = configLine.index(':')
                configLine = configLine[startInp + 1:]
                configLine = configLine.strip().split()
                self.inputFile = configLine[0]
                self.inputClasses = configLine[1]
                print(self.inputFile)
                print(self.inputClasses)
            elif "output" in configLine:
                statusOK = self.parseOutputLine(configLine)
            elif "classif" in configLine:
                startInp = configLine.index(':')
                configLine = configLine[startInp + 1:]
                configLine = configLine.strip().split()
                self.classifiersList = configLine
                print(self.classifiersList)
            else:
                params = configLine.split()
                if len(params) == 2:
                    if params[0].isdigit():
                        self.featureIDs.append(int(params[0]))
                        self.featargs.append(params[1])
                    else:
                        statusOK = 0
                        print("Feature ID is not a Number")
                else:
                    # Incorrect number/value of params
                    statusOK = 0
                    print("Incorrect number of params, should be exactly 2")

        return statusOK

    def loadConfig(self):
        """Read the config file, extract the featureIDs and
        their argument strings.
        """
        statusOK = 0
        # Extract featureID and feature Argument string
        with open(self.config) as config:
            # Parse the config file
            statusOK = self.parseConfig(config)

            if self.inputFile is 0:
                print("Error, Input file not found.")
                statusOK = 0
            else:
                preprocessor = preprocess.Preprocess()
                self.listOfSent = preprocessor.preprocessBySentence(self.inputFile)

        print(self.featOutFormat)
        print(self.featOutput)
        print(self.classifReport)

        return statusOK, self.featureIDs

    def manageFeatures(self):
        """Init and call a feature manager. """

        manageFeatures = featman.FeatureManager(self.featureIDs, self.featargs, self.listOfSent)
        validFeats = manageFeatures.checkFeatValidity()
        if validFeats:
            # Continue to call features
            self.extractedFeats = manageFeatures.callExtractors()
            return 0
        else:
            # terminate
            print("Requested Feature ID not available.")
            return -1
    
    def formatFeatures(self):
        """Instantiate a Formater then run it. """
        preprocessor = preprocess.Preprocess()
        self.classesList = preprocessor.preprocessClassID(self.inputClasses)
        formatter = format.Format(self.extractedFeats, self.classesList)

        if self.featOutput:
            outFeats = self.extractedFeats
            if self.featOutFormat:
                outFeats = formatter.outFormat(self.extractedFeats, self.featOutFormat)
            with open(self.featOutput, 'w') as featOut:
                featOut.write(str(outFeats))

        self.extractedFeats, self.classesList = formatter.scikitFormat()


    def classifyFeats(self):
        """Instantiate a classifier Manager then run it. """

        if self.inputClasses and self.classifiersList:
            # Classify if the parameters needed are specified
            self.formatFeatures()
            #print(self.y)
            classifying = classifierManager.ClassifierManager(
                          self.classifiersList, self.extractedFeats, self.classesList)
            validClassifiers = classifying.checkValidClassifier()
            if validClassifiers:
                # Continue to call classifiers
                reportOfClassif = classifying.callClassifiers()
                print(reportOfClassif)
                # Write output if file specified
                if self.classifReport:
                    with open(self.classifReport, 'w') as classifOut:
                        classifOut.write(reportOfClassif)
                return 0
            else:
                # terminate
                print("Requested Classifier not available.")
                return -1
        else:
            print("Classifier parameters not specified.")
        return 1

