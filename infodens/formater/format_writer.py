# -*- coding: utf-8 -*-
"""
Created on Thu Sep 15 08:39:18 2016

@author: admin
"""

import sklearn
from scipy import sparse

class Format_writer:
    
    def __init__(self):
        self.className = 'format Writer'

    def libsvmwriteToFile(self, X, Y, theFile):
        sklearn.datasets.dump_svmlight_file(X, Y, theFile, zero_based=False)

    def arffwriteToFile(self, X, Y, theFile):
        #TODO: Fix warning
        import arff

        arffFeatObj = {'description': 'infodens feats', 'relation': 'translationese'}
        dims = X.get_shape()
        attrib = []

        # list of attributes
        for i in range(dims[1]):
            attribTuple = (str(i), "REAL")
            attrib.append(attribTuple)

        arffClasses = list(map(str, set(Y)))
        attrib.append(("y", arffClasses))

        Y = sparse.coo_matrix(Y).transpose()
        data = sparse.hstack([X, Y], "lil")

        arffFeatObj['attributes'] = attrib
        arffFeatObj['data'] = data.tocoo()

        thefile = open(theFile, 'w')
        arff.dump(arffFeatObj, thefile)
        thefile.close()


