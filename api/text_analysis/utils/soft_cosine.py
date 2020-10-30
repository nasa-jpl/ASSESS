import numpy as np
from scipy.sparse import csr_matrix
import datetime

def soft_cosine(first_sent_tokens, second_sent_tokens, first_sent_wordvecs, second_sent_wordvecs):
    dot_product_sum = 0

    # start=datetime.datetime.now()
    # implementation help from:
    # http://na-o-ys.github.io/others/2015-11-07-sparse-vector-similarities.html
    # https://github.com/sprvCollaboration/soft_cosine
    mat=[]
    for token_a in first_sent_tokens:
        mat.append(first_sent_wordvecs[token_a])
    for token_b in second_sent_tokens:
        mat.append(second_sent_wordvecs[token_b])
    mat=csr_matrix(np.array(mat).transpose())
    sim_mat=np.array(cosine_similarities(mat).todense())

    for i in range(len(first_sent_tokens)):
        for j in range(len(first_sent_tokens), len(first_sent_tokens)+len(second_sent_tokens)):
            cosine_sim = sim_mat[i][j]
            dot_product_sum += cosine_sim
            # print(first_sent_tokens[i], second_sent_tokens[j-len(first_sent_tokens)], cosine_sim)

    norm_a_sum = 0
    for i in range(len(first_sent_tokens)):
        for j in range(len(first_sent_tokens)):
            cosine_sim = sim_mat[i][j]
            norm_a_sum += cosine_sim
            # print(first_sent_tokens[i], first_sent_tokens[j], cosine_sim)

    norm_b_sum = 0
    for i in range(len(first_sent_tokens), len(first_sent_tokens)+len(second_sent_tokens)):
        for j in range(len(first_sent_tokens), len(first_sent_tokens)+len(second_sent_tokens)):
            cosine_sim =sim_mat[i][j]
            norm_b_sum += cosine_sim
            # print(second_sent_tokens[j-len(first_sent_tokens)], second_sent_tokens[j-len(first_sent_tokens)], cosine_sim)

    ##  The below implementation is good for learning, but very slow
    # for token_a in first_sent_tokens:
    #     for token_b in second_sent_tokens:
    #         cosine_sim = cos_similarity(first_sent_wordvecs[token_a], second_sent_wordvecs[token_b])
    #         dot_product_sum += cosine_sim
    #
    # norm_a_sum = 0
    # for token_a in first_sent_tokens:
    #     for token_b in first_sent_tokens:
    #         cosine_sim = cos_similarity(first_sent_wordvecs[token_a], first_sent_wordvecs[token_b])
    #         norm_a_sum += cosine_sim
    #
    # for token_a in first_sent_tokens:
    #     for token_b in first_sent_tokens:
    #         cosine_sim = cos_similarity(first_sent_wordvecs[token_a], first_sent_wordvecs[token_b])
    #         norm_a_sum += cosine_sim
    #
    # norm_b_sum = 0
    # for token_a in second_sent_tokens:
    #     for token_b in second_sent_tokens:
    #         cosine_sim = cos_similarity(second_sent_wordvecs[token_a], second_sent_wordvecs[token_b])
    #         norm_b_sum += cosine_sim

    # print('time taken:',datetime.datetime.now()-start)


    soft_cosine = dot_product_sum / ((norm_a_sum ** 0.5) * (norm_b_sum) ** 0.5)
    return (soft_cosine)

import sklearn.preprocessing as pp

def cosine_similarities(mat):
    col_normed_mat = pp.normalize(mat.tocsc(), axis=0)
    return col_normed_mat.T * col_normed_mat

def cos_similarity(vect1, vect2):
    dot_product = np.dot(vect1, vect2)
    norm1 = np.linalg.norm(vect1)
    norm2 = np.linalg.norm(vect2)
    similarity = dot_product / (norm1 * norm2)
    return (similarity)