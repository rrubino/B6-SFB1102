import sys
from infodens.controller.controller import Controller

# TODO: Reformat to use sys arguments for config file.

def infodensRun(configFile):
    # Init a Controller.
    control = Controller(configFile)
    # Load the config file
    featIds, featargs = control.loadConfig()
    print(featIds)
    print(featargs)
    # MAIN PROCESS (Extract all features)
    control.manageFeatures()



infodensRun("testconfig.txt")
