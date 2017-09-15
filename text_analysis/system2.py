import networkx as nx
import nltk
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
import sys
import utils as use
import os
import csv


# Calculate the 1-gram scores based on TRS (technique-4). Find the cosine similarity and rank documents.
# Use keywords (provide as an option). Extract and score keywords. Use them with some labmda importance over the n-gram scores.


def ne_rank(text_tf_1,text_tf_2,tfidftransformer_1,vocab_map_1,vocab_map_2):
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

def system2(sowpath,labmbda,n_results,retrain):

    model_flag=0

    # ===================== read the model =================
    master_phrases_vectors = ''
    title_all = ''
    tfidftransformer_1 = ''
    tfidftransformer_2 = ''
    master_nerank_vectors=''

    if os.path.exists('master_phrases_vectors_2') and not retrain:
        model_flag = 1
        master_phrases_vectors = use.loadmodel('master_phrases_vectors_2')
        title_all = use.loadmodel('title_all_2')
        tfidftransformer_1 = use.loadmodel('tfidftransformer_1_2')
        tfidftransformer_2 = use.loadmodel('tfidftransformer_2_2')
        master_nerank_vectors=use.loadmodel('master_nerank_vectors_2')


    if model_flag == 0 or retrain:


        # ===================== read standards =======================
        texts_all = []
        title_all = []
        with open('IEEE-standards.csv') as csvDataFile:
            csvReader = csv.reader(csvDataFile)
            counter = 0
            for row in csvReader:
                if counter == 0 or counter==1:
                    counter += 1
                    continue
                texts_all.append(unicode(row[10], errors='ignore'))
                title_all.append(unicode(row[0], errors='ignore'))



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
        title_all_new=[]

        for title,text,text_tf_1,text_tf_2 in zip(title_all,texts_all,texts_all_tf_1,texts_all_tf_2):

            # put a check for no text. see that the titles are aligned
            if len(text_tf_1.indices)==0 or len(text_tf_2.indices)==0:
                continue

            final_vec=ne_rank(text_tf_1,text_tf_2,tfidftransformer_1,vocab_map_1,vocab_map_2)
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
            title_all_new.append(title)

        title_all=title_all_new

        # ===================== save the model =================

        use.savemodel(master_phrases_vectors, 'master_phrases_vectors_2')
        use.savemodel(title_all, 'title_all_2')
        use.savemodel(tfidftransformer_1,'tfidftransformer_1_2')
        use.savemodel(tfidftransformer_2,'tfidftransformer_2_2')
        use.savemodel(master_nerank_vectors,'master_nerank_vectors_2')

    # ===================== read sow =======================

    sow = open(sowpath, 'r').read().decode('utf-8')


    # ===================== vectorize the SOW =======================

    sow_tf1=tfidftransformer_1.transform([sow])[0]
    sow_tf2=tfidftransformer_2.transform([sow])[0]

    sow_final_vec=ne_rank(sow_tf1,sow_tf2,tfidftransformer_1,vocab_map_1,vocab_map_2)

    phrases=use.noun_tokenize(sow)
    phrases=list(set(phrases))
    phrases_vectors=[list(tfidftransformer_1.transform([x])[0].indices) for x in phrases]
    sow_phrase_dict = {}
    for x, phrase in zip(phrases_vectors, phrases):
        x = [sow_final_vec[y] for y in x if y in sow_final_vec.keys()]
        avg = np.sum(x)
        sow_phrase_dict[phrase] = avg


    # ===================== find cosine similarities =======================

    similarities=[]
    all_important_terms_tf=[]
    all_important_terms_keywords=[]
    for nerank_vec,phrase_dict in zip(master_nerank_vectors,master_phrases_vectors):
        sim_nerank,product_tf=use.get_cosine(nerank_vec,sow_final_vec)
        keys = product_tf.keys()
        values = product_tf.values()
        important_terms_tf = list(reversed(np.argsort(values)))
        important_terms_tf = [vocab_map_1[keys[x]] for x in important_terms_tf]
        all_important_terms_tf.append(important_terms_tf)

        sim_keyword,product_keyword=use.get_cosine(phrase_dict,sow_phrase_dict)
        keys = product_keyword.keys()
        values = product_keyword.values()
        important_terms_keyword = list(reversed(np.argsort(values)))
        important_terms_keyword = [keys[x] for x in important_terms_keyword]
        all_important_terms_keywords.append(important_terms_keyword)

        sim=(labmbda*sim_nerank)+((1-labmbda)*sim_keyword)
        similarities.append(sim)


    # ===================== rank the documents and print the top n =======================

    ranked_docs=list(reversed(np.argsort(similarities)))

    for i in range(n_results):
        index=ranked_docs[i]
        print similarities[index] ,title_all[index]
        print all_important_terms_tf[index]
        print all_important_terms_keywords[index]


if __name__ == "__main__":
    sowpath = 'sow_test'
    labmbda = .5
    n_results = 10
    retrain=True

    # sowpath = sys.argv[1]
    # labmbda = sys.argv[2]
    # n_results = sys.argv[3]
    # retrain = sys.argv[4]

    system2(sowpath, labmbda, n_results,retrain)
