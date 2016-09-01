from infodens.controller import controller as ctrl


featModIds, featIds, featargs = ctrl.loadConfig("testconfig.txt")
#print(infodens_loadconfig("testconfig.txt"))

ctrl.callExtractors(featModIds, featIds, featargs)
