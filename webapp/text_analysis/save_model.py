from sklearn.metrics.pairwise import cosine_similarity
import networkx as nx
import nltk
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from text_analysis import utils as use


def build_cosine(texts_all, n=2):



    # ===================== create the model =======================
    tfidftransformer=TfidfVectorizer(ngram_range=(1,n))#,max_df=0.6)
    texts_all_tf=tfidftransformer.fit_transform(texts_all)
    # vocab_map = {v: k for k, v in tfidftransformer.vocabulary_.items()}


    # ===================== save the model =================
    use.savemodel(texts_all_tf,'texts_all_tf_new')
    use.savemodel(tfidftransformer,'tfidftransformer_new')


def predict_cosine(sow, n_results):


    # ===================== read the model =================

    texts_all_tf=use.loadmodel('texts_all_tf_new')
    tfidftransformer=use.loadmodel('tfidftransformer_new')

    vocab_map = {v: k for k, v in tfidftransformer.vocabulary_.items()}

    # ===================== read sow =======================

    sow=sow#.decode('utf-8')

    # ===================== vectorize the SOW =======================

    sow_tf=tfidftransformer.transform([sow])[0]
    sow_tf=sow_tf.todense()


    # ===================== find cosine similarities =======================

    similarities=[]
    all_important_terms_tf=[]
    for text_tf in texts_all_tf:
        sim_tf=cosine_similarity(text_tf,sow_tf)
        product=np.array(text_tf.todense()).flatten()*np.array(sow_tf).flatten()
        important_terms_tf=list(reversed(np.argsort(product)))[:10]
        important_terms_tf=[vocab_map[x] for x in important_terms_tf]
        all_important_terms_tf.append(important_terms_tf)
        sim_tf=sim_tf.flatten()[0]
        similarities.append(sim_tf)


    # ===================== rank the documents and print the top n =======================

    ranked_docs=list(reversed(np.argsort(similarities)))
    results_sim=[]
    results_index=[]
    for i in range(n_results):
        index=ranked_docs[i]
        # print similarities[index]
        results_sim.append(format(100*similarities[index],'.2f'))
        results_index.append(index)
        # print all_important_terms_tf[index]
        # print all_important_terms_keywords[index]

    return results_index, results_sim
