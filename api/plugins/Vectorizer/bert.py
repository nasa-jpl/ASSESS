from .template import Template
from .utilities import get_BERT_vectors

from transformers import AutoTokenizer
from transformers import TFAutoModelForMaskedLM

class TF_IDF(Template):
    def __init__(self):
        super().__init__()
        self.description = 'Implements the BERT vectorizer'

    def train(self, list_of_texts):
        # can be used as is without re-training
        pass

    def vectorize(self, list_of_texts):
        self.tokenizer = AutoTokenizer.from_pretrained('bert-base-uncased')
        self.model = TFAutoModelForMaskedLM.from_pretrained("bert-base-uncased", output_hidden_states=True)

        BERT_vectors=get_BERT_vectors(list_of_texts, self.model, self.tokenizer)

        return BERT_vectors

    def save_to_disk(self, target_path):
        # gets automatically saved on disk when first used
        pass

    def load_from_disk(self, target_path):
        self.tokenizer=AutoTokenizer.from_pretrained('bert-base-uncased')
        self.model=TFAutoModelForMaskedLM.from_pretrained("bert-base-uncased", output_hidden_states=True)

    def exists_on_disk(self, target_path):
        return True
