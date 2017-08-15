from infodens.feature_extractor import feature_manager as featman
from infodens.preprocessor import preprocess
from infodens.preprocessor.preprocess_services import Preprocess_Services
from infodens.classifier import classifier_manager
from infodens.formater import format
from infodens.controller.configurator import Configurator
import os.path


class Controller:
    """Read and parse the config file, init a FeatureManager,
     and init a classifier manager. Handle output. """

    def __init__(self, configFile =None):
        self.config = configFile
        self.configurator = Configurator()

        #array format of dataset and labels for classifying
        self.numSentences = 0
        self.extractedFeats = []
        self.classesList = []

    def loadConfig(self):
        """Read the config file, extract the featureIDs and
        their argument strings.
        """
        statusOK = 0
        # Extract featureID and feature Argument string
        with open(self.config) as config:
            # Parse the config file
            statusOK = self.configurator.parseConfig(config)

            if self.configurator.inputFile is 0 and statusOK:
                print("Error, Input file not found.")
                statusOK = 0

        return statusOK, self.configurator.featureIDs, self.configurator.classifiersList

    def classesSentsMismatch(self, sentsPrep):
        if self.configurator.inputClasses:
            # Extract the classed IDs from the given classes file and Check for
            # Length equality with the sentences.
            prep_serv = Preprocess_Services()
            self.classesList = prep_serv.preprocessClassID(self.configurator.inputClasses)
            sentLen = len(sentsPrep.getPlainSentences())
            classesLen = len(self.classesList)
            self.numSentences = sentLen
            if sentLen != classesLen:
                return True
        return False

    def manageFeatures(self):
        """Init and call a feature manager. """
        preprocessor = preprocess.Preprocess(self.configurator.inputFile, self.configurator.corpusLM,
                                             self.configurator.threadsCount, self.configurator.language,
                                             self.configurator.srilmBinPath, self.configurator.kenlmBinPath)
        if self.classesSentsMismatch(preprocessor):
            print("Classes and Sentences length differ. Quiting. ")
            return 0
        else:
            manageFeatures = featman.Feature_manager(self.numSentences, self.configurator.featureIDs,
                                                     self.configurator.featargs, preprocessor,
                                                     self.configurator.threadsCount)
            validFeats = manageFeatures.checkFeatValidity()
            if validFeats:
                # Continue to call features
                self.extractedFeats = manageFeatures.callExtractors()
                self.scaleFeatures()
                self.outputFeatures()
                return 1
            else:
                # terminate
                print("Requested Feature ID not available.")
                return 0

    def scaleFeatures(self):
        from sklearn import preprocessing as skpreprocess
        scaler = skpreprocess.MaxAbsScaler(copy=False)
        self.extractedFeats = scaler.fit_transform(self.extractedFeats)

    def outputFeatures(self):
        """Output features if requested."""

        if self.configurator.featOutput:
            formatter = format.Format(self.extractedFeats, self.classesList)
            # if format is not set in config, will use a default libsvm output.
            formatter.outFormat(self.configurator.featOutput, self.configurator.featOutFormat)
        else:
            print("Feature output was not specified.")

    def classifyFeats(self):
        """Instantiate a classifier Manager then run it. """

        if self.configurator.inputClasses and self.configurator.classifiersList:
            # Classify if the parameters needed are specified
            classifying = classifier_manager.Classifier_manager(
                          self.configurator.classifiersList, self.extractedFeats, self.classesList,
                            self.configurator.threadsCount, self.configurator.cv_folds)

            validClassifiers = classifying.checkValidClassifier()

            if validClassifiers:
                # Continue to call classifiers
                reportOfClassif = classifying.callClassifiers()
                print(reportOfClassif)
                # Write output if file specified
                if self.configurator.classifReport:
                    with open(self.configurator.classifReport, 'w') as classifOut:
                        classifOut.write(reportOfClassif)
                return 0
            else:
                # terminate
                print("Requested Classifier not available.")
                return -1
        else:
            print("Classifier parameters not specified.")
        return 1

