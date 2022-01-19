from jpl.pipedreams.plugins_ops import PluginCollection
import pandas as pd
import datetime
from pandas.io.json import json_normalize
from collections import deque
from elasticsearch import Elasticsearch
from elasticsearch.helpers import scan, bulk


def train_vectorizers(
    list_of_texts, type, vectorizers: PluginCollection, fresh=False, name=None
):
    if name is None:
        name = type
    # Add path for mounted drive.
    name = "./data/" + name
    model_exists = vectorizers.apply(
        "plugins.Vectorizer", type, "exists_on_disk", {"target_path": name}
    )
    if fresh or not model_exists:
        vectorizers.apply(
            "plugins.Vectorizer", type, "train", {"list_of_texts": list_of_texts}
        )
        vectorizers.apply(
            "plugins.Vectorizer", type, "save_to_disk", {"target_path": name}
        )
    vectorizers.apply(
        "plugins.Vectorizer", type, "load_from_disk", {"target_path": name}
    )


def create_vectors(list_of_texts, type, vectorizers: PluginCollection):
    vectors = vectorizers.apply(
        "plugins.Vectorizer", type, "vectorize", {"list_of_texts": list_of_texts}
    )
    return vectors


def create_indexes(vectors, type, indexes: PluginCollection, fresh=False, name=None):
    if name is None:
        name = type
    # Add path for mounted drive.
    name = "./data/" + name
    model_exists = indexes.apply(
        "plugins.Index", type, "exists_on_disk", {"target_path": name}
    )
    if fresh or not model_exists:
        indexes.apply("plugins.Index", type, "create_index", {"vectors": vectors})
        indexes.apply("plugins.Index", type, "save_to_disk", {"target_path": name})
    indexes.apply("plugins.Index", type, "load_from_disk", {"target_path": name})


def get_top_n(target_vector, n, type, indexes: PluginCollection):
    top_n = indexes.apply(
        "plugins.Index", type, "get_top_n", {"target_vector": target_vector, "n": n}
    )
    return top_n


def load_into_memory(index_types, vectorizer_types):
    # ==== load vectorizers from disk
    vectorizers = PluginCollection()
    print("\nLoading Vectorizers...")
    for vectorizer_type in vectorizer_types:
        print("vectorizer_type:", vectorizer_type)
        train_vectorizers(
            [], type=vectorizer_type, vectorizers=vectorizers, fresh=False
        )

    # ==== Init Vector Storage from disk (will load from disk automatically when it is called the first time)
    vector_storage = PluginCollection()
    print("\nInitialized the Vector Storage.")

    # ==== load indexes from disk
    vector_indexes = {}
    print("\nLoading Indexes...")
    for vectorizer_type in vectorizer_types:
        indexes = PluginCollection()
        for index_type in index_types:
            print("vectorizer_type:", vectorizer_type, "|| index_type:", index_type)
            create_indexes(
                [],
                type=index_type,
                indexes=indexes,
                name=vectorizer_type + "_" + index_type,
                fresh=False,
            )
        vector_indexes[vectorizer_type] = indexes
    return vectorizers, vector_storage, vector_indexes


def train(es, index_types, vectorizer_types):
    # ==== train vectorizers (needs to train on all standards in the corpus)
    ES_ids, list_of_texts = get_list_of_text(es)
    vectorizers = PluginCollection()
    print("\nTraining Vectorizers...")
    for vectorizer_type in vectorizer_types:
        print("vectorizer_type:", vectorizer_type)
        train_vectorizers(list_of_texts, type=vectorizer_type, vectorizers=vectorizers)

    # ==== create vectors and update Vector Storage
    print("\nCreating Vectors...")
    vector_storage = PluginCollection()
    for vectorizer_type in vectorizer_types:
        print("vectorizer_type:", vectorizer_type)
        vectors = create_vectors(
            list_of_texts, type=vectorizer_type, vectorizers=vectorizers
        )
        # TODO: remove line
        # ES_ids = list(range(len(vectors)))  # using dummy values
        vector_storage.apply(
            "plugins.Vector_Storage",
            "basic",
            "add_update_vectors",
            # TODO: Pass as a list of ES_ids
            {"ids": ES_ids, "vectors": vectors, "vec_type": vectorizer_type},
        )

    # ==== create indexes (one or many kind for each vectorizer i.e. type of vector)
    vector_indexes = {}
    print("\nCreating Indexes...")
    for vectorizer_type in vectorizer_types:
        vectors, _ = vector_storage.apply(
            "plugins.Vector_Storage",
            "basic",
            "get_all_vectors",
            {"vec_type": vectorizer_type},
        )
        indexes = PluginCollection()
        for index_type in index_types:
            print("vectorizer_type:", vectorizer_type, "|| index_type:", index_type)
            create_indexes(
                vectors,
                type=index_type,
                indexes=indexes,
                name=vectorizer_type + "_" + index_type,
            )
        vector_indexes[vectorizer_type] = indexes
    return


def predict(
    sow,
    n,
    start_from,
    vectorizers,
    vector_storage,
    vector_indexes,
    list_of_texts,
    vectorizer_types,
    index_types,
):
    for vectorizer_type in vectorizer_types:
        begin = datetime.datetime.now()
        # vectorize
        vector = create_vectors([sow], type=vectorizer_type, vectorizers=vectorizers)[0]
        for index_type in index_types:
            # retrieve
            print("vectorizer_type:", vectorizer_type, "|| index_type:", index_type)
            top_n_idx, scores = get_top_n(
                vector, n, type=index_type, indexes=vector_indexes[vectorizer_type]
            )
            # get the ES_ids
            top_n_ES_ids = vector_storage.apply(
                "plugins.Vector_Storage",
                "basic",
                "get_vector_Ids",
                {"vec_type": vectorizer_type, "vector_indexes": top_n_idx},
            )
            # print(
            #     "|-->top_n_ES_ids:",
            #     top_n_ES_ids[:n],
            #     ", time taken:",
            #     datetime.datetime.now() - begin,
            # )
            # TODO: retrieve results from ES, for now just use the dataframe
            # iso_data = pd.read_feather("data/feather_text")
            # for ES_id in top_n_ES_ids[:n]:
            #     print(ES_id, list_of_texts[ES_id])
    return top_n_ES_ids[start_from:n], scores.tolist()


def get_list_of_text(es=None):
    # df = pd.read_feather("data/feather_text")
    df = es_to_df(es)
    print(df)
    # print(df.columns)
    # TODO: get this information from the text column.
    # return the text and the elasticsearch ids
    return list(df["_id"]), list(df["title"] + ". " + df["description"])


def es_to_df(es=None, index="assess_remap", path="data/feather_text"):
    if not es:
        # ADD FILES YOU WANT TO READ HERE:
        df = pd.read_feather("data/feather_text")
    else:
        res = list(scan(es, query={}, index=index))
        output_all = deque()
        output_all.extend([((x["_source"]['description']), (x["_source"]['title']), (x["_id"])) for x in res])
        output_all = [{'description': t[0], 'title': t[1], '_id': t[2]} for t in output_all]
        df = json_normalize(output_all)
        df = df[["_id", "title", "description"]]
    return df


if __name__ == "__main__":
    es = Elasticsearch(http_compress=True)
    #es = None
    do_training = True
    index_types = ["flat", "flat_sklearn"]
    vectorizer_types = ["tf_idf"]
    ES_ids, list_of_texts = get_list_of_text(es)
    # list_of_texts=['computer science', 'space science', 'global summit for dummies', 'deep neural nets', 'technology consultants',
    #                'space science', 'global summit for dummies', 'deep neural nets', 'technology consultants',
    #                '', '', '', '']
    print("Number of Standards text to process:", len(list_of_texts))
    if do_training:
        train(es, index_types, vectorizer_types)
    else:
        vectorizers, vector_storage, vector_indexes = load_into_memory(
            index_types, vectorizer_types
        )
        # ==== retrieve
        print("\nRetrieving results...")
        r = predict(
            "Computer software and stuff!!!",
            10,
            0,
            vectorizers,
            vector_storage,
            vector_indexes,
            list_of_texts,
            vectorizer_types,
            index_types,
        )
        print(r)