import importlib


# ========================== featuremanager ======================
# This module validates the config file feature requests,
# And calls the necessary feature extractors.
# ================================================================

# ============================call_extractors==============================
# Reads the config file, extracts the featureIDs and their argument strings
# =========================================================================
def checkValid(featureModuleIds, featureIDs):
    print("hello from featman")
    return 1

def call_extractors(featureModuleIds, featureIDs, featargs ):
    #print(featureIDs[0])

    modulePath = 'infodens.featurextractor.' + featureModuleIds[0]
    m =  importlib.import_module(modulePath)
    featToCall = getattr(m,featureIDs[0])
    featToCall(featargs[0])
    print("Called features")
	

