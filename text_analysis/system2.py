import networkx as nx
import nltk
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer

import utils as use


# Calculate the 1-gram scores based on TRS (technique-4). Find the cosine similarity and rank documents.
# Use keywords (provide as an option). Extract and score keywords. Use them with some labmda importance over the n-gram scores.


def ne_rank(text_tf_1,text_tf_2):
    ranks = {}
    g = nx.Graph()
    indices = text_tf_2.indices
    for i in indices:
        ind = tfidftransformer_1.transform([vocab_map_2[i]])[0].indices
        # spl case when both words are the same
        if len(ind) < 2:
            continue
        if not g.has_edge(ind[0], ind[1]):
            g.add_node(ind[0], {'tfidf': text_tf_1[0, ind[0]]})
            g.add_node(ind[1], {'tfidf': text_tf_1[0, ind[1]]})
            g.add_edge(ind[0], ind[1], {"weight": 0})
            ranks[ind[0]] = 0
            ranks[ind[1]] = 0

        weight = g.edge[ind[0]][ind[1]]["weight"]
        weight += 1
        g.add_edge(ind[0], ind[1], {"weight": weight})

    iterations = 1000
    current = g.nodes()[0]

    for i in range(iterations):
        # print i
        neighbours = g.neighbors(current)
        neighbours_score = {}

        for neighbour in neighbours:
            tfidf = g.node[neighbour]['tfidf']
            weight = g.edge[neighbour][current]['weight']
            mult = tfidf * weight
            neighbours_score[neighbour] = mult

        prob = np.array(neighbours_score.values(), dtype=float)
        total = np.sum(prob)
        if total != 0:
            prob = prob / total
        current = np.random.choice(neighbours_score.keys(), 1, p=prob)[0]
        # toss a coin
        toss = np.random.choice([True, False], 1)[0]
        if toss:
            ranks[current] += 1
        else:
            current = np.random.choice(g.nodes(), 1)[0]

    words = ranks.keys()
    ranks = np.array(ranks.values(), dtype=float)
    total = np.sum(ranks)
    if total != 0:
        ranks = ranks / total

    final = {}
    final_vec = {}
    for word, rank in zip(words, ranks):
        final[vocab_map_1[word]] = rank
        final_vec[word] = rank
    return final_vec

n=1
sow=''
labmbda=0.5
n_results=10

# ===================== read standards =======================

texts_all=open('standards','r').readlines()
categories=[line.split(' ')[0] for line in texts_all]
texts_all=[' '.join(line.decode('utf-8').strip().split(' ')[1:]) for line in texts_all]
title_all=[]

# ===================== read sow =======================

sow=open('sow_test','r').read().decode('utf-8')


# ===================== create the model =======================


poss=['JJ','NN','RB']
texts_all_new=[]
for text in texts_all:
    text_new=[]
    t = nltk.pos_tag(nltk.word_tokenize(text))
    for a,b in t:
        for pos in poss:
            if pos in b:
                text_new.append(a)
    text_new=' '.join(text_new)
    texts_all_new.append(text_new)


tfidftransformer_1=TfidfVectorizer(ngram_range=(1,1))
tfidftransformer_2=TfidfVectorizer(ngram_range=(2,2))


texts_all_tf_2=tfidftransformer_2.fit_transform(texts_all_new)
texts_all_tf_1=tfidftransformer_1.fit_transform(texts_all_new)

tfidftransformer_1.fit(texts_all_new)

vocab_map_2 = {v: k for k, v in tfidftransformer_2.vocabulary_.iteritems()}
vocab_map_1 = {v: k for k, v in tfidftransformer_1.vocabulary_.iteritems()}



master_phrases_vectors=[]
master_nerank_vectors=[]
for text,text_tf_1,text_tf_2 in zip(texts_all,texts_all_tf_1,texts_all_tf_2):


    final_vec=ne_rank(text_tf_1,text_tf_2)

    phrases=use.noun_tokenize(text)
    phrases=list(set(phrases))
    phrases_vectors=[list(tfidftransformer_1.transform([x])[0].indices) for x in phrases]
    phrases_dict = {}
    for x, phrase in zip(phrases_vectors, phrases):
        x=[final_vec[y] for y in x if y in final_vec.keys()]
        avg = np.sum(x)
        phrases_dict[phrase] = avg
    master_phrases_vectors.append(phrases_dict)
    master_nerank_vectors.append(final_vec)


# ===================== vectorize the SOW =======================

sow_tf1=tfidftransformer_1.transform([sow])[0]
sow_tf2=tfidftransformer_2.transform([sow])[0]

sow_final_vec=ne_rank(sow_tf1,sow_tf2)

phrases=use.noun_tokenize(sow)
phrases=list(set(phrases))
phrases_vectors=[list(tfidftransformer_1.transform([x])[0].indices) for x in phrases]
sow_phrase_dict = {}
for x, phrase in zip(phrases_vectors, phrases):
    x = [final_vec[y] for y in x if y in final_vec.keys()]
    avg = np.sum(x)
    sow_phrase_dict[phrase] = avg


# ===================== find cosine similarities =======================

similarities=[]
for nerank_vec,phrase_dict in zip(master_nerank_vectors,master_phrases_vectors):
    sim_nerank=use.get_cosine(nerank_vec,sow_final_vec)
    sim_keyword=use.get_cosine(phrase_dict,sow_phrase_dict)
    sim=(labmbda*sim_nerank)+((1-labmbda)*sim_keyword)
    similarities.append(sim)


# ===================== rank the documents and print the top n =======================

ranked_docs=list(reversed(np.argsort(similarities)))

for i in range(n_results):
    index=ranked_docs[i]
    print similarities[index] #,title_all[index]

