import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import os
import utils as use
import csv
import sys

# Calculate tf-idf for n-grams (provide as argument). Find cosine similarity. Rank the documents based on cosine similarity.
# Use keywords (provide as an option). Extract and score keywords. Use them with some labmda importance over the n-gram scores.

def system1(n,sowpath,labmbda,n_results,retrain):

    model_flag=0


    # ===================== read the model =================
    master_phrases_vectors=''
    texts_all_tf=''
    title_all=''
    tfidftransformer=''

    if os.path.exists('master_phrases_vectors_1') and not retrain:
        model_flag=1
        master_phrases_vectors=use.loadmodel('master_phrases_vectors_1')
        texts_all_tf=use.loadmodel('texts_all_tf_1')
        title_all=use.loadmodel('title_all_1')
        tfidftransformer=use.loadmodel('tfidftransformer_1')

    if model_flag==0 or retrain:
        # ===================== read standards =======================
        texts_all = []
        title_all = []
        with open('IEEE-standards.csv') as csvDataFile:
            csvReader = csv.reader(csvDataFile)
            counter=0
            for row in csvReader:
                if counter==0 or counter==1:
                    counter+=1
                    continue
                texts_all.append(unicode(row[10], errors='ignore'))
                title_all.append(unicode(row[0], errors='ignore'))



        # ===================== create the model =======================
        tfidftransformer=TfidfVectorizer(ngram_range=(1,n))#,max_df=0.6)
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


        # ===================== save the model =================

        use.savemodel(master_phrases_vectors,'master_phrases_vectors_1')
        use.savemodel(texts_all_tf,'texts_all_tf_1')
        use.savemodel(title_all,'title_all_1')
        use.savemodel(tfidftransformer,'tfidftransformer_1')


    # ===================== read sow =======================

    sow=open(sowpath,'r').read().decode('utf-8')

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
    all_important_terms_tf=[]
    all_important_terms_keywords=[]
    for text_tf,phrase_dict in zip(texts_all_tf,master_phrases_vectors):
        sim_tf=cosine_similarity(text_tf,sow_tf)
        product=np.array(text_tf.todense()).flatten()*np.array(sow_tf).flatten()
        important_terms_tf=list(reversed(np.argsort(product)))[:10]
        important_terms_tf=[vocab_map[x] for x in important_terms_tf]
        all_important_terms_tf.append(important_terms_tf)
        sim_tf=sim_tf.flatten()[0]
        sim_keyword,product_keyword=use.get_cosine(phrase_dict,sow_phrase_dict)
        keys=product_keyword.keys()
        values=product_keyword.values()
        important_terms_keyword = list(reversed(np.argsort(values)))
        important_terms_keyword=[keys[x] for x in important_terms_keyword]
        all_important_terms_keywords.append(important_terms_keyword)
        sim=(labmbda*sim_tf)+((1-labmbda)*sim_keyword)
        similarities.append(sim)


    # ===================== rank the documents and print the top n =======================

    ranked_docs=list(reversed(np.argsort(similarities)))

    for i in range(n_results):
        index=ranked_docs[i]
        print similarities[index],title_all[index]
        print all_important_terms_tf[index]
        print all_important_terms_keywords[index]


if __name__ == "__main__":
    n_gram = 2
    sowpath = 'sow_test'
    labmbda = 1
    n_results = 10
    retrain=True

    # sowpath=sys.argv[1]
    # n_gram=sys.argv[2]
    # labmbda=sys.argv[3]
    # n_results=sys.argv[4]
    # retrain=sys.argv[5]

    system1(n_gram,sowpath,labmbda,n_results,retrain)
