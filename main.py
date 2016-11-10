import sys
from infodens.controller.controller import Controller

# TODO: Reformat to use sys arguments for config file.

def infodensRun(configFile):
    # Init a Controller.
    control = Controller(configFile)
    # Load the config file
    status, featIds, classifiersList = control.loadConfig()
    # MAIN PROCESS (Extract all features)
    if status != 0:
        print("Requested features: ")
        print(featIds)
        if (classifiersList):
            print("Requested classifiers: ")
            print(classifiersList)
        # Manages feature Extraction
        status = control.manageFeatures()
        if status != 0:
            # Manages a classifier
            control.classifyFeats()
        else:
            print("Error in feature Management.")
            return 0

    else:
        print("Error in Config file.")
        return 0

if __name__ == '__main__':
    infodensRun("testconfig.txt")
