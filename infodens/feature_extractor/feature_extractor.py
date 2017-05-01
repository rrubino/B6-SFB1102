# -*- coding: utf-8 -*-
"""
Created on Sun Sep 04 14:42:43 2016

@author: admin
"""
import inspect
from infodens.preprocessor.preprocess_services import Preprocess_Services

def featid(fid):
    def tags_decorator(func):
        def func_wrapper(*args, **kwargs):
            return func(*args, **kwargs)
        return func_wrapper
    return tags_decorator


class Feature_extractor(object):

    def __init__(self, preprocessed):
        '''
        Initializes the class with a preprocessor. '''
        self.preprocessor = preprocessed
        self.prep_servs = Preprocess_Services()

