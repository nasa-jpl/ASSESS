from .template import Template
from sklearn.feature_extraction.text import TfidfVectorizer
import pickle
import os
from tqdm import  tqdm
from .utilities import  spacy_tokenize_lemmatize_punc_remove
import en_core_web_sm

def identity_func(x):
    return x

class TF_IDF(Template):
    def __init__(self):
        super().__init__()
        self.description = 'Implements the TF-IDF vectorizer'
        self.vectorizer=TfidfVectorizer(tokenizer=identity_func, lowercase=False, max_features=5000)
        self.nlp = en_core_web_sm.load()

    def train(self, list_of_texts):
        print('Preprocessing text for training (tokenize, lemmatize and punctuation removal)..')
        # we add a dummy token 'lemma_lemma' Faiss flat index is giving a higher matching values to vectors for empty strings than some more relevant ones!
        list_of_texts= [spacy_tokenize_lemmatize_punc_remove(item, self.nlp)+['lemma_lemma'] for item in tqdm(list_of_texts)]
        self.vectorizer.fit(list_of_texts)

    def vectorize(self, list_of_texts):
        # we add a dummy token 'lemma_lemma' Faiss flat index is giving a higher matching values to vectors for empty strings than some more relevant ones!
        print('Preprocessing for vectorization (tokenize, lemmatize and punctuation removal)..')
        list_of_texts= [spacy_tokenize_lemmatize_punc_remove(item, self.nlp)+['lemma_lemma'] for item in tqdm(list_of_texts)]
        return self.vectorizer.transform(list_of_texts).todense()

    def save_to_disk(self, target_path):
        with open(target_path+'.pk', 'wb') as vec:
            pickle.dump( self.vectorizer, vec)

    def load_from_disk(self, target_path):
        self.vectorizer=pickle.load(open(target_path+'.pk', 'rb'))

    def exists_on_disk(self, target_path):
        return os.path.exists(target_path+'.pk')