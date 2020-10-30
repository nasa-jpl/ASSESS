from itertools import product
from collections import defaultdict
import pysbd
import tensorflow.compat.v1 as tf
import numpy as np
import tensorflow_hub as hub
from scipy.spatial.distance import euclidean
import pulp
import pandas
import datetime

seg = pysbd.Segmenter(language="en", clean=False)
tf.disable_eager_execution()

model_elmo= None


singleindexing = lambda m, i, j: m*i+j
unpackindexing = lambda m, k: (k/m, k % m)


def tokens_to_fracdict(tokens):
    cntdict = defaultdict(lambda : 0)
    for token in tokens:
        cntdict[token] += 1
    totalcnt = sum(cntdict.values())
    return {token: float(cnt)/totalcnt for token, cnt in cntdict.items()}

def load_model():
    global model_elmo
    if model_elmo==None:
        filename = 'https://tfhub.dev/google/elmo/3'
        model_elmo = hub.Module(filename)
    return model_elmo


# use PuLP
def word_mover_distance_probspec(first_sent_tokens, second_sent_tokens, wordvecs, lpFile=None):
    all_tokens = list(set(first_sent_tokens+second_sent_tokens))

    first_sent_buckets = tokens_to_fracdict(first_sent_tokens)
    second_sent_buckets = tokens_to_fracdict(second_sent_tokens)

    T = pulp.LpVariable.dicts('T_matrix', list(product(all_tokens, all_tokens)), lowBound=0)

    prob = pulp.LpProblem('WMD', sense=pulp.LpMinimize)
    prob += pulp.lpSum([T[token1, token2]*euclidean(wordvecs[token1], wordvecs[token2])
                        for token1, token2 in product(all_tokens, all_tokens)])
    for token2 in second_sent_buckets:
        prob += pulp.lpSum([T[token1, token2] for token1 in first_sent_buckets])==second_sent_buckets[token2]
    for token1 in first_sent_buckets:
        prob += pulp.lpSum([T[token1, token2] for token2 in second_sent_buckets])==first_sent_buckets[token1]

    if lpFile!=None:
        prob.writeLP(lpFile)

    prob.solve()

    return prob

def word_mover_distance_probspec_mod(first_sent_tokens, second_sent_tokens, first_sent_wordvecs, second_sent_wordvecs, lpFile=None):

    # merge the two lookups:
    wordvecs={}
    for k, v in first_sent_wordvecs.items():
        wordvecs[k]=v
    for k, v in second_sent_wordvecs.items():
        wordvecs[k]=v

    all_tokens = list(set(first_sent_tokens+second_sent_tokens))

    first_sent_buckets = tokens_to_fracdict(first_sent_tokens)
    second_sent_buckets = tokens_to_fracdict(second_sent_tokens)

    T = pulp.LpVariable.dicts('T_matrix', list(product(all_tokens, all_tokens)), lowBound=0)

    prob = pulp.LpProblem('WMD', sense=pulp.LpMinimize)
    prob += pulp.lpSum([T[token1, token2]*euclidean(wordvecs[token1], wordvecs[token2])
                        for token1, token2 in product(all_tokens, all_tokens)])
    for token2 in second_sent_buckets:
        prob += pulp.lpSum([T[token1, token2] for token1 in first_sent_buckets])==second_sent_buckets[token2]
    for token1 in first_sent_buckets:
        prob += pulp.lpSum([T[token1, token2] for token2 in second_sent_buckets])==first_sent_buckets[token1]

    if lpFile!=None:
        prob.writeLP(lpFile)

    prob.solve()

    return prob

def word_mover_distance(first_sent_tokens, second_sent_tokens, wvmodel, lpFile=None):
    prob = word_mover_distance_probspec(first_sent_tokens, second_sent_tokens, wvmodel, lpFile=lpFile)
    return pulp.value(prob.objective)


def process_text_for_elmo_wmd(text, suffix=0, unique_connector= '_~_'):
    """
    process the text to be able to use with ELMO enabled version of WMD. Then, create ELMO vectors as well.
    """
    # elmo = hub.Module("https://tfhub.dev/google/elmo/3") # todo: this worked well with the vector generation using 'Dask'
    elmo=load_model()
    wordvecs={}

    sentences =seg.segment(text)
    if len(sentences)==0:
        return None, None

    # tokenize the sentences
    sentences_tokens=[item.lower().split() for item in sentences]
    # create padding using "" based on the max length
    tokens_length=[len(item) for item in sentences_tokens]
    max_len=max(tokens_length)
    tokens_input=[item+(max_len-len(item))*[''] for item in sentences_tokens]

    embeddings = elmo(
        inputs={
            "tokens": tokens_input,
            "sequence_len": tokens_length
        },
        signature="tokens",
        as_dict=True)["elmo"]
    # print(embeddings.shape)

    # convert from tensor to array
    with tf.Session() as session:
        session.run([tf.global_variables_initializer(), tf.tables_initializer()])
        numpy_arr = session.run(embeddings)

    # rename the tokens (add suffix) and separate elmo vectors for each tokens
    text_suffixed = []
    for sentence_tokens in sentences_tokens:
        sentence_tokens_suffixed=[]
        for j, token in enumerate(sentence_tokens):
            sentence_tokens_suffixed.append(token + unique_connector + str(suffix))
            wordvecs[token + unique_connector + str(suffix)] = numpy_arr[0][j]

        text_suffixed.extend(sentence_tokens_suffixed)

    return text_suffixed, wordvecs

def give_paragraph_elmo_vector(text):
    elmo = hub.Module("https://tfhub.dev/google/elmo/3")

    sentences = seg.segment(text)

    if len(sentences) == 0:
        # print('Empty returned')
        return ''


    # tokenize the sentences
    sentences_tokens = [item.lower().split() for item in sentences]
    # create padding using "" based on the max length
    tokens_length = [len(item) for item in sentences_tokens]
    max_len = max(tokens_length)
    # add padding
    tokens_input = [item + (max_len - len(item)) * [''] for item in sentences_tokens]

    embeddings = elmo(
        inputs={
            "tokens": tokens_input,
            "sequence_len": tokens_length
        },
        signature="tokens",
        as_dict=True)["elmo"]
    # print(embeddings.shape)

    # convert from tensor to array
    with tf.Session() as session:
        session.run([tf.global_variables_initializer(), tf.tables_initializer()])
        numpy_arr = session.run(embeddings)


    # take mean of elmo token vectors to create a paragraph vector
    token_vectors = []
    for sentence_tokens in sentences_tokens:
        # extract vectors from the array
        for j, token in enumerate(sentence_tokens):
            token_vectors.append(numpy_arr[0][j])

    token_vectors =np.array(token_vectors)
    # print(token_vectors.shape)
    para_vector=np.mean(token_vectors, axis=0)
    # print(para_vector.shape)
    return list(para_vector)

def give_paragraph_elmo_vector_multi(texts):
    """this function takes a list of strings. This is a much faster way to create ELMO vectors"""
    elmo = hub.Module("https://tfhub.dev/google/elmo/3")

    track_sent_position=[] # to track which sent belongs to which paragraph/text
    counter=0
    all_sentences=[]
    empty_texts=[]
    for i, text in enumerate(texts):
        sentences = seg.segment(text)
        if len(sentences)==0:
            sentences=[''] # adding a placeholder, will process the results later
            empty_texts.append(i)
        all_sentences.extend(sentences)
        track_sent_position.append(range(counter, counter+len(sentences)))
        counter+=len(sentences)

    # prepare to get the embeddings
    # tokenize the sentences
    all_sentences_tokens = [item.lower().split() for item in all_sentences]
    # create padding using "" based on the max length
    tokens_length = [len(item) for item in all_sentences_tokens]
    max_len = max(tokens_length)
    # add padding
    tokens_input = [item + (max_len - len(item)) * [''] for item in all_sentences_tokens]
    embeddings = elmo(
        inputs={
            "tokens": tokens_input,
            "sequence_len": tokens_length
        },
        signature="tokens",
        as_dict=True)["elmo"]
    # print(embeddings.shape)

    # convert from tensor to array
    with tf.Session() as session:
        session.run([tf.global_variables_initializer(), tf.tables_initializer()])
        numpy_arr = session.run(embeddings)

    # extract the token vectors and create paragraph vectors
    para_vectors=[]
    for k, positions in enumerate(track_sent_position): # for each paragraph or text
        if k in empty_texts:
            para_vectors.append('')
            continue
        numpy_arr_part=numpy_arr[positions]
        all_sentences_tokens_part=[all_sentences_tokens[i] for i in positions]

        para_token_vectors = []
        for sentence_tokens in all_sentences_tokens_part:
            # extract token vectors and collect for each paragraph
            for j, token in enumerate(sentence_tokens):
                para_token_vectors.append(numpy_arr_part[0][j])

        # take mean of elmo token vectors to create a paragraph vector
        para_token_vectors =np.array(para_token_vectors)
        para_vector=np.mean(para_token_vectors, axis=0)
        para_vectors.append(list(para_vector))

    return para_vectors

# eg codes:
# text='Hello my name is Mr. TomCat. I have come from far lands to do business.'
# print(len(give_paragraph_elmo_vector(text)))

# texts=['Hello my name is Mr. TomCat. I have come from far lands to do business.', 'today is my lucky day. I found a penny on the street']
# para_vectors=give_paragraph_elmo_vector_multi(texts)
# print(para_vectors)
