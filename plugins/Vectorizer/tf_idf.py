from .template import Template
from sklearn.feature_extraction.text import TfidfVectorizer
import pickle
import os

class TF_IDF(Template):
    def __init__(self):
        super().__init__()
        self.description = 'Implements the TF-IDF vectorizer'
        self.vectorizer=TfidfVectorizer()

    def train(self, list_of_texts):
        self.vectorizer.fit(list_of_texts)

    def vectorize(self, list_of_texts):
        return self.vectorizer.transform(list_of_texts).todense()

    def save_to_disk(self, target_path):
        with open(target_path+'.pk', 'wb') as vec:
            pickle.dump( self.vectorizer, vec)

    def load_from_disk(self, target_path):
        self.vectorizer=pickle.load(open(target_path+'.pk', 'rb'))

    def exists_on_disk(self, target_path):
        return os.path.exists(target_path+'.pk')