from .template import Template
import pickle
import os
import numpy as np
from sklearn.neighbors import NearestNeighbors

class Flat(Template):
    def __init__(self):
        super().__init__()
        self.description = 'Implements Scikit learn library based flat index'

    def create_index(self, vectors):
        if type(vectors)==list:
            vectors_=np.array(vectors)
        else:
            # assuming numpy array
            vectors_=vectors
        self.index=NearestNeighbors(n_neighbors=vectors_.shape[1], algorithm="brute", metric="cosine")
        self.index.fit(vectors_)

    def save_to_disk(self, target_path):
        with open(target_path+'.pk', 'wb') as index:
            pickle.dump(self.index, index)

    def load_from_disk(self, target_path):
        self.index=pickle.load(open(target_path+'.pk', 'rb'))

    def exists_on_disk(self, target_path):
        return os.path.exists(target_path+'.pk')

    def get_top_n(self, target_vector, n):
        if type(target_vector)==list:
            vector_=np.array(target_vector)
        else:
            vector_=target_vector
        if len(vector_.shape)==1:
            vector_=np.reshape(vector_, (1, vector_.shape[0]))
        _, top_indicies = self.index.kneighbors(vector_)
        return top_indicies[0]
