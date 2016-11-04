from ..featurextractor import featuremanager as featman
from ..preprocessor import preprocess
from ..classifier import classifierManager
from ..formater import format

class Controller:
    """Read and parse the config file, init a FeatureManager,
     and init a classifier manager. Handle output. """

    def __init__(self, configFile =None):
        self.config = configFile
        self.featureIDs = []
        self.featargs = []
        self.inputClasses = []
        self.classifiersList = []
        self.inputFile = 0
        self.classifReport = 0
        self.corpusLM = 0
        self.featOutput = 0
        self.featOutFormat = 0
        self.threadsCount = 1
        self.language = 'EN'
        
        #array format of dataset and labels for classifying
        self.extractedFeats = []
        self.classesList = []

    def parseOutputLine(self, line):
        status = 1
        startInp = line.index(':')
        outputLine = line[startInp + 1:]
        outputLine = outputLine.strip().split()
        if "classif" in line and not self.classifReport :
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
            elif "model" in configLine:
                startInp = configLine.index(':')
                configLine = configLine[startInp + 1:]
                configLine = configLine.strip().split()
                self.corpusLM = configLine
                print(self.corpusLM)
            elif "lang" in configLine :
                startInp = configLine.index(':')
                configLine = configLine[startInp + 1:]
                configLine = configLine.strip().split()
                self.language = configLine
                print(self.language)
            elif "thread" in configLine:
                startInp = configLine.index(':')
                configLine = configLine[startInp + 1:]
                configLine = configLine.strip().split()
                if configLine[0].isdigit():
                    threads = int(configLine[0])
                    if threads > 0:
                        self.threadsCount = threads
                    else:
                        statusOK = 0
                        print("Number of threads is not a positive integer.")
                    print(self.threadsCount)
                else:
                    statusOK = 0
                    print("Number of threads is not a positive integer.")
            else:
                params = configLine.split()
                if len(params) == 2 or len(params) == 1:
                    if params[0].isdigit():
                        self.featureIDs.append(int(params[0]))
                        if len(params) == 2:
                            self.featargs.append(params[1])
                        else:
                            self.featargs.append([])
                    else:
                        statusOK = 0
                        print("Feature ID is not a Number")
                else:
                    # Incorrect number/value of params
                    statusOK = 0
                    print("Incorrect number of params, max 2 parameters.")

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

            if self.inputFile is 0 and statusOK:
                print("Error, Input file not found.")
                statusOK = 0

        return statusOK, self.featureIDs

    def classesSentsMismatch(self,sentsPrep):
        if self.inputClasses:
            # Extract the classed IDs from the given classes file
            preprocessor = preprocess.Preprocess(self.inputClasses)
            self.classesList = preprocessor.preprocessClassID()
            sentLen = len(sentsPrep.getPlainSentences())
            classesLen = len(self.classesList)
            if (sentLen != classesLen):
                return True
        return False

    def manageFeatures(self):
        """Init and call a feature manager. """
        preprocessor = preprocess.Preprocess(self.inputFile,self.corpusLM,
                                             self.language)
        if self.classesSentsMismatch(preprocessor):
            print("Classes and Sentences length differ. Quiting. ")
            return 0
        else:
            manageFeatures = featman.FeatureManager(self.featureIDs, self.featargs, preprocessor)
            validFeats = manageFeatures.checkFeatValidity()
            if validFeats:
                # Continue to call features
                # preprocessor.buildLanguageModel()
                self.extractedFeats = manageFeatures.callExtractors()
                self.outputFeatures()
                return 1
            else:
                # terminate
                print("Requested Feature ID not available.")
                return 0

    def outputFeatures(self):
        """Output features if requested."""

        #TODO : cleaner Format class with only needed init.
        formatter = format.Format(self.extractedFeats, self.classesList)
        if self.featOutput:
            outFeats = self.extractedFeats
            # Check if a format is requested then format with it
            if self.featOutFormat:
                outFeats = formatter.outFormat(self.extractedFeats, self.featOutFormat)
            with open(self.featOutput, 'w') as featOut:
                #TODO : write as binary
                featOut.write(str(outFeats))
        else:
            print("Feature output was not specified.")

    def formatFeatures(self):
        """Instantiate a Formater then run it. """

        formatter = format.Format(self.extractedFeats, self.classesList)

        self.extractedFeats, self.classesList = formatter.scikitFormat()


    def classifyFeats(self):
        """Instantiate a classifier Manager then run it. """

        if self.inputClasses and self.classifiersList:
            # Classify if the parameters needed are specified
            self.formatFeatures()
            #print(self.y)
            classifying = classifierManager.ClassifierManager(
                          self.classifiersList, self.extractedFeats, self.classesList, self.threadsCount)
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

