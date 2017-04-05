from ..featurextractor import featureManager as featman
from ..preprocessor import preprocess
from ..classifier import classifierManager
from ..formater import format
from sklearn import preprocessing as skpreprocess
import multiprocessing
import numpy as np
import os.path

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
        self.threadsCount = multiprocessing.cpu_count()
        self.language = 'EN'
        self.numSentences = 0
        self.srilmBinPath = 0
        self.cv_folds = 1
        
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
            elif len(outputLine) == 1:
                self.featOutput = outputLine[0]
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
            elif "input files" in configLine:
                # Extract input files
                startInp = configLine.index(':')
                configLine = configLine[startInp + 1:]
                configLine = configLine.strip().split()
                self.inputFile = configLine[0]
                self.inputClasses = configLine[1]
                print("Input File: ")
                print(self.inputFile)
            elif "output" in configLine:
                statusOK = self.parseOutputLine(configLine)
            elif "classif" in configLine:
                startInp = configLine.index(':')
                configLine = configLine[startInp + 1:]
                configLine = configLine.strip().split()
                self.classifiersList = configLine
            elif "model" in configLine:
                startInp = configLine.index(':')
                configLine = configLine[startInp + 1:]
                configLine = configLine.strip().split()
                self.corpusLM = configLine[0]
            elif "SRILM" in configLine or "srilm" in configLine:
                startInp = configLine.index(':')
                configLine = configLine[startInp + 1:]
                configLine = configLine.strip()
                self.srilmBinPath = configLine
                if not os.path.isdir(self.srilmBinPath):
                    statusOK = 0
                    print("Invalid SRILM binaries path.")
            elif "operating language" in configLine:
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
                        #handle single thread case
                        self.threadsCount = threads if threads < 3 else threads-1
                    else:
                        statusOK = 0
                        print("Number of threads is not a positive integer.")
                    #print(self.threadsCount)
                else:
                    statusOK = 0
                    print("Number of threads is not a positive integer.")
            elif "fold" in configLine:
                startInp = configLine.index(':')
                configLine = configLine[startInp + 1:]
                configLine = configLine.strip().split()
                if configLine[0].isdigit():
                    folds = int(configLine[0])
                    if folds > 0:
                        self.cv_folds = folds

                    else:
                        statusOK = 0
                        print("Number of folds is not a positive integer.")
                else:
                    statusOK = 0
                    print("Number of folds is not a positive integer.")
            else:
                params = str(configLine).split(' ', 1)
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

        return statusOK, self.featureIDs, self.classifiersList

    def classesSentsMismatch(self, sentsPrep):
        if self.inputClasses:
            # Extract the classed IDs from the given classes file and Check for
            # Length equality with the sentences.
            preprocessor = preprocess.Preprocess(self.inputClasses)
            self.classesList = preprocessor.preprocessClassID()
            sentLen = len(sentsPrep.getPlainSentences())
            classesLen = len(self.classesList)
            self.numSentences = sentLen
            if (sentLen != classesLen):
                return True
        return False

    def manageFeatures(self):
        """Init and call a feature manager. """
        preprocessor = preprocess.Preprocess(self.inputFile, self.corpusLM,
                                             self.threadsCount, self.language, self.srilmBinPath)
        if self.classesSentsMismatch(preprocessor):
            print("Classes and Sentences length differ. Quiting. ")
            return 0
        else:
            manageFeatures = featman.FeatureManager(self.numSentences, self.featureIDs, self.featargs,
                                                    preprocessor, self.threadsCount)
            validFeats = manageFeatures.checkFeatValidity()
            if validFeats:
                # Continue to call features
                self.extractedFeats = manageFeatures.callExtractors()
                self.outputFeatures()
                self.scaleFeatures()
                return 1
            else:
                # terminate
                print("Requested Feature ID not available.")
                return 0

    def scaleFeatures(self):
        scaler = skpreprocess.MaxAbsScaler(copy=False)
        self.extractedFeats = scaler.fit_transform(self.extractedFeats)

    def outputFeatures(self):
        """Output features if requested."""

        if self.featOutput:
            formatter = format.Format(self.extractedFeats, self.classesList)
            # if format is not set in config, will use a default libsvm output.
            formatter.outFormat(self.featOutput, self.featOutFormat)
        else:
            print("Feature output was not specified.")

    def classifyFeats(self):
        """Instantiate a classifier Manager then run it. """

        if self.inputClasses and self.classifiersList:
            # Classify if the parameters needed are specified
            classifying = classifierManager.ClassifierManager(
                          self.classifiersList, self.extractedFeats, self.classesList, self.threadsCount,
                            self.cv_folds)

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

