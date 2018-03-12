import numpy as np
import logging
from sklearn.naive_bayes import MultinomialNB
from utils import vectorizer_tf_idf

logger = logging.getLogger(__file__)


class Trainer(object):
    """Parent training model using different recipe of methods"""

    def __init__(self, raw_data, vect):
        """Initialize some metadata..."""
        logger.info("Training corpus.")
        self.raw_data = data
        self.size = len(data)
        self.vect = vect

    def make_model(self):
        """Takes a corpus and creates a classification model"""
        pass

    def __json__(self):
        """JSON data representation of model."""
        pass

class DemoClass(Trainer):
    """Demo custom trainer class."""

    def demo_function(self):
        x = len(self.data)
        return x

class LogisticRegression(Trainer):
    pass

class SupportVectorMachine(Trainer):
    pass

class KNearest(Trainer):
    pass

class RandomForest(Trainer):
    pass

class NaiveBayes(Trainer):
    docs_new = ['God is love', 'OpenGL on the GPU is fast']
    X_new_counts = count_vect.transform(docs_new)
    X_new_tfidf = tfidf_transformer.transform(X_new_counts)
    predicted = clf.predict(X_new_tfidf)
    for doc, category in zip(docs_new, predicted):
        print('%r => %s' % (doc, twenty_train.target_names[category]))
