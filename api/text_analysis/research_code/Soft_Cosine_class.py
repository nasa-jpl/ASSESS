# -*- coding: utf-8 -*-
"""
Created on Tue Jan 21 16:12:23 2020

@author: SParravano
"""

import gensim

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from nltk.tokenize import word_tokenize
import string
import numpy as np

from scipy import spatial
import time


# %%
class soft_cosine:
    def __init__(self, project):
        self.project = project
        print('Thank you for using the Soft_Cosine class for Project: ' + self.project)

    def soft_cosine_prep(self, ordered_list_features, word_embeddings, similarity_threshold=0):
        Global_start_time = time.time()
        print('##########')
        # print('Step one: Tokenizing our corpus..')
        # list_of_tokens=[word_tokenize(x) for x in corpus]
        # we can flatten out the list
        # list_of_tokens=list(set(list([item for sublist in list_of_tokens for item in sublist])))
        list_of_tokens = list(ordered_list_features)

        # we can use our word2vec embeddings to look up the dense vector representations of each of our features
        print('Creating Dictionary to look up our word embeddings..')
        dict_ = {}
        for token_ in list_of_tokens:
            key_ = str(token_)
            value_ = word_embeddings[token_]
            dict_.update({key_: value_})

        # let's build out our similarity matrix of dense word vectors
        # The matrix should be of sixe n x n where n is the number of features (tokens)
        # We should also expect our similarity matrix to be symmetric with diagonal values of 1
        print('Creating similarity matrix to compute sim i,j scores for our features')
        A = np.empty([len(dict_), len(dict_[key_])])
        counter_ = 0
        for key in dict_:
            A[counter_] = (np.array(dict_[key]))
            counter_ += 1

        # we can now compute the pairwise similarities of each of our features using cosine similarity
        similarity_matrix = cosine_similarity(A)

        print('Storing pairwise similarity scores in a Dictionary..')
        # we can store these in a dictionary
        similarity_dict = {}
        keys_list = list(dict_.keys())
        counter_ = 0
        for x in range(len(keys_list)):
            for y in range(len(keys_list)):
                key_ = keys_list[x] + '_' + keys_list[y]
                value_ = similarity_matrix[x, y]
                similarity_dict.update({key_: value_})
        # similarity threshold step... it's easy to see from the math that the soft cosine is
        # susceptible to over estimating the true siilarity betweeen documents by including similarity
        # terms between features that are not really realted. By viture of how word vectors are represetend
        # two words that are NOT similar will still yield a similarity score > 0. To combat this we can
        # introduce a threshold. Scores below the threshold will be encoded to 0. Deciding what the threshold should
        # be is another problem. A solution is not proposed her but for now the practitioner will pass it as a
        # parameter.
        if similarity_threshold == 0:
            pass
        else:
            print('Updating pairwise similarity scores to account for the user inputted similarity threshold.')
            for x in similarity_dict:
                if similarity_dict[x] < similarity_threshold:
                    similarity_dict[x] = 0

        print('Returning Similarity Dictionary and Word Embedding Dictionary')
        Global_time_end = time.time()
        total_time = Global_time_end - Global_start_time
        print('Our prep was completed in:', str(total_time))
        print('##########')
        print('\n')
        return (similarity_dict, dict_)

        # given two documents we have been studying..

    def soft_cosine(self, ordered_list_features, word_embedding_dictionary, similarity_dictionary, doc1, doc2):
        Global_start_time = time.time()
        # keys_list=list(word_embedding_dictionary.keys())
        keys_list = ordered_list_features
        print('##########')
        print('Starting Vector Math Computations...')
        dot_product_sum = 0
        for i in range(len(keys_list)):
            for j in range(len(keys_list)):
                sim_i_j_string = keys_list[i] + '_' + keys_list[j]
                sim_i_j = similarity_dictionary[sim_i_j_string]
                dot_prod_element_i_j = sim_i_j * doc1[i] * doc2[j]
                dot_product_sum += dot_prod_element_i_j
                if dot_prod_element_i_j!=0:
                    print(keys_list[i],keys_list[j],sim_i_j, dot_prod_element_i_j)

        print('boop', dot_product_sum)
        norm_a_sum = 0
        for i in range(len(keys_list)):
            for j in range(len(keys_list)):
                sim_i_j_string = keys_list[i] + '_' + keys_list[j]
                sim_i_j = similarity_dictionary[sim_i_j_string]
                dot_prod_element_i_j = sim_i_j * doc1[i] * doc1[j]
                norm_a_sum += dot_prod_element_i_j
                if dot_prod_element_i_j!=0:
                    print(keys_list[i],keys_list[j],sim_i_j)

        print('boop', norm_a_sum)

        norm_b_sum = 0
        for i in range(len(keys_list)):
            for j in range(len(keys_list)):
                sim_i_j_string = keys_list[i] + '_' + keys_list[j]
                sim_i_j = similarity_dictionary[sim_i_j_string]
                dot_prod_element_i_j = sim_i_j * doc2[i] * doc2[j]
                norm_b_sum += dot_prod_element_i_j
                if dot_prod_element_i_j!=0:
                    print(keys_list[i],keys_list[j],sim_i_j, dot_prod_element_i_j)

        print('boop', norm_b_sum)

        soft_cosine = dot_product_sum / ((norm_a_sum ** 0.5) * (norm_b_sum) ** 0.5)
        # print('Norm a sum:',norm_a_sum,'Norm b sum:',norm_b_sum,'Dot product:',dot_product_sum,'sotft_cosine:',soft_cosine)
        Global_time_end = time.time()
        total_time = Global_time_end - Global_start_time
        print('Our result was calculated in:', str(total_time))
        print('Soft Cosine Score:', str(soft_cosine))
        print('##########')
        print('\n')
        return (soft_cosine)

    def soft_cosine_mod(self, first_sent_tokens, second_sent_tokens, first_sent_wordvecs, second_sent_wordvecs):

        dot_product_sum = 0
        for token_a in first_sent_tokens:
            for token_b in second_sent_tokens:
                cosine_sim = self.cos_similarity(first_sent_wordvecs[token_a], second_sent_wordvecs[token_b])
                dot_product_sum += cosine_sim
                print(token_a, token_b, cosine_sim)

        norm_a_sum = 0
        for token_a in first_sent_tokens:
            for token_b in first_sent_tokens:
                cosine_sim = self.cos_similarity(first_sent_wordvecs[token_a], first_sent_wordvecs[token_b])
                norm_a_sum += cosine_sim
                print(token_a, token_b, cosine_sim)

        norm_b_sum = 0
        for token_a in second_sent_tokens:
            for token_b in second_sent_tokens:
                cosine_sim = self.cos_similarity(second_sent_wordvecs[token_a], second_sent_wordvecs[token_b])
                norm_b_sum += cosine_sim
                print(token_a, token_b, cosine_sim)


        soft_cosine = dot_product_sum / ((norm_a_sum ** 0.5) * (norm_b_sum) ** 0.5)
        return (soft_cosine)

    def cos_similarity(self, vect1, vect2):
        dot_product = np.dot(vect1, vect2)
        norm1 = np.linalg.norm(vect1)
        norm2 = np.linalg.norm(vect2)
        similarity = dot_product / (norm1 * norm2)
        return (similarity)
# %%
