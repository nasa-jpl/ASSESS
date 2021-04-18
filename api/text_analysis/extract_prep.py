import json
import os
import pathlib
import subprocess
from collections import deque
import numpy as np
import dill
import pandas as pd
from elasticsearch import Elasticsearch
from elasticsearch.helpers import scan
from pandas.io.json import json_normalize
from sklearn.feature_extraction import text
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import normalize
from standard_extractor import find_standard_ref
from web_utils import connect_to_es

# Connect to Elasticsearch
es, idx_main, idx_log, idx_stats = connect_to_es()


def parse_text(filepath):
    if os.path.exists(filepath + "_parsed.txt"):
        # todo: remove this. Caches the parsed text.
        return str(open(filepath + "_parsed.txt", "r").read())

    bashCommand = "java -jar standards_extraction/lib/tika-app-1.16.jar -t " + filepath
    output = ""
    try:
        output = subprocess.check_output(["bash", "-c", bashCommand])
        file = open(filepath + "_parsed.txt", "wb")
        file.write(output)
        file.close()
    except subprocess.CalledProcessError as e:
        print(e.output)
    return str(output)


def transfrom(df):
    df = df[df["sdo.iso.type"] == "standard"].reset_index(drop=True)
    df.fillna("", inplace=True)
    tfidftransformer = TfidfVectorizer(
        ngram_range=(1, 1), stop_words=text.ENGLISH_STOP_WORDS
    )
    X = tfidftransformer.fit_transform(
        [m + " " + n for m, n in zip(df["description"], df["title"])]
    )
    X = normalize(X, norm="l2", axis=1)
    nbrs_brute = NearestNeighbors(
        n_neighbors=X.shape[0], algorithm="kd_tree", metric="cosine"
    )
    nbrs_brute.fit(X.todense())
    return tfidftransformer, X, nbrs_brute


def predict(file=None, in_text=None, size=10):
    """
    Predict recommendations given text or pdf file.
    Fields in the dataframe:
    ['id',
    'raw_id',
    'doc_number',
    'description',
    'status',
    'technical_committee',
    'text',
    'title',
    'published_date',
    'isbn',
    'url',
    'ingestion_date',
    'hash',
    'sdo.iso.code',
    'sdo.iso.field',
    'sdo.iso.group',
    'sdo.iso.subgroup',
    'sdo.iso.edition',
    'sdo.iso.number_of_pages',
    'sdo.iso.section_titles',
    'sdo.iso.sections',
    'sdo.iso.type',
    'sdo.iso.preview_url',
    'category.ics']
    """
    if file:
        if file.filename == "":
            return "No selected file!"
        new_text = parse_text(file.filename)

    else:
        # Get text from form
        new_text = in_text
        file = open("temp_text", "w")
        file.write(str(new_text.encode("utf-8", "ignore")))
        file.flush()
        file.close()
    res = list(scan(es, query={}, index=idx_main))
    output_all = deque()
    output_all.extend([x["_source"] for x in res])
    df = json_normalize(output_all)
    tfidftransformer, X, nbrs_brute = transfrom(df)

    standard_refs = find_standard_ref(new_text)
    result = {}
    result["embedded_references"] = standard_refs
    result["recommendations"] = []
    sow = tfidftransformer.transform([new_text])
    sow = normalize(sow, norm="l2", axis=1)

    # This is memory intensive.
    distances, indices = nbrs_brute.kneighbors(sow.todense())
    print(distances)
    distances = list(distances[0])
    indices = list(indices[0])

    for indx, dist in zip(indices[:size], distances[:size]):
        id = df.iloc[indx]["id"]
        result["recommendations"].append(
            {
                "sim": 100 * round(1 - dist, 21),
                "id": id,
            }
        )
        return result
