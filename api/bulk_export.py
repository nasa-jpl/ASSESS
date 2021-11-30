from elasticsearch import Elasticsearch
from elasticsearch.helpers import scan, bulk
import json
import requests
import uuid
import hashlib
import time
from pprint import pprint
import ast
import pyarrow.feather as feather
from pandas.io.json import json_normalize
from collections import deque
import yaml


def es_to_df(es, index, path="data/feather_text"):
    res = list(scan(es, query={}, index=index))
    output_all = deque()
    output_all.extend([x["_source"] for x in res])
    df = json_normalize(output_all)
    print(df)
    df.to_feather(path)
    return


def series_to_json(doc):
    document_out = {
        "id": doc["id"],
        "raw_id": doc["raw_id"],
        "doc_number": doc["doc_number"],
        "description": doc["description"],  # doc["description_clean"]
        "status": doc["status"],
        "technical_committee": doc["technical_committee"],
        "sdo": {
            "abbreviation": doc["sdo.abbreviation"],
            "data": {
                "code": doc["sdo.data.code"],
                "field": doc["sdo.data.field"],
                "group": doc["sdo.data.subgroup"],
                "subgroup": doc["sdo.data.group"],
                "edition": doc["sdo.data.edition"],
                "number_of_pages": doc["sdo.data.number_of_pages"],
                "section_titles": doc["sdo.data.section_titles"],
                "sections": doc["sdo.data.sections"],
                "type": doc["sdo.data.type"],
                "preview_url": doc["sdo.data.preview_url"],
            },
        },
        "category": {"ics": doc["category.ics"]},  # literal_to_list(doc["ics"])},
        "text": ["description", "title"],  # Change to which field is used for analysis
        "title": doc["title"],
        "published_date": doc["published_date"],
        "isbn": doc["isbn"],
        "url": doc["url"],
        "ingestion_date": doc["ingestion_date"],
        "hash": doc["hash"],  # convert_to_hash(doc["link"]),
    }
    return document_out


def doc_generator(df, index, normalize):
    df_iter = df.iterrows()
    for i, doc in df_iter:
        print(i)
        # print(doc.to_json())
        doc = json.loads(doc.to_json())
        if normalize:
            doc = series_to_json(doc)
        print(json.dumps(doc, indent=4))
        yield {
            "_index": index,
            "_type": "_doc",
            "_id": doc["id"],
            "_source": doc,
        }


def convert_to_hash(url):
    if url and "http" in url:
        r = requests.get(url)
        if r.status_code == 200:
            hash_object = hashlib.sha256(r.content)
            result = hash_object.hexdigest()
            return result
    return None


def strip_number(txt):
    return [int(s) for s in txt.split() if s.isdigit()]


def literal_to_list(val):
    try:
        val = val.replace("'", '"')
        val = val.replace("\\n", "\n")
        val = val.replace("\n", " ")
        res = ast.literal_eval(val)
        return res
    except Exception:
        return


def convert_to_new(doc, client, i, new_index):
    """Convert old schema to new schema."""
    if doc["datetime"]:
        timestamp = doc["datetime"]
    else:
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")  # 2018-03-10 01:23:27
    if doc["current_status"] == "Awaiting_Removal":
        return
    section_titles = literal_to_list(doc["section_titles"])
    sections = literal_to_list(doc["sections"])
    mappings = {
        "id": uuid.uuid4().hex,
        "raw_id": doc["id"].strip("~"),
        "doc_number": i,
        "description": doc["description_clean"],  # doc["description_clean"]
        "status": doc["current_status"],
        "technical_committee": doc["tc"],
        "sdo": {
            "abbreviation": "iso",
            "data": {
                "code": doc["code"].strip("~"),
                "field": doc["field"].strip("~"),
                "group": doc["group"].strip("~"),
                "subgroup": doc["subgroup"].strip("~"),
                "edition": strip_number(doc["edition"]),
                "number_of_pages": strip_number(doc["number_of_pages"]),
                "section_titles": section_titles,
                "sections": sections,
                "type": doc["type"],
                "preview_url": doc["preview_url"],
            },
        },
        "category": {"ics": doc["ics"]},  # literal_to_list(doc["ics"])},
        "text": ["description", "title"],  # Change to which field is used for analysis
        "title": doc["title"].strip("~"),
        "published_date": doc["publication_date"],
        "isbn": None,
        "url": doc["link"],
        "ingestion_date": timestamp,
        "hash": None,  # convert_to_hash(doc["link"]),
    }
    return mappings


def es_to_json(client, local_file, index):
    """Export to json file"""
    i = 0
    start = time.time()
    fp = open(local_file, "w")
    for doc in scan(client, query={}, index=index):
        json.dump(doc, fp)
        fp.write("\n")
        fp.flush()  # So you can tail -f the file
        i += 1
        pprint(i)
    end = time.time() - start
    print(end)
    fp.close()
    return


def df_to_es(df_path, index, client, overwrite=False, normalize=False):
    """Read dataframe and insert into index."""
    # !Important, this will start your index from scratch.
    if overwrite:
        client.indices.delete(index, ignore=[400, 404])
        client.indices.create(index, ignore=400)
    df = feather.read_feather(df_path)
    bulk(client, doc_generator(df, index, normalize))
    return


def es_to_es(client, index, new_index):
    """Migrate from old Elasticsearch index to new Elasticsearch index."""
    i = 0
    start = time.time()
    for doc in scan(client, query={}, index=index):
        i += 1
        pprint(i)
        new_doc = convert_to_new(doc["_source"], client, i, new_index)
        res = client.index(index=new_index, body=json.dumps(new_doc))
    end = time.time() - start
    print(end)
    return


with open("conf.yaml", "r") as stream:
    conf = yaml.safe_load(stream)
df_paths = conf.get("df_paths")
new_index = conf.get("es_index_main")
client = Elasticsearch(http_compress=True)
# es_to_json(client, "elasticsearch-dump.json", index)
for i, df_path in enumerate(df_paths):
    if i == 0:
        df_to_es(df_path, new_index[0], client, overwrite=True, normalize=True)
    else:
        df_to_es(df_path, new_index[0], client)
# es_to_df(client, new_index)
