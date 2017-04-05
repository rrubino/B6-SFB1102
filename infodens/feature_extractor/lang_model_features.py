# -*- coding: utf-8 -*-
"""
Created on Sun Sep 04 14:12:49 2016

@author: admin
"""
from .feature_extractor import featid, Feature_Extractor
from scipy import sparse
import scipy.io
import numpy as np
import platform
import subprocess
import os
import codecs


class LangModel_Features(Feature_Extractor):

    def extractValues(self, srilmOutput, sentCount):
        feats = []
        with codecs.open(srilmOutput, encoding='utf-8') as sents:
            for line in sents:
                if "logprob=" in line:
                    line = str(line).strip().split(" ")
                    if len(feats) < sentCount:
                        tmp = []
                        for i in [3, 5, 7]:
                            if line[i] != "undefined":
                                tmp.append(np.float32(line[i]))
                            else:
                                tmp.append(np.float32(0.0))
                        feats.append(tmp)
        return feats

    @featid(17)
    def langModelFeat(self, argString, preprocessReq=0):
        '''
        Extracts n-gram lemmatized bag of words features.
        '''
        ngramOrder = 3
        langModel = 0
        # Binary1/0,ngramOrder,LMFilePath(ifBinary1)
        arguments = argString.split(',')
        if(int(arguments[0])):
            # Use file of tagged sents (last argument)
            langModel = "\"{0}\"".format(arguments[-1])

        ngramOrder = int(arguments[1])
        if preprocessReq:
            # Request all preprocessing functions to be prepared
            if not langModel:
                self.preprocessor.buildLanguageModel(ngramOrder)
            self.preprocessor.getInputFileName()
            self.preprocessor.getBinariesPath()
            return 1

        sentsFile = self.preprocessor.getInputFileName()
        srilmBinary = self.preprocessor.getBinariesPath()

        if not langModel:
            langModel = self.preprocessor.buildLanguageModel(ngramOrder)

        pplFile = "tempLang{0}{1}.ppl".format(sentsFile, ngramOrder)
        command = "\"{0}\\ngram\" -order {1} -lm {2} -ppl {3} -debug 1 -unk> {4}".format(srilmBinary, ngramOrder,
                                                                                     langModel, sentsFile, pplFile)

        subprocess.call(command, shell=True)
        probab = self.extractValues(pplFile, self.preprocessor.getSentCount())
        os.remove(pplFile)

        #print(probab[0])

        return sparse.lil_matrix(probab)

