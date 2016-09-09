import sys
from infodens.controller.controller import Controller

# TODO: Reformat to use sys arguments for config file.

def infodensRun(configFile):
    # Init a Controller.
    control = Controller(configFile)
    # Load the config file
    featIds, featargs, sentencesList = control.loadConfig()
    print(featIds)
    print(featargs)
    print(sentencesList)
    # MAIN PROCESS (Extract all features)
    control.manageFeatures()



infodensRun("testconfig.txt")
