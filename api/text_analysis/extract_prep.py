import os
import json
import subprocess
from sklearn.neighbors import NearestNeighbors
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import normalize
import dill
import pandas as pd
from sklearn.feature_extraction import text
from standard_extractor import find_standard_ref
import pathlib
from elasticsearch import Elasticsearch
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


def predict(file=None, in_text=None):
    dirPath = str(pathlib.Path(__file__).parent.absolute())

    standards_dir = dirPath + "/../standards/data"
    json_output_dir = "output"
    models_dir = "models"

    res = es.search(index=idx_main, body={"query": {"match_all": {}}})
    print(res)
    # TODO: Fix this line
    # df = pd.concat(map(pd.DataFrame.from_dict, res), axis=1)
    df = pd.read_csv(
        os.path.join(standards_dir, "iso_final_all_clean_text.csv"), index_col=0
    )
    # print(df2)
    df = df[df["type"] == "standard"].reset_index(drop=True)
    df.fillna("", inplace=True)

    tfidftransformer = TfidfVectorizer(
        ngram_range=(1, 1), stop_words=text.ENGLISH_STOP_WORDS
    )
    X = tfidftransformer.fit_transform(
        [m + " " + n for m, n in zip(df["description_clean"], df["title"])]
    )  # using both desc and tile to predict
    # tfidftransformer = TfidfVectorizer(ngram_range=(1,1))
    # X = tfidftransformer.fit_transform([m+' '+n for m, n in zip(df['description'], df['title'])]) # using both desc and tile to predict
    print("shape", X.shape)
    X = normalize(X, norm="l2", axis=1)
    nbrs_brute = NearestNeighbors(
        n_neighbors=X.shape[0], algorithm="brute", metric="cosine"
    )
    print("fitting")
    nbrs_brute.fit(X.todense())
    print("fitted")

    # How do we get request.file
    new_text = ""
    # ======================== find the referenced standards
    filename = "temp_text"
    # check if the post request has the file part
    if file:
        print("made it to the PDF part")
        # INSERT FILES OBJECT HERE
        # file = files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == "":
            return "no selected file!"
            # return redirect(request.url)
        if file:
            filename = file.filename
            ### Save the file
            new_text = parse_text(filename)
            print("parsed")
    else:
        # get text from form
        new_text = in_text
        file = open(filename, "w")
        file.write(str(new_text.encode("utf-8", "ignore")))
        file.flush()
        file.close()

    print("extracting standards")
    # standard_refs=extract_standard_ref(filename)
    standard_refs = find_standard_ref(new_text)
    print("standards extracted")

    # ======================== find the recommended standards

    result = {}
    result["extracted_standards"] = standard_refs
    result["recommendations"] = []

    sow = tfidftransformer.transform([new_text])
    sow = normalize(sow, norm="l2", axis=1)

    print("scoring standards")
    distances, indices = nbrs_brute.kneighbors(sow.todense())
    distances = list(distances[0])
    indices = list(indices[0])

    for indx, dist in zip(indices[:10], distances[:10]):
        title = df.iloc[indx]["title"]
        description = df.iloc[indx]["description"]
        link = df.iloc[indx]["link"]
        standard_code = df.iloc[indx]["standard"]
        standard_id = df.iloc[indx]["id"].replace("~", "")
        code = df.iloc[indx]["code"].replace("~", "")
        tc = df.iloc[indx]["tc"]
        type_standard = ["Information Technology"]

        # TODO: this code calculates the word importances for the top results (slows the operation, hence commented)
        # print(title)
        # print(description)
        #
        # to_print = [
        #     tfidftransformer.get_feature_names()[i]
        #     + ' ' +
        #     str(abs(np.array(sow[0].todense()).flatten()[i] - np.array(X[indx].todense()).flatten()[i]))
        #     for i in set(sow.indices).intersection(X[indx].indices)]
        # print(' || '.join(to_print), '\n')

        result["recommendations"].append(
            {
                "sim": 100 * round(1 - dist, 2),
                "raw_id": standard_id,
                "code": code,
                "type": type_standard,
            }
        )
    print("testttt")
    print(result)
    return result
