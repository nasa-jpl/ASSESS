from elasticsearch import Elasticsearch
from elasticsearch.helpers import scan
import json
import requests
import uuid
import hashlib
import time
from pprint import pprint
import ast


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


def clean_sections(txt):
    # TODO: Fix.
    res = {}
    if len(txt) == 1:
        txt = str(txt[0])
    for section in txt:
        try:
            spl = section.split("\n")
            res[spl[0]] = spl[1]
            return res
        except Exception:
            return None
    return res


def convert_to_new(doc, client, i, new_index):
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
        "description": doc["description_clean"],
        "status": doc["current_status"],
        "technical_committee": doc["tc"],
        "sdo": {
            "iso": {
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
            }
        },
        "category": {"ics": literal_to_list(doc["ics"])},
        "text": ["description", "title"],  # Change to which field is used for analysis
        "title": doc["title"].strip("~"),
        "published_date": doc["publication_date"],
        "isbn": None,
        "url": doc["link"],
        "ingestion_date": timestamp,
        "hash": None,  # convert_to_hash(doc["link"]),
    }
    return mappings


def export(client, local_file, index):
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
    fp.close()
    return


def migrate(client, local_file, index, new_index):
    i = 0
    start = time.time()
    for doc in scan(client, query={}, index=INDEX):
        i += 1
        pprint(i)
        new_doc = convert_to_new(doc["_source"], client, i, new_index)
        res = client.index(index=NEW_INDEX, body=json.dumps(new_doc))
    end = time.time() - start
    print(end)
    return


REMOTE_URL = "https://localhost:9200/"
LOCAL_FILE = "elasticsearch-dump.txt"
INDEX = "iso_final_clean"
NEW_INDEX = "assess_remap"
client = Elasticsearch()


migrate(client, LOCAL_FILE, INDEX, NEW_INDEX)
# export(client, LOCAL_FILE, INDEX)
