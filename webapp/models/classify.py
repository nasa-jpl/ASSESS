import numpy as np
import logging


logger = logging.getLogger(__file__)


class Classify(object):
    """Classify  model using the training data."""

    def __init__(self, text):
        self.text = text

    def run_on_model(self):
        """Run classifier against model"""
        logger.info("Classifying text...")
        pass



