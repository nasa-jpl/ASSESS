"""
This is research code to try out Word Mover's Distance implementations

"""

# ======================================================================================================================
## load word2vec model
# ======================================================================================================================

# sentence_A = 'Obama speaks to the media in Illinois'
# sentence_B = 'The president greets the press in Chicago'

# sentence_A = 'american bank is the best financial institution'
sentence_B = 'bank of this river is overflowing'
sentence_A = 'bank has agreed to give us money'

def preprocess(sentence, model):
    return [item for item in sentence.lower().split() if item in model]

import gensim.downloader as api
model = api.load('word2vec-google-news-300')

# print(model['president'])


sentence_A = preprocess(sentence_A, model)
sentence_B = preprocess(sentence_B, model)

# ======================================================================================================================
## WMD Using Gensim
# ======================================================================================================================

# distance = model.wmdistance(sentence_obama, sentence_president)
# print('distance = %.4f' % distance)
# sentence_orange = preprocess('Oranges are my favorite fruit')
# distance = model.wmdistance(sentence_obama, sentence_orange)
# print('distance = %.4f' % distance)
#
# exit()


# ======================================================================================================================
## WMD Using PulP solver
# ======================================================================================================================
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
def word_mover_distance_probspec(first_sent_tokens, second_sent_tokens, wvmodel, lpFile=None):
    all_tokens = list(set(first_sent_tokens+second_sent_tokens))
    wordvecs = {token: wvmodel[token] for token in all_tokens}

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

print('stated calculating wmd....')
prob = word_mover_distance_probspec(sentence_A, sentence_B, model)
print(pulp.value(prob.objective))
for v in prob.variables():
    if v.varValue!=0:
        print(v.name, '=', v.varValue)



