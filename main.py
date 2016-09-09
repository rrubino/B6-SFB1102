import sys
from infodens.controller.controller import Controller

# TODO: Reformat to use sys arguments for config file.

def infodensRun(configFile):
    # Init a Controller.
    control = Controller(configFile)
    # Load the config file
    status, featIds, featargs, sentencesList = control.loadConfig()
    # MAIN PROCESS (Extract all features)
    if status != 0:
        print(featIds)
        print(featargs)
        print(sentencesList)
        control.manageFeatures()
    else:
        print("Error")
        return 0



infodensRun("testconfig.txt")
