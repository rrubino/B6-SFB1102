# -*- coding: utf-8 -*-
"""
Created on Sun Sep 04 14:12:49 2016

@author: admin
"""
from .feature_extractor import featid, Feature_extractor
from scipy import sparse
import scipy.io
import numpy as np
import subprocess
import os
import codecs


class Lang_model_features(Feature_extractor):

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
        Extracts n-gram Language Model preplexity features.
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
                langModel = self.preprocessor.buildLanguageModel(ngramOrder)
            self.preprocessor.getInputFileName()
            self.preprocessor.getBinariesPath()
            return 1

        sentsFile = self.preprocessor.getInputFileName()
        srilmBinary = self.preprocessor.getBinariesPath()

        if not langModel:
            langModel = self.preprocessor.buildLanguageModel(ngramOrder)

        pplFile = "tempLang{0}{1}.ppl".format(sentsFile, ngramOrder)
        command = "\"{0}ngram\" -order {1} -lm {2} -ppl {3} -debug 1 -unk> {4}".format(srilmBinary, ngramOrder,
                                                                                     langModel, sentsFile, pplFile)

        #print(command)

        subprocess.call(command, shell=True)
        probab = self.extractValues(pplFile, self.preprocessor.getSentCount())
        os.remove(pplFile)

        #print(probab[0])

        return sparse.lil_matrix(probab)


    @featid(18)
    def langModelPOSFeat(self, argString, preprocessReq=0):
        '''
        Extracts n-gram POS language model preplexity features.
        '''
        ngramOrder = 3
        langModel = ""
        taggedInput = ""
        taggedCorpus = ""
        # TaggedInput1/0,LM0/1,taggedCorpus0/1,ngramOrder(,TaggedPOSfile(ifTaggedInp1),
        # LMFilePath(ifLM1),taggedCorpus(if LM0&TaggedCorpus1))
        arguments = argString.split(',')
        if int(arguments[0]):
            # Use file of tagged sents (last argument)
            taggedInput = "\"{0}\"".format(arguments[4])
        if int(arguments[1]):
            # Next argument
            langModel = "\"{0}\"".format(arguments[4+int(arguments[0])])
        elif int(arguments[2]):
            taggedCorpus = "\"{0}\"".format(arguments[4+int(arguments[0])])

        ngramOrder = int(arguments[3])

        if preprocessReq:
            # Request all preprocessing functions to be prepared
            if not taggedInput:
                taggedInput = self.prep_servs.dumpTokensTofile(dumpFile="taggedInput18.txt",
                                                 tokenSents=self.preprocessor.getPOStagged())
            if not langModel:
                if not taggedCorpus:
                    taggedCorpus = self.prep_servs.dumpTokensTofile(dumpFile="taggedCorpus18.txt",
                                                     tokenSents=self.prep_servs.tagPOSfromFile(
                                                         self.preprocessor.getCorpusLMName()
                                                     ))

                # If tagged corpus is empty, just use
                langModel = self.preprocessor.buildLanguageModel(ngramOrder, taggedCorpus, False)

            outFile = open("tempfiles18.txt", 'w')
            outFile.write(taggedInput+"\n")
            outFile.write(taggedCorpus+"\n")
            outFile.write(langModel)
            outFile.close()

            return 1

        # Retrieve preprocessing results
        with codecs.open("tempfiles18.txt", mode="r") as f:
            lines = f.readlines()
        taggedInput = lines[0].strip()
        langModel = lines[2].strip()

        os.remove("tempfiles18.txt")

        srilmBinary = self.preprocessor.getBinariesPath()

        #pplFile = "tempLang{0}{1}.ppl".format(taggedInput, ngramOrder)
        pplFile = "tempLang{0}{1}.ppl".format("input18", ngramOrder)

        command = "\"{0}ngram\" -order {1} -lm {2} -ppl {3} -debug 1 -unk> {4}".format(srilmBinary, ngramOrder,
                                                                                       langModel, taggedInput, pplFile)

        #print(command)

        subprocess.call(command, shell=True)
        probab = self.extractValues(pplFile, self.preprocessor.getSentCount())
        os.remove(pplFile)

        #for tempFile in lines:
        #    os.remove(tempFile.strip())


        # print(probab[0])

        return sparse.lil_matrix(probab)

