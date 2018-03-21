"""
One way to test doc2vec is to test its similarity method on 3 sets, A-B-C, where A & B are chosen such
that they have a high degree of similarity, and C is randomly chosen. For this set, I will choose A & B
from the same top level ICS category and C from some other random category. A & B should evaluate to be
more similar than A & C or B & C.

We can additionally test its weighting by choosing a set of docs the model was trained on and comparing
the similarity of their vectors to the vectors created by inferring a weight on the same doc.
"""
from gensim.models.doc2vec import Doc2Vec, TaggedDocument, LabeledSentence
import json
import random
from random import shuffle
from scipy.spatial.distance import cosine
import os

from itertools import groupby

random.seed(1234)
data_path = "adeploy/ASSESS/data/ISO/catalogue/iso_flat.json"

with open(data_path, "r") as f:
    data = json.load(f)


def split_ics(row):
    row["ics"][0] = row["ics"][0].split(".")
    return row


def concat_title_descr(row):
    row["title_descr"] = row["title"] + ". " + row["description"]
    return row


data = map(split_ics, data)
data = map(concat_title_desc, data)
data.sort(key = lambda row: row["ics"][0])
groups = groupby(data, lambda row: row["ics"][0])
keys = []
for key, group in groups:
    keys.append(key)

A_B_keys = random.sample(keys, len(keys)//2)
C_keys = set(keys) - set(A_B_keys)

train = []
A_B = []
C = []

for key, group in groups:
    train_temp = random.sample(group, int(len(group)*.7))
    if key in A_B_keys:
         A_B.append(set(group) - set(train_temp))
    else:
         C.append(set(group) - set(train_temp))
    train.append(train_temp)

print("Length train %d" % len(train))
print("Length of A_B %d" % len(A_B))
# # TODO: implement with from disk streaming
# class LabeledLineSentence(object):
#     def __init__(self, doc_list, labels_list):
#         self.labels_list = labels_list
#         self.doc_list = doc_list
#
#     def __iter__(self):
#         shuffle(self.labels_list)
#         for idx in self.labels_list:
#             # TODO: test with spaCy tokenizer as well
#             yield TaggedDocument(self.doc_list[idx].split(), [idx])
#
#
# doc_labels = range(len(train))
#
# doc_iterator = LabeledLineSentence(train["title_descr"], doc_labels)
#
# model = Doc2Vec(vector_size=100, window=10, min_count=5, workers=8,
#                 alpha=0.025, min_alpha=0.015)  # just threw in some params for now
#
# model.build_vocab(doc_iterator)
#
# model.train(doc_iterator, total_examples=model.corpus_count, epochs=10)
#
# model.save("trained_models/Doc2Vec_test3")
#
# #check the similarity between A & B, A & C. We don't need to test for every pair combo.
#
# # sanity check: The vector the model infers for an example in the training data should
# # should have a cosine similarity with the stored vector very close to 1
#
# test = text[0]
# p = model[0]
# q = model.infer_vector(test.split())
# dissimilarity = cosine(p, q)
# similarity = (dissimilarity - 1) * (-1)
# print(similarity)
