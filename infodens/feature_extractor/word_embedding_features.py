from infodens.feature_extractor.feature_extractor import featid, Feature_extractor
import numpy as np
from scipy import sparse


class Word_embedding_features(Feature_extractor):
    
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

            import cv2
            huMoments.append(cv2.HuMoments(cv2.moments(np.asarray(vecImage))).flatten())

        return sparse.lil_matrix(huMoments)
