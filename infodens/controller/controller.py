from ..featurextractor import featuremanager as featman

# ========================== Controller ==========================
# This script reads the config file, calls the feature extractors
# And calls the necessary methods to print/classify the output.
# ================================================================

# ============================loadConfig===================================
# Reads the config file, extracts the featureIDs and their argument strings
# =========================================================================
def loadConfig(config_file):
    config = open(config_file, 'r')

    # Skip header
    header = config.readline()
    featureModuleIDs = []
    featureIDs = []
    featarg = []

    #Extract featureID and feature Argument string
    for line in config:
        line = line.strip()
        params = line.split()
        featureModuleIDs.append(params[0])
        featureIDs.append(params[1])
        featarg.append(params[2])

    config.close()

    return featureModuleIDs, featureIDs, featarg

# ============================callExtractors================================
# Given a list of featureIDs and their arguments, call the feature manager
# Which then checks the validity of the feature strings, and if all is valid
# does the calls to feature extractors.
# ===========================================================================
def callExtractors(featureModIds, featureIDs, featargs):
    valid_feats = featman.checkValid(featureModIds,featureIDs)
    if(valid_feats):
        # Continue to call features
        featman.call_extractors(featureModIds, featureIDs,featargs)
        return 0
    else:
        # terminate
        return -1

