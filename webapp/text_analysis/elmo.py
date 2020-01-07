"""
This is research code to try out Elmo implementations
"""

# ======================================================================================================================
## get elmo vectors using allennlp
# ======================================================================================================================

# from allennlp.commands.elmo import ElmoEmbedder
# elmo = ElmoEmbedder()
# tokens = ["I", "ate", "an", "apple", "for", "breakfast"]
# vectors = elmo.embed_sentence(tokens)
#
# import scipy
# vectors2 = elmo.embed_sentence(["I", "ate", "a", "carrot", "for", "breakfast"])
# scipy.spatial.distance.cosine(vectors[2][3], vectors2[2][3]) # cosine distance between "apple" and "carrot" in the last layer


# ======================================================================================================================
## get elmo vectors using tensorflow-hub
# ======================================================================================================================

# import tensorflow_hub as hub
# import tensorflow.compat.v1 as tf
# import numpy as np
# # To make tf 2.0 compatible with tf1.0 code, we disable the tf2.0 functionalities
# # https://github.com/tensorflow/hub/issues/350
# tf.disable_eager_execution()
#
# elmo = hub.Module("https://tfhub.dev/google/elmo/2")
#
# # just a random sentence
# x = ["Roasted ants are a popular snack in Columbia"]
#
# # Extract ELMo features
# embeddings = elmo(x, signature="default", as_dict=True)["elmo"]
#
#
# print(embeddings.shape)
# print(embeddings)
#
# with tf.Session() as session:
#   session.run([tf.global_variables_initializer(), tf.tables_initializer()])
#   numpy_arr = session.run(embeddings)
#
# print(numpy_arr)



# ======================================================================================================================
## WMD using PulP solver, modified to use ELMO vectors
# ======================================================================================================================
import tensorflow_hub as hub
import tensorflow.compat.v1 as tf
import numpy as np
from scipy.spatial import distance

# To make tf 2.0 compatible with tf1.0 code, we disable the tf2.0 functionalities
# https://github.com/tensorflow/hub/issues/350
tf.disable_eager_execution()

elmo = hub.Module("https://tfhub.dev/google/elmo/2")


# sentence_A = 'Obama speaks to the media in Illinois'
# sentence_B = 'The president greets the press in Chicago'

# sentence_A = 'our bank is the best financial institution know to us'
# sentence_B = 'the bank of this river is overflowing'
# sentence_C = 'bank has agreed to give us money'

sentence_A = 'the release of this version of the tool is upon us'
sentence_B = 'the gases released in the atmosphere are giving rise to global warming'
sentence_C = 'I released this chemical yesterday'
# sentence_C = 'I released this movie yesterday'


sentences=[sentence_A, sentence_B, sentence_C]

embeddings = elmo(sentences, signature="default", as_dict=True)["elmo"]

print(embeddings.shape)

with tf.Session() as session:
  session.run([tf.global_variables_initializer(), tf.tables_initializer()])
  numpy_arr = session.run(embeddings)

# print(numpy_arr)

wordvecs={}
sentences_tokens=[]
for i,sent in enumerate(sentences):
    sentence_tokens=[]
    for j,token in enumerate(sent.lower().split()):
        sentence_tokens.append(token+'_~_'+str(i))
        wordvecs[token+'_~_'+str(i)]=numpy_arr[i][j]
    sentences_tokens.append(sentence_tokens)

# # test the distances between word vectors generated based on context
# print(distance.euclidean(wordvecs['bank_~_0'],wordvecs['bank_~_1']))
# print(distance.euclidean(wordvecs['bank_~_1'],wordvecs['bank_~_2']))
# print(distance.euclidean(wordvecs['bank_~_2'],wordvecs['bank_~_3']))
# exit()

# print(distance.euclidean(wordvecs['release_~_0'],wordvecs['released_~_1']))
# print(distance.euclidean(wordvecs['released_~_1'],wordvecs['released_~_2']))
# print(distance.euclidean(wordvecs['released_~_2'],wordvecs['release_~_0']))
# exit()

# print(wordvecs)

from itertools import product
from collections import defaultdict
import gensim

import numpy as np
from scipy.spatial.distance import euclidean
import pulp


singleindexing = lambda m, i, j: m*i+j
unpackindexing = lambda m, k: (k/m, k % m)


def tokens_to_fracdict(tokens):
    cntdict = defaultdict(lambda : 0)
    for token in tokens:
        cntdict[token] += 1
    totalcnt = sum(cntdict.values())
    return {token: float(cnt)/totalcnt for token, cnt in cntdict.items()}


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


def word_mover_distance(first_sent_tokens, second_sent_tokens, wvmodel, lpFile=None):
    prob = word_mover_distance_probspec(first_sent_tokens, second_sent_tokens, wvmodel, lpFile=lpFile)
    return pulp.value(prob.objective)

prob = word_mover_distance_probspec(sentences_tokens[1], sentences_tokens[2], wordvecs)
print(pulp.value(prob.objective))
for v in prob.variables():
    if v.varValue!=0:
        print(v.name, '=', v.varValue)