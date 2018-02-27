
from sklearn.neighbors import NearestNeighbors
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
import networkx as nx
import nltk
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
import utils as use

global unsup_method
unsup_method=''

# TODO: test with atleat one example

def unsup_train(dataset, dataset_name, vectorizer, data_fields=[], support_fields=[], unsup_meth=NearestNeighbors()):
    """trains an unsupervised model. Pickles the model and other necessary info related to data samples.


        Parameters
        ----------
        dataset : pandas dataframe

        dataset_name : string
            name of the dataset used for this experiment. Helps retrieve the relevant models.

        vectorizer : an implementation of vectorizer (with sklearn interface)

        data_fields : list
            list of the fields from which textual content is to be extracted

        support_fields : list
            list of fields that provide relevant info/IDs for each sample of data

        unsup_meth : sklearn unsupervised method or some an implementation with sklearn interface

    """

    global unsup_method

    if unsup_method=='':
        unsup_method=unsup_meth

    # ============ Extract data and support data. Create a view for just the support data. =============

    # dataset=pd.DataFrame()
    data_fields_view=dataset[data_fields]
    # merge all the data fields
    data=data_fields_view.apply(lambda x: ' '.join(x), axis=1)
    support_fields_view=dataset[support_fields]

    # ============ vectorize data =============

    vectors = vectorizer.fit_transform(data.values)

    # ============ train model =============

    model=unsup_meth.fit(vectors)

    # ============ save the model and support data =============

    use.savemodel(model,'model_'+dataset_name+'_'+str(vectorizer)+str(unsup_meth))
    use.savemodel(support_fields_view,'support_'+dataset_name+'_'+str(vectorizer)+str(unsup_meth))






def unsup_predict(textdata, dataset_name, vectorizer, unsup_meth=NearestNeighbors()):
    """predicts the nearest data samples from the model (to the given data sample) and
        relevant info about each sample.


            Parameters
            ----------
            textdata : String

            dataset_name : string
                name of the dataset used for this experiment. Helps retrieve the relevant models.

            vectorizer : an implementation of vectorizer (with sklearn interface)

            unsup_meth : sklearn unsupervised method or some an implementation with sklearn interface

            Returns
            ----------
            result : pandas dataframe

    """

    global unsup_method

    if unsup_method=='':
        unsup_method=unsup_meth

    # ============ vectorize data =============

    vector = vectorizer.fit_transform([textdata])[0]

    # ============ load the model and support data =============

    model=use.loadmodel('model_'+dataset_name+'_'+str(vectorizer)+str(unsup_meth))
    support_fields_view=use.loadmodel('support_'+dataset_name+'_'+str(vectorizer)+str(unsup_meth))


    # ============ predict the k nearest neighbours =============
    k_neighbours = model.predict(vector)

    # ============ extract/return/print view for the nearest neighbours from the support data =============
    results=support_fields_view[k_neighbours] # TODO : correct the syntax.
    return results



def vectorizer_tf_idf():
    vectorizer = TfidfVectorizer(ngram_range=(1, 2))
    return vectorizer


def vectorizer_methodology_used():
    """Implement your own"""
    vectorizer=''
    return vectorizer



