
# load all the standards
import pandas as pd
import os
import numpy as np
standards_dir = '../standards/data'
df=pd.read_csv(os.path.join(standards_dir,'iso_final_all_clean_standards_text_w_elmo.csv'),index_col=0)
df=df[df['type']=='standard'].reset_index(drop=True)
df.fillna('', inplace=True)


# # ======================================================================================================================
# ## Retrival based on full version of WMD-ELMO (slow)
# # ======================================================================================================================
#
# find elmo vectors for each token in the text
from webapp.text_analysis.utils.elmo import *
import tensorflow_hub as hub
import tensorflow.compat.v1 as tf
import copy


tf.disable_eager_execution()
elmo = hub.Module("https://tfhub.dev/google/elmo/2")

# find wmd between the sow and all standards in the library
text_sow=open('test_input_sow_text.txt','r').read()
text_sow_suffixed, wordvecs_sow=process_text_for_elmo_wmd(text_sow)
for indx, row in df.iterrows():
    text_standard=row['description']+' '+row['title']
    wordvecs_sow=copy.deepcopy(wordvecs_sow)
    text_standard_suffixed, wordvecs_standards=process_text_for_elmo_wmd(text_standard, suffix=1)
    if text_standard_suffixed==None:
        print('Could not create ELMO vectors for (skipping it):', text_standard)
        continue

    # merge the two word_vector lookup data structure
    wordvecs = {}
    for k, v in wordvecs_sow.items():
        wordvecs[k] = v
    for k, v in wordvecs_standards.items():
        wordvecs[k] = v

    # calculate distance
    prob = word_mover_distance_probspec(text_sow_suffixed, text_standard_suffixed, wordvecs)
    print(pulp.value(prob.objective))

# ======================================================================================================================
## Retrival based on 'averaged' version of ELMO (fast). Create a paragraph vector by squishing the ELMO token vectors.
# ======================================================================================================================
from sklearn.neighbors import NearestNeighbors
from webapp.text_analysis.utils.elmo import *
import ast
import dask.dataframe as dd
import multiprocessing

# remove the rows that do do have an elmo vector
df['elmo'].replace('', np.nan, inplace=True)
df.dropna(subset=['elmo'], inplace=True)
df=df.reset_index()

text_sow=open('test_input_sow_text.txt','r').read()
elmo_vec_sow=give_paragraph_elmo_vector(text_sow)
elmo_vec_sow=np.array([elmo_vec_sow])
print(elmo_vec_sow.shape)

df_=df['elmo']
df_=df_.reset_index()
ddf=dd.from_pandas(df_, npartitions=2*multiprocessing.cpu_count())
df['elmo']=ddf.elmo.map(lambda elmo: ast.literal_eval(elmo), meta=('elmo', object)).compute() # df['elmo'] = df.apply(lambda row: ast.literal_eval(row['elmo']) , axis=1)
X=np.array(list(df['elmo']))
print(X.shape)

nbrs_brute = NearestNeighbors(n_neighbors=len(df['title']), algorithm='brute')

print('fitting')
nbrs_brute.fit(X)

print('scoring standards')
distances, indices = nbrs_brute.kneighbors(elmo_vec_sow)
distances = list(distances[0])
indices = list(indices[0])

for indx, dist in zip(indices[:10],distances[:10]):
    title=df.iloc[indx]['title']
    description=df.iloc[indx]['description']
    link=df.iloc[indx]['link']
    standard_code = df.iloc[indx]['standard']
    print(dist, title, description)


# ======================================================================================================================
## Retrival based on Word2Vec and Glove vectors
# https://towardsdatascience.com/light-on-math-ml-intuitive-guide-to-understanding-glove-embeddings-b13b4f19c010 (difference between Glove and word2vec)
# https://machinelearningmastery.com/develop-word-embeddings-python-gensim/ (implementations)
# ======================================================================================================================
from sklearn.neighbors import NearestNeighbors
import dask.dataframe as dd
import multiprocessing
from webapp.text_analysis.utils.utils import *
from webapp.text_analysis.utils.word_vectors import *
import time

for model_type in ['w2v','glove']:

    text_sow=open('test_input_sow_text.txt','r').read()
    text_sow=clean_text(text_sow)
    w2_vec_sow=get_w2v_para(text_sow.split(), model_type=model_type)
    w2_vec_sow=np.array([w2_vec_sow])
    print(w2_vec_sow.shape)

    df=dd.from_pandas(df, npartitions=2*multiprocessing.cpu_count())
    df=df[df['type']=='standard'].reset_index(drop=True)
    df=df.fillna('')
    df=df.map_partitions(lambda df: df.assign(usable_text=df['description_clean'] +' ' + df['title'])).compute()
    # df=df.head(1000).reset_index()
    df_=df['usable_text']
    df_=df_.reset_index()
    ddf=dd.from_pandas(df_, npartitions=2*multiprocessing.cpu_count())
    start = time.process_time()
    df['w2v']=ddf.usable_text.map(lambda usable_text: get_w2v_para(usable_text, model_type=model_type), meta=('usable_text', str)).compute()
    print(time.process_time() - start)
    df['w2v'].replace('', np.nan, inplace=True)
    df.dropna(subset=['w2v'], inplace=True)
    df=df.reset_index(drop=True)
    X=np.array(list(df['w2v']))
    print(X.shape)
    nbrs_brute = NearestNeighbors(n_neighbors=len(df['title']), algorithm='brute')

    print('fitting')
    nbrs_brute.fit(X)

    print('scoring standards')
    distances, indices = nbrs_brute.kneighbors(w2_vec_sow)
    distances = list(distances[0])
    indices = list(indices[0])

    for indx, dist in zip(indices[:10],distances[:10]):
        title=df.iloc[indx]['title']
        description=df.iloc[indx]['description']
        link=df.iloc[indx]['link']
        standard_code = df.iloc[indx]['standard']
        print(dist, title, description)




"""
Observations and Todos:
-the sentence disambiguator (SD) may work badly with the format of the documents of certain SOWs. May need additional preprocessing!! Check it!
-cannot use the description_clean in this case, since it detects only a single sentence. Should we clean by first SDing it! 
then it may not be a well formed sentence, on which the ELMO is trained!
-speed of comparison is pretty bad with the full version!
--calculating elmo vectors for 30K paragraphs is taking too long even with Dask dataframes (~60hrs)
-create a test to compare elmo-wmd vs. cosine:
    -get three categories of standards for an ; bad ones + ones that are top 20 based on cosine; re-rank them based on elmo-wmd and compare the matching keywords as well
    -the above may help rank better the things that were retrieved based on "exact matches", but does not fully help us ascertain the capability
        of the model to retrieve suitable standards!
-to have retrieval based on the wmd-elmo, we can create a paragraph vector by squishing the elmo token vectors and get the top 20, then re-rank them based on the full version
    - we can also analyse what kind of affect the re-ranking has, to understand the comparison between fast and full versions of elmo-wmd
--we are extracting the elmo vectors one sentence at a time using the tenforflow hub, we can give all sentences at once (this will be faster), 
    then connecting the actual token to word vec may be a little more difficult
"""