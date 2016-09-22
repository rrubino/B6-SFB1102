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
        control.manageFeatures()
        # Manages a classifier
        control.classifyFeats()
    else:
        print("Error")
        return 0


infodensRun("testconfig.txt")
