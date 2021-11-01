from .template import Template
import pickle
import os
import numpy as np

class Basic(Template):
    def __init__(self):
        super().__init__()
        self.description = 'for storing Dense Vectors'
        if self._exists_on_disk():
            self._load_from_disk()
        else:
            self.sorted_ids = {}
            self.vector_storage = {}


    def _add_update_vector(self, id, vector, vec_type):
        if vec_type not in self.vector_storage.keys():
            self.vector_storage[vec_type]={}
        self.vector_storage[vec_type][id] = vector
        if vec_type not in self.sorted_ids.keys():
            self.sorted_ids[vec_type]=[]
        if id not in self.sorted_ids[vec_type]:
            self.sorted_ids[vec_type].append(id)

    def _remove_vector(self, id, vec_type):
        self.vector_storage[vec_type].pop(id)
        self.sorted_ids[vec_type].remove(id)

    def _save_to_disk(self):
        with open('basic_vector_storage.pk', 'wb') as storage:
            pickle.dump(self.vector_storage, storage)
        with open('basic_sorted_ids.pk', 'wb') as ids:
            pickle.dump(self.sorted_ids, ids)

    def _load_from_disk(self):
        self.vector_storage = pickle.load(open('basic_vector_storage.pk', 'rb'))
        self.sorted_ids = pickle.load(open('basic_sorted_ids.pk', 'rb'))

    def _exists_on_disk(self):
        if os.path.exists('basic_vector_storage.pk') and os.path.exists(
                'basic_sorted_ids.pk'):
            return True
        return False

    def clean_storage(self):
        self.sorted_ids = {}
        self.vector_storage = {}
        os.remove('basic_vector_storage.pk')
        os.remove('basic_sorted_ids.pk')

    def add_update_vectors(self, ids, vectors, vec_type):
        for id, vector in zip(ids, vectors.tolist()):
            self._add_update_vector(id, np.array(vector), vec_type)
        self._save_to_disk()

    def remove_vectors(self, ids, vec_type):
        for id, vector in zip(ids):
            self._remove_vector(id, vec_type)
        self._save_to_disk()

    def get_all_vectors(self, vec_type):
        vectors=[]
        for id in self.sorted_ids[vec_type]:
            vectors.append(self.vector_storage[vec_type][id])
        return np.array(vectors), self.sorted_ids[vec_type]

    def get_vector_Ids(self, vector_indexes, vec_type):
        Ids=[]
        for idx in vector_indexes:
          Ids.append(self.sorted_ids[vec_type][idx])
        return Ids


