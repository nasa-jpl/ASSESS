from jpl.pipedreams.plugins_ops import Plugin


class Template(Plugin):
    def __init__(self):
        super().__init__()
        self.description = 'for storing Dense Vectors'

    def clean_storage(self, *args, **kwargs):
        raise NotImplementedError

    def load_from_disk(self, *args, **kwargs):
        raise NotImplementedError

    def add_update_vectors(self, ids, vectors, vec_type):
        raise NotImplementedError

    def remove_vectors(self, ids, vec_type):
        raise NotImplementedError

    def get_all_vectors(self, vec_type):
        raise NotImplementedError

    def get_vector_Ids(self,  vector_indexes, vec_type):
        raise NotImplementedError