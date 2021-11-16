from jpl.pipedreams.plugins_ops import Plugin

class Template(Plugin):
    def __init__(self):
        super().__init__()
        self.description = 'for Indexing and retrieval of Dense Vectors'

    def create_index(self, vectors):
        raise NotImplementedError

    def save_to_disk(self, target_path):
        raise NotImplementedError

    def load_from_disk(self, target_path):
        raise NotImplementedError

    def exists_on_disk(self, target_path):
        raise NotImplementedError

    def get_top_n(self, target_vector, n):
        raise NotImplementedError

