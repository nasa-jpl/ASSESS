import ast
import multiprocessing

import dask.dataframe as dd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import normalize

from webapp.text_analysis.utils.word_vectors import *
from webapp.text_analysis.utils.utils import *
from sklearn.feature_extraction import text
from webapp.text_analysis.utils.soft_cosine import *
import datetime

from webapp.text_analysis.utils.elmo import *
import tensorflow_hub as hub
import tensorflow.compat.v1 as tf
import copy
import pandas as pd


def get_similar_standards(input_text, standards_df, algo='cosine-sim', id_column='id'):
    # todo: provide an option for choosing between wmd and soft-cosine

    """
    algo: cosine-sim, elmo-sim, glove-sim, w2v-sim, emlo-wmd-sim, w2v-wmd-sim, glove-wmd-sim
    Note: make sure there is no resetting of indexes or removal of values in this function from the standards_df!
    """

    standards_df=standards_df.copy()

    feature_importances=[]
    if 'wmd' not in algo:
        if algo=='elmo-sim':
            # add zero rows to the rows that do not have an elmo vector. todo: Is this a good idea!

            vec_sow = give_paragraph_elmo_vector(input_text)
            vec_sow = np.array([vec_sow])
            standards_df['elmo'] = standards_df['elmo'].replace('', str([0.0] * 1024))
            df_ = standards_df['elmo']
            df_ = df_.reset_index()
            ddf = dd.from_pandas(df_, npartitions=2 * multiprocessing.cpu_count())
            standards_df['elmo'] = ddf.elmo.map(lambda elmo: ast.literal_eval(elmo), meta=(
                'elmo', object)).compute()  # df['elmo'] = df.apply(lambda row: ast.literal_eval(row['elmo']) , axis=1)
            X = np.array(list(standards_df['elmo']))

        elif algo=='glove-sim':
            input_text = clean_text(input_text)
            vec_sow = get_w2v_para(input_text.split(), model_type='glove')
            vec_sow = np.array([vec_sow])

            df = dd.from_pandas(standards_df, npartitions=2 * multiprocessing.cpu_count())
            df = df.map_partitions(lambda df: df.assign(usable_text=df['description_clean'] + ' ' + df['title'])).compute()
            df_ = df['usable_text']
            df_ = df_.reset_index()
            ddf = dd.from_pandas(df_, npartitions=2 * multiprocessing.cpu_count())
            standards_df['glove'] = ddf.usable_text.map(lambda usable_text: get_w2v_para(usable_text, model_type='glove'),
                                            meta=('usable_text', str)).compute()

            # df['w2v'].replace('', np.nan, inplace=True)
            # df.dropna(subset=['w2v'], inplace=True)
            # df = df.reset_index(drop=True)

            X = np.array(list(standards_df['glove']))

        elif algo=='w2v-sim':
            text_sow = clean_text(input_text)
            vec_sow = get_w2v_para(text_sow.split(), model_type='w2v')
            vec_sow = np.array([vec_sow])

            df = dd.from_pandas(standards_df, npartitions=2 * multiprocessing.cpu_count())
            df = df.map_partitions(lambda df: df.assign(usable_text=df['description_clean'] + ' ' + df['title'])).compute()
            df_ = df['usable_text']
            df_ = df_.reset_index()
            ddf = dd.from_pandas(df_, npartitions=2 * multiprocessing.cpu_count())
            standards_df['w2v'] = ddf.usable_text.map(lambda usable_text: get_w2v_para(usable_text, model_type='w2v'),
                                            meta=('usable_text', str)).compute()
            # df['w2v'].replace('', np.nan, inplace=True)
            # df.dropna(subset=['w2v'], inplace=True)
            # df = df.reset_index(drop=True)

            X = np.array(list(standards_df['w2v']))

        elif algo=='cosine-sim':
            tfidftransformer = TfidfVectorizer(ngram_range=(1, 1), stop_words=text.ENGLISH_STOP_WORDS)
            df = dd.from_pandas(standards_df, npartitions=2 * multiprocessing.cpu_count())
            df = df.map_partitions(lambda df: df.assign(usable_text=df['description_clean'] + ' ' + df['title'])).compute()
            X_text = list(df['usable_text'])
            X = tfidftransformer.fit_transform(X_text)
            vec_sow = tfidftransformer.transform([input_text])
        else:
            print("No Such Algorithm:", algo)
            raise NotImplementedError

        print('standards data shape', X.shape)
        nbrs_brute = NearestNeighbors(n_neighbors=len(standards_df['title']), algorithm='brute', metric='cosine')

        print('fitting standards')
        nbrs_brute.fit(X)

        print('scoring standards')
        sorted_distances, sorted_indices = nbrs_brute.kneighbors(vec_sow)
        standards_df_sorted=standards_df.reindex(sorted_indices[0])

        sorted_distances = list(sorted_distances[0])
        sorted_ids = list(standards_df_sorted[id_column])
    else:
        start=datetime.datetime.now()
        if algo == 'elmo-wmd-sim':
            input_text_tokens, vec_sow = process_text_for_elmo_wmd(input_text)
        elif algo in ['w2v-wmd-sim', 'glove-wmd-sim']:
            input_text_tokens, vec_sow = get_w2v(input_text.split(), model_type='w2v')
        else:
            print("No Such Algorithm:", algo)
            raise NotImplementedError

        # print('input processed in:', datetime.datetime.now()-start)

        distances_collect = []

        # calculate new distances
        for indx, row in standards_df.iterrows():
            print(indx)
            text_standard = row['description'] + ' ' + row['title']
            vec_sow = copy.deepcopy(vec_sow)

            if algo == 'elmo-wmd-sim':
                standard_text_tokens, vec_standard = process_text_for_elmo_wmd(text_standard, suffix=1)
                if standard_text_tokens == None:
                    distances_collect.append(0.99)
                    print('Could not create ELMO vectors for:', text_standard)
                    continue
            elif algo in ['w2v-wmd-sim', 'glove-wmd-sim']:
                standard_text_tokens, vec_standard = get_w2v(text_standard.split(), model_type=algo.split('-')[0])
            else:
                print("No Such Algorithm:", algo)
                raise NotImplementedError

            # print('standards processed in:', datetime.datetime.now() - start)

            # prob = word_mover_distance_probspec_mod(input_text_tokens, standard_text_tokens, vec_sow,vec_standard)
            # distances_collect.append(pulp.value(prob.objective))
            # matches = {}
            # for v in prob.variables():
            #     if v.varValue != 0:
            #         # print(v.name, '=', v.varValue)
            #         matches[str(v.name)[8:]] = v.varValue
            # matches = {k: v for k, v in sorted(matches.items(), key=lambda item: item[1])}
            # feature_importances.append(matches)

            sim = soft_cosine(input_text_tokens, standard_text_tokens, vec_sow, vec_standard)
            distances_collect.append(1.0-sim)

        sorted_distances = []
        sorted_indices = []
        for index, distance in sorted(enumerate(distances_collect), key=lambda pair: pair[1]):
            sorted_distances.append(distance)
            sorted_indices.append(index)

        standards_df_sorted = standards_df.reindex(sorted_indices)

        sorted_distances = list(sorted_distances)
        sorted_ids = list(standards_df_sorted[id_column])



    # for indx, dist in zip(indices[:result_count], distances[:result_count]):
    #     title = df.iloc[indx]['title']
    #     description = df.iloc[indx]['description']
    #     link = df.iloc[indx]['link']
    #     standard_code = df.iloc[indx]['standard']
    #     print(dist, title, description)

    return sorted_ids, sorted_distances, feature_importances, vec_sow




def get_paragraph_vectors(standards_df, vec='elmo'):

    """
    vec: elmo, glove, w2v
    """

    standards_df=standards_df.copy()

    if vec=='elmo':
            # add zero rows to the rows that do not have an elmo vector. todo: Is this a good idea!
            standards_df['elmo'] = standards_df['elmo'].replace('', str([0.0] * 1024))
            df_ = standards_df['elmo']
            df_ = df_.reset_index()
            ddf = dd.from_pandas(df_, npartitions=2 * multiprocessing.cpu_count())
            standards_df['elmo'] = ddf.elmo.map(lambda elmo: ast.literal_eval(elmo), meta=(
                'elmo', object)).compute()  # df['elmo'] = df.apply(lambda row: ast.literal_eval(row['elmo']) , axis=1)

    elif vec=='glove':

            df = dd.from_pandas(standards_df, npartitions=2 * multiprocessing.cpu_count())
            df = df.map_partitions(lambda df: df.assign(usable_text=df['description_clean'] + ' ' + df['title'])).compute()
            df_ = df['usable_text']
            df_ = df_.reset_index()
            ddf = dd.from_pandas(df_, npartitions=2 * multiprocessing.cpu_count())
            standards_df['glove'] = ddf.usable_text.map(lambda usable_text: get_w2v_para(usable_text, model_type='glove'),
                                            meta=('usable_text', str)).compute()



    elif vec=='w2v':

            df = dd.from_pandas(standards_df, npartitions=2 * multiprocessing.cpu_count())
            df = df.map_partitions(lambda df: df.assign(usable_text=df['description_clean'] + ' ' + df['title'])).compute()
            df_ = df['usable_text']
            df_ = df_.reset_index()
            ddf = dd.from_pandas(df_, npartitions=2 * multiprocessing.cpu_count())
            standards_df['w2v'] = ddf.usable_text.map(lambda usable_text: get_w2v_para(usable_text, model_type='w2v'),
                                            meta=('usable_text', str)).compute()


    else:
        print("No Such Algorithm:", vec)
        raise NotImplementedError



    return standards_df