from .featureExtraction import featid, FeatureExtractor
import numpy as np
from scipy import sparse
import scipy.io


class WordEmbedding(FeatureExtractor):
    
    @featid(33)
    def word2vecAverage(self, argString):
        '''Find average word2vec vector of every sentence. '''

        # TODO: Make size an argument
        # Uses language Model from config File
        model = self.preprocessor.trainWord2Vec(100)
        vecAverages = []

        for sentence in self.preprocessor.gettokenizeSents():
            if len(sentence) is 0:
                #Empty sentence, default is zero vector
                vecAverages.append([0]*100)
            else:
                sentVec = []
                for word in sentence:
                    sentVec.append(model[word])
                vecAverages.append(np.mean(sentVec, axis=0))

        return sparse.lil_matrix(vecAverages)
