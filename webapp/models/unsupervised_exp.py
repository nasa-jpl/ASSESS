
from sklearn.neighbors import NearestNeighbors
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
import networkx as nx
import nltk
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
import utils as use
import os

global unsup_method
unsup_method=''
modeldir='trained_models'

def train(dataset, dataset_name, vectorizer, data_fields=[], support_fields=[], unsup_meth=NearestNeighbors(), force_train=False):
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

        force_train : if 'True' then it trains the model even if a model is available, and replaces the old model with the new one

    """

    # check if the model is already available
    def collect(row):
        res=''
        for field in data_fields:
            res+=' '+str(row[field])
        return res

    ifmodel=os.path.exists(modeldir+'/'+'model_'+dataset_name+'_'+str(vectorizer)+str(unsup_meth))

    if not ifmodel or force_train:

        global unsup_method

        if unsup_method=='':
            unsup_method=unsup_meth

        # ============ Extract data and support data. Create a view for just the support data. =============

        # dataset=pd.DataFrame()
        data_fields_view=dataset[data_fields]
        # merge all the data fields
        data=data_fields_view.apply(collect, axis=1)
        support_fields_view=dataset[support_fields]

        # ============ vectorize data =============


        vectors = vectorizer.fit_transform(data.values)

        # ============ train model =============

        model=unsup_meth.fit(vectors)

        # ============ save the model and support data =============

        use.savemodel(model,modeldir+'/'+'model_'+dataset_name+'_'+str(vectorizer).split('(')[0]+str(unsup_meth).split('(')[0])
        use.savemodel(support_fields_view,modeldir+'/'+'support_'+dataset_name+'_'+str(vectorizer).split('(')[0]+str(unsup_meth).split('(')[0])






def predict(textdata, dataset_name, vectorizer, unsup_meth=NearestNeighbors()):
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

    vector = vectorizer.transform([textdata])[0]

    # ============ load the model and support data =============

    model=use.loadmodel(modeldir+'/'+'model_'+dataset_name+'_'+str(vectorizer).split('(')[0]+str(unsup_meth).split('(')[0])
    support_fields_view=use.loadmodel(modeldir+'/'+'support_'+dataset_name+'_'+str(vectorizer).split('(')[0]+str(unsup_meth).split('(')[0])

    # ============ predict the k nearest neighbours =============
    distances, indices = model.kneighbors(vector)
    # ============ extract/return/print view for the nearest neighbours from the support data =============
    results=support_fields_view.ix[indices[0]]
    results['dist']=distances[0]
    results=results.sort_values(by=['dist'],ascending=False)
    return results



# Follow sklearn interface. Must have the two methods.
class Vectorizer_methodology_used():

    """Implement your own"""



    def fit_transform(self, raw_documents, y=None):
        """Learn vocabulary and idf, return term-document matrix.

        This is equivalent to fit followed by transform, but more efficiently
        implemented.

        Parameters
        ----------
        raw_documents : iterable
            an iterable which yields either str, unicode or file objects

        Returns
        -------
        X : sparse matrix, [n_samples, n_features]
            Tf-idf-weighted document-term matrix.
        """

        pass


    def transform(self, raw_documents, copy=True):
        """Transform documents to document-term matrix.

        Uses the vocabulary and document frequencies (df) learned by fit (or
        fit_transform).

        Parameters
        ----------
        raw_documents : iterable
            an iterable which yields either str, unicode or file objects

        copy : boolean, default True
            Whether to copy X and operate on the copy or perform in-place
            operations.

        Returns
        -------
        X : sparse matrix, [n_samples, n_features]
            Tf-idf-weighted document-term matrix.
        """


# usage example

# df=pd.read_csv('../standards/IEEE-standards_rev1.csv',index_col=0)
#
# vectorizer_tf_idf = TfidfVectorizer(ngram_range=(1, 2))
#
# train(df,'data_test_1',vectorizer_tf_idf,['abstract_new','purpose_new','scope_new'],['Publication Title','Category'])
#
# sample='The use of traffic scheduling and per-stream filtering and policing to support cyclic queuing and forwarding are described in this amendment to IEEE Std 802.1Q-2014.'
#
# results=predict(sample,'data_test_1',vectorizer_tf_idf)
# results.style