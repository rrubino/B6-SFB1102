# -*- coding: utf-8 -*-
"""
Created on Sun Sep 04 14:12:49 2016

@author: admin
"""
from .featureExtraction import featid, FeatureExtractor
from scipy import sparse
import scipy.io
import platform
import subprocess
import os
import codecs


class LangModel(FeatureExtractor):

    def extractValues(self, srilmOutput, i, sentCount):
        tmp = []
        with codecs.open(srilmOutput, encoding='utf-8') as sents:
            for line in sents.readlines():
                if "logprob=" in line:
                    line = str(line).strip().split(" ")
                    if len(tmp) < sentCount:
                        if line[i] != "undefined":
                            tmp.append(float(line[i]))
                        else:
                            tmp.append(0.0)
        return tmp

    @featid(17)
    def langModelFeat(self, argString, preprocessReq=0):
        '''
        Extracts n-gram lemmatized bag of words features.
        '''
        ngramOrder = 3
        if argString:
            ngramOrder = int(argString)

        if preprocessReq:
            # Request all preprocessing functions to be prepared
            self.preprocessor.buildLanguageModel(ngramOrder)
            self.preprocessor.getInputFileName()
            return 1

        sentsFile = self.preprocessor.getInputFileName()
        langModel = self.preprocessor.buildLanguageModel(ngramOrder)

        command = ""
        command += "ngram -order " + str(ngramOrder) + " -lm "
        command += langModel + " -ppl " + sentsFile + " -debug 1 -unk"

        pplFile = "tempLang" + sentsFile + ".ppl"
        if "Linux" in platform.system():
            command += "> " + pplFile
        else:
            command += "> " + pplFile

        subprocess.call(command, shell=True)
        probab = self.extractValues(pplFile, 3, self.preprocessor.getSentCount())
        os.remove(pplFile)

        print(probab[0])

        return sparse.lil_matrix(probab).transpose()

