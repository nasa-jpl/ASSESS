from sklearn.metrics.pairwise import cosine_similarity
import networkx as nx
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from text_analysis import utils as use
from sklearn.neighbors import NearestNeighbors
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import normalize
import gc
import os

model_dir=os.path.join('models','trained_models')


def build_cosine(texts_all, n=1, force=False):
    global model
    if force or not os.path.exists(os.path.join(model_dir,'cosine_model')):
        tfidftransformer=TfidfVectorizer(ngram_range=(1,n))
        X=tfidftransformer.fit_transform(texts_all)
        nbrs_brute = NearestNeighbors(n_neighbors=X.shape[0], algorithm='brute', metric='cosine')
        print('fitting cosine')
        nbrs_brute.fit(X.todense())
        print('fitted cosine')

        model={}
        print('saving cosine model')
        model['tfidftransformer']=tfidftransformer
        model['nbrs_brute']=nbrs_brute
        # use.savemodel(model, os.path.join(model_dir,'cosine_model'))
        print('cosine model saved')
        del(X)
        gc.collect()
        return

def predict_cosine(sow, n_results):
    global model
    print('loading cosine_ model')
    # model=use.loadmodel(os.path.join(model_dir, 'cosine_model'))
    tfidftransformer=model['tfidftransformer']
    nbrs_brute=model['nbrs_brute']
    print('loaded cosine model')

    sow=tfidftransformer.transform([sow])
    distances, indices=nbrs_brute.kneighbors(sow.todense())

    return indices[0][:n_results], distances[0][:n_results] # todo : verify this logic of getting the first thing in the array
