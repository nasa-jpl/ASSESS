import numpy as np
from tqdm import tqdm
import re

def get_sentences(l, n):
    """
    break the text into sentences; simple scheme using space separator
    """
    l=l.split()
    for i in range(0, len(l), n):
        yield ' '.join(l[i:i + n])

def divide_chunks(l, n):
    for i in range(0, len(l), n):
        yield l[i:i + n]


def get_BERT_vectors(list_of_texts, model, tokenizer, layers=None, batch_size=100):

    if layers is None:
        layers=list(range(9, 13))

    # create sentences from each text because BERT only takes a limited number of tokens as input. Also, maintain a mapping between text and its sentences.
    # when we say paragraph we mean any length of text.
    paragraph_idx_to_sentence_idxs = []
    all_sentences = []
    for text in list_of_texts:
        sentences = list(get_sentences(text, 20))
        all_sentences_next_id = len(all_sentences)
        paragraph_idx_to_sentence_idxs.append(
            list(range(all_sentences_next_id, all_sentences_next_id + len(sentences))))
        all_sentences.extend(sentences)

    # function to get activations from the BERT model, give a list of sentences (small enough so that nothing will be discarded!)
    def get_activations(list_of_sentences):
        encoded_input = tokenizer(list_of_sentences, padding=True, truncation=True, return_tensors="tf")
        outputs = model(**encoded_input)
        hidden_states = list(outputs[1])
        # NOTE:- for some reason directly doing np.array(hidden_states) does not always work, so an extra below operation!
        hidden_states= [hidden_state.numpy() for hidden_state in hidden_states]
        hidden_states=np.array(hidden_states)
        hidden_states_sent =hidden_states[layers]
        # print(hidden_states_sent.shape)
        hidden_states_sent = np.reshape(hidden_states_sent, (hidden_states[0].shape[0],
                                                             len(layers),
                                                             hidden_states[0].shape[1],
                                                             hidden_states[0].shape[2]))

        # # create sentence vectors
        # By averaging everything (shape=(num_sent, features))
        sent_vecs_schm_avg = np.average(hidden_states_sent, axis=2)
        sent_vecs_schm_avg = np.average(sent_vecs_schm_avg, axis=1)
        return sent_vecs_schm_avg

    # chunk list of sentences into smaller batches to improve memory and can be parallelized in future.
    # WARNING: currently, the Hugginface Model class does not lend itself to parallelization, due to some picklization error!
    all_sent_vectors = []
    for chunked_sentences in tqdm(list(divide_chunks(all_sentences, batch_size))):
        chunk_of_vector = get_activations(chunked_sentences)
        all_sent_vectors.extend(chunk_of_vector)
    all_sent_vectors = np.array(all_sent_vectors)

    # average the vectors of the sentences for each text using the mapping
    paragraph_vectors = []
    for sent_idxs in tqdm(paragraph_idx_to_sentence_idxs):
        para_vec_schm_avg = np.average(all_sent_vectors[sent_idxs], axis=0)
        paragraph_vectors.append(para_vec_schm_avg)
    paragraph_vectors = np.array(paragraph_vectors)

    return paragraph_vectors

def preprocessor(text):
    if type(text) == str:
        text = re.sub('<[^>]*>', '', text)
        text = re.sub('[\W]+', '', text.lower())
    return text

def spacy_tokenize_lemmatize_punc_remove(text, nlp):

    processed = nlp(text)
    lemma_list = []
    for token in processed:
        if token.is_stop is False:
            token_preprocessed = preprocessor(token.lemma_.lower())
            if token_preprocessed != '':
                lemma_list.append(token_preprocessed)
    return lemma_list

"""
Refs:
https://towardsdatascience.com/setting-up-text-preprocessing-pipeline-using-scikit-learn-and-spacy-e09b9b76758f
"""