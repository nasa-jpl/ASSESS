from .template import Template
import pickle
import os
import numpy as np
from tqdm import tqdm
import gc

class Basic(Template):
    def __init__(self):
        super().__init__()
        self.description = "for storing Dense Vectors"
        self.sorted_ids = {}
        self.vector_storage = {}

    def _add_update_vector(self, id, vector, vec_type):
        if vec_type not in self.vector_storage.keys():
            self.vector_storage[vec_type] = {}
        self.vector_storage[vec_type][id] = vector
        if vec_type not in self.sorted_ids.keys():
            self.sorted_ids[vec_type] = []
        if id not in self.sorted_ids[vec_type]:
            self.sorted_ids[vec_type].append(id)

    def _remove_vector(self, id, vec_type):
        self.vector_storage[vec_type].pop(id)
        self.sorted_ids[vec_type].remove(id)

    def _save_to_disk(self):
        with open("data/basic_vector_storage.pk", "wb") as storage:
            pickle.dump(self.vector_storage, storage)
        gc.collect()
        with open("data/basic_sorted_ids.pk", "wb") as ids:
            pickle.dump(self.sorted_ids, ids)

    def load_from_disk(self):
        if os.path.exists("data/basic_vector_storage.pk") and os.path.exists(
                "data/basic_sorted_ids.pk"
        ):
            self.vector_storage = pickle.load(open("data/basic_vector_storage.pk", "rb"))
            self.sorted_ids = pickle.load(open("data/basic_sorted_ids.pk", "rb"))

    def clean_storage(self):
        self.sorted_ids = {}
        self.vector_storage = {}
        os.remove("data/basic_vector_storage.pk")
        os.remove("data/basic_sorted_ids.pk")

    def add_update_vectors(self, ids, vectors, vec_type):
        vectors = np.asarray(vectors)
        for id, vector in tqdm(zip(ids, vectors), total=len(ids)):
            self._add_update_vector(id, vector, vec_type)
        print('writing to disk..')
        self._save_to_disk()
        print('writing complete!')

    def remove_vectors(self, ids, vec_type):
        for id, vector in zip(ids):
            self._remove_vector(id, vec_type)
        self._save_to_disk()

    def get_all_vectors(self, vec_type):
        vectors = []
        for id in self.sorted_ids[vec_type]:
            vectors.append(self.vector_storage[vec_type][id])
        return np.array(vectors), self.sorted_ids[vec_type]

    def unload_only_vectors_from_memory(self):
        self.vector_storage = {}
        gc.collect()

    def get_vector_Ids(self, vector_indexes, vec_type):
        Ids = []
        for idx in vector_indexes:
            Ids.append(self.sorted_ids[vec_type][idx])
        return Ids
