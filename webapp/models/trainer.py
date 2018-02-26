import numpy as np
import logging


logger = logging.getLogger(__file__)


class Trainer(object):
    """Parent training model using different recipe of methods"""

    def __init__(self, data):
        """Initialize some metadata..."""
        logger.info("Training corpus.")
        self.data = data
        self.size = len(data)

    def make_model(self):
        """Takes a corpus and creates a classification model"""
        pass

    def normalize(self):
        """Normalize data."""
        pass

    def __json__(self):
        """JSON data representation of model."""
        pass

class DemoClass(Trainer):
    """Demo custom trainer class."""

    def demo_function(self):
        x = len(self.data)
        return x

class Regression(Trainer):
    pass

class Word2Vec(Trainer):
    pass

class SupportVectorMachine(Trainer):
    pass

class KNearest(Trainer):
    pass

class TFIDF(Trainer):
    pass
