from jpl.pipedreams.plugins_ops import Plugin


class Template(Plugin):
    def __init__(self):
        super().__init__()
        self.description = 'for creating and managing Dense Vectors'

    def vectorize(self, list_of_texts):
        raise NotImplementedError

    def save_to_disk(self, target_path):
        raise NotImplementedError

    def load_from_disk(self, target_path):
        raise NotImplementedError

    def exists_on_disk(self, target_path):
        raise NotImplementedError
