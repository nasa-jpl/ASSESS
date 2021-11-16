from jpl.pipedreams.plugins_ops import PluginCollection
import pandas as pd
import datetime


def train_vectorizers(
    list_of_texts, type, vectorizers: PluginCollection, fresh=False, name=None
):
    if name is None:
        name = type
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


def train(index_types, vectorizer_types, list_of_texts):
    # ==== train vectorizers (needs to train on all standards in the corpus)
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
        # TODO: get ES IDs
        ES_ids = list(range(len(vectors)))  # using dummy values
        vector_storage.apply(
            "plugins.Vector_Storage",
            "basic",
            "add_update_vectors",
            {"ids": ES_ids, "vectors": vectors, "vec_type": vectorizer_type},
        )
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
    return vectorizers, vector_storage, vector_indexes


def predict(
    sow,
    n,
    vectorizers,
    vector_storage,
    vector_indexes,
    list_of_texts,
    vectorizer_types=["tf_idf"],
    index_types=["flat"],
):
    for vectorizer_type in vectorizer_types:
        begin = datetime.datetime.now()
        # vectorize
        vector = create_vectors([sow], type=vectorizer_type, vectorizers=vectorizers)[0]
        for index_type in index_types:
            # retrieve
            print("vectorizer_type:", vectorizer_type, "|| index_type:", index_type)
            top_n_idx = get_top_n(
                vector, n, type=index_type, indexes=vector_indexes[vectorizer_type]
            )
            # get the ES_ids
            top_n_ES_ids = vector_storage.apply(
                "plugins.Vector_Storage",
                "basic",
                "get_vector_Ids",
                {"vec_type": vectorizer_type, "vector_indexes": top_n_idx},
            )
            print(
                "|-->top_n_ES_ids:",
                top_n_ES_ids[:n],
                ", time taken:",
                datetime.datetime.now() - begin,
            )
            # TODO: retrieve results from ES, for now just use the dataframe
            iso_data = pd.read_feather("data/feather_text")
            for ES_id in top_n_ES_ids[:n]:
                print(ES_id, list_of_texts[ES_id])
    return


def get_list_of_text(df_file):
    df = pd.read_feather(df_file)
    # print(df.columns)
    return list(df["title"] + ". " + df["description"])


# TEST CODE:
if __name__ == "__main__":
    do_training = False
    index_types = ["flat", "flat_sklearn"]
    vectorizer_types = ["tf_idf"]
    df_file = "data/feather_text"
    list_of_texts = get_list_of_text(df_file)
    # list_of_texts=['computer science', 'space science', 'global summit for dummies', 'deep neural nets', 'technology consultants',
    #                'space science', 'global summit for dummies', 'deep neural nets', 'technology consultants',
    #                '', '', '', '']
    print("Number of Standards text to process:", len(list_of_texts))
    if do_training:
        vectorizers, vector_storage, vector_indexes = train(
            index_types, vectorizer_types, list_of_texts
        )
    else:
        vectorizers, vector_storage, vector_indexes = load_into_memory(
            index_types, vectorizer_types
        )
    # ==== retrieve
    print("\nRetrieving results...")
    predict(
        "Computer software and stuff!!!",
        10,
        vectorizers,
        vector_storage,
        vector_indexes,
        list_of_texts,
    )


"""
The flow for CRUD operations:
    - need to add new standards:
        - update the metadata into ES and get the ES-ids
        - create multiple types of vectors for the texts
        - add the ES-id:vector to the vector storage
        - recreate all indexes
    - update vectors for a standards:
        - get the ES-ids
        - create multiple types of vectors for the texts
        - add the ES-id:vector to the vector storage
        - recreate all indexes
    - remove standards:
        - remove the standards from the ES and get their ES-ids
        - remove the ES-id:vector from the vector storage
        - recreate all indexes

Known issues:
    -Faiss flat index is giving a higher matching values to vectors for empty strings than some more relevant ones!
        - currently we are circumventing it by adding an extra dummy token to each text
"""
