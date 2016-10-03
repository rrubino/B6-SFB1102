import sys
from infodens.controller.controller import Controller

# TODO: Reformat to use sys arguments for config file.

def infodensRun(configFile):
    # Init a Controller.
    control = Controller(configFile)
    # Load the config file
    status, featIds = control.loadConfig()
    # MAIN PROCESS (Extract all features)
    if status != 0:
        print(featIds)
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


infodensRun("testconfig.txt")
