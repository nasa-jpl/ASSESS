import numpy as np
import logging


logger = logging.getLogger(__file__)


class Trainer(object):
    """Train model using different recipe of methods"""


    def __init__(self, corpus):
        logger.info("Training corpus.")
        self.corpus = corpus
        self.size = len(corpus)

    def create_classification_model(self):
        """Takes a corpus and creates a classification model"""
        pass

    def normalize_corpus(self):
        pass

