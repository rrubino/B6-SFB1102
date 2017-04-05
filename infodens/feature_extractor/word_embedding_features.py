from .feature_extractor import featid, Feature_Extractor
import numpy as np
from scipy import sparse
import scipy.io
from sklearn.preprocessing import scale as skScale
import cv2


class Word_Embedding_Features(Feature_Extractor):
    
    @featid(33)
    def word2vecAverage(self, argString, preprocessReq=0):
        '''Find average word2vec vector of every sentence. '''

        if len(argString) > 0:
            vecSize = int(argString)
        else:
            #default
            vecSize = 100

        if preprocessReq:
            # Request all preprocessing functions to be prepared
            self.preprocessor.getWord2vecModel(vecSize)
            self.preprocessor.gettokenizeSents()
            return 1

        if len(argString) > 0:
            vecSize = int(argString)
        else:
            #default
            vecSize = 100

        # Uses language Model from config File
        model = self.preprocessor.getWord2vecModel(vecSize)
        vecAverages = []

        for sentence in self.preprocessor.gettokenizeSents():
            if len(sentence) is 0:
                #Empty sentence, default is zero vector
                vecAverages.append([0]*100)
            else:
                sentVec = []
                for word in sentence:
                    # TODO: Handle OOV
                    sentVec.append(model[word])
                vecAverages.append(np.mean(sentVec, axis=0))

        return sparse.lil_matrix(vecAverages)


    @featid(34)
    def word2vecMoments(self, argString, preprocessReq=0):
        '''Find average word2vec vector of every sentence. '''

        if len(argString) > 0:
            vecSize = int(argString)
        else:
            #default
            vecSize = 100

        if preprocessReq:
            # Request all preprocessing functions to be prepared
            self.preprocessor.getWord2vecModel(vecSize)
            self.preprocessor.gettokenizeSents()
            return 1

        # Uses language Model from config File
        model = self.preprocessor.getWord2vecModel(vecSize)
        huMoments = []

        for sentence in self.preprocessor.gettokenizeSents():
            vecImage = []
            for word in sentence:
                vecImage.append(model[word])

            huMoments.append(cv2.HuMoments(cv2.moments(np.asarray(vecImage))).flatten())

        return sparse.lil_matrix(huMoments)
