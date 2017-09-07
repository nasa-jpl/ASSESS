import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

import utils as use

# Calculate tf-idf for n-grams (provide as argument). Find cosine similarity. Rank the documents based on cosine similarity.
# Use keywords (provide as an option). Extract and score keywords. Use them with some labmda importance over the n-gram scores.


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
tfidftransformer=TfidfVectorizer(ngram_range=(1,n))
texts_all_tf=tfidftransformer.fit_transform(texts_all)
vocab_map = {v: k for k, v in tfidftransformer.vocabulary_.iteritems()}

master_phrases_vectors=[]
for text_tf,text in zip(texts_all_tf,texts_all):
    text_tf= text_tf.todense()
    phrases=use.noun_tokenize(text)
    phrases=list(set(phrases))
    phrases_vectors=[list(tfidftransformer.transform([x])[0].indices) for x in phrases]
    phrases_dict={}
    for x,phrase in zip(phrases_vectors,phrases):
        x=np.array(text_tf).flatten()[x]
        avg=np.mean(x)
        phrases_dict[phrase]=avg
    master_phrases_vectors.append(phrases_dict)

# ===================== vectorize the SOW =======================

sow_tf=tfidftransformer.transform([sow])[0]
sow_tf=sow_tf.todense()
phrases=use.noun_tokenize(sow)
phrases=list(set(phrases))
phrases_vectors=[list(tfidftransformer.transform([x])[0].indices) for x in phrases]
sow_phrase_dict = {}
for x, phrase in zip(phrases_vectors, phrases):
    x = np.array(sow_tf).flatten()[x]
    avg = np.mean(x)
    sow_phrase_dict[phrase] = avg

# ===================== find cosine similarities =======================

similarities=[]
for text_tf,phrase_dict in zip(texts_all_tf,master_phrases_vectors):
    sim_tf=cosine_similarity(text_tf,sow_tf)
    sim_tf=sim_tf.flatten()[0]
    sim_keyword=use.get_cosine(phrase_dict,sow_phrase_dict)
    sim=(labmbda*sim_tf)+((1-labmbda)*sim_keyword)
    similarities.append(sim)


# ===================== rank the documents and print the top n =======================

ranked_docs=list(reversed(np.argsort(similarities)))

for i in range(n_results):
    index=ranked_docs[i]
    print similarities[index]#,title_all[index]

