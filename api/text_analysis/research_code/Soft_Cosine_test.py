# -*- coding: utf-8 -*-
"""
Created on Tue Jan 21 10:24:08 2020

@author: SParravano
"""
dir_path = '/dsdata/Soft_Cosine'

# %%
import os

import gensim

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from nltk.tokenize import word_tokenize
import string
import numpy as np

from scipy import spatial

import api.text_analysis.research_code.Soft_Cosine_class as soft_cosine_1
from api.text_analysis.utils.soft_cosine import *
import time

# %%
from api.text_analysis.utils.word_vectors import *
# In the absence of copious training data we can utilize the pre-trained word embeddings. Google trained their model
# utilizing a Google News dataset with roughly 100 billion words. The vector length is 300 features
# pre_trained = os.path.join(dir_path, 'GoogleNews-vectors-negative300.bin')
# word_vectors = gensim.models.KeyedVectors.load_word2vec_format(pre_trained, binary=True)

word_vectors=load_model('w2v')
# %%

# let's first instantiate our custom built class that conatains the methods we need to perform our vector math
vector_math = soft_cosine_1.soft_cosine('Soft Cosine test Example')
# let's imagine we have 2 documents:
a = ['The woman is extremely ill']
b = ['The man is very sick']

corpus = a + b

# we frist instantiate the contVectorizer class --> this will enable us to create the vector space
# for our corpus
vectorizer = CountVectorizer(binary=True, min_df=1)
vectors_ = vectorizer.fit_transform(corpus)

ordered_list_features = vectorizer.get_feature_names()
if vectors_.toarray().shape[0] < 50:
    print('Below is our vocabulary. Thesve festures define our vector space..')
    print(ordered_list_features)
    print('Here is the vector representation of the documents in our corpus')
    print(vectors_.toarray())
else:
    pass

text_to_print = '''
Using plain vanilla cosine similarity we can directly compute the similarity of our two documents while ignoring any
similarities between features.
'''
print(text_to_print)
print('Here are the results:')
# print(cosine_similarity(vectors_)) #this computes the similarity matrix. Overkill and not needed

# we can compute the cosinfe similarity
vectors_array = vectors_.toarray()
doc1 = vectors_array[0]
doc2 = vectors_array[1]

similarity_cosine = vector_math.cos_similarity(doc1, doc2)
print(similarity_cosine)
# %%
text_to_print2 = '''
Now we transition to a different approach. Can we somehow capture the similarity between features?
extremely and very are similar words, and that should be accounted for. Sick and ill
point ot the same meaning and that also should be part of the calculus here... Man and person are intimately
related concepts as well, and that should be factored into our math. A human reader would be able to recgognize
the two documents as being intrisincally realted; almost identical! Our traditional vector math approach fails to identify this 
relationship. This is because features that are not the same are orthoganal! Let's try to correct for this. 
'''
print(text_to_print2)

similarity_dictionary, word_embedding_dictionary = vector_math.soft_cosine_prep(
    ordered_list_features=ordered_list_features,
    word_embeddings=word_vectors,
    similarity_threshold=0)

print(similarity_dictionary)
soft_cosine_score = vector_math.soft_cosine(ordered_list_features=ordered_list_features,
                                      word_embedding_dictionary=word_embedding_dictionary,
                                      similarity_dictionary=similarity_dictionary,
                                      doc1=doc1,
                                      doc2=doc2)
print('score',soft_cosine_score)
soft_cosine_score= soft_cosine(a[0].lower().split(), b[0].lower().split(), word_vectors, word_vectors)
print('score', soft_cosine_score)
