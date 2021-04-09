from elasticsearch import Elasticsearch
from elasticsearch.helpers import scan
import json
import requests
import uuid
import hashlib
import time
from pprint import pprint


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


def clean_sections(txt):
    res = {}
    for section in txt:
        try:
            spl = section.split("\n")
            res[spl[0]] = spl[1]
        except Exception:
            return None
    return res


def convert_to_new(doc, client, i, new="assess_remap"):
    if doc["datetime"]:
        timestamp = doc["datetime"]
    else:
        timestamp = time.strftime("%Y/%m/%d %H:%M:%S")  # 2018-03-10 01:23:27

    mappings = {
        "_id": uuid.uuid4().hex,
        "raw_id": doc["id"].strip("~"),
        "doc_number": i,
        "description": doc["description"],
        "status": doc["current_status"],
        "technical_committee": doc["tc"],  # doc["technical_committee"]
        "sdo": {
            "ics": {
                "raw_ics": list(doc["ics"]),
                "code": doc["code"].strip("~"),
                "field": doc["field"].strip("~"),
                "group": doc["group"].strip("~"),
                "subgroup": doc["subgroup"].strip("~"),
                "edition": strip_number(doc["edition"]),
                "number_of_pages": strip_number(doc["number_of_pages"]),
                "section_titles": list(doc["section_titles"]),
                "sections": clean_sections(list(doc["sections"])),
                "new_standard": doc["new_standard"].strip("~"),
                "new_field": doc["new_field"].strip("~"),
                "new_group": doc["new_group"].strip("~"),
                "new_subgroup": doc["new_subgroup"].strip("~"),
                "type": doc["type"],
                "preview_url": doc["preview_url"],
            }
        },
        "title": doc["title"].strip("~"),
        "published_date": doc["publication_date"],
        "isbn": None,
        "url": doc["link"],
        "ingestion_date": timestamp,
        "hash": convert_to_hash(doc["link"]),
    }
    print(doc["sections"])
    return mappings


REMOTE_URL = "https://localhost:9200/"
LOCAL_FILE = "elasticsearch-dump.txt"
INDEX = "iso_final_clean"
client = Elasticsearch()

# fp = open(LOCAL_FILE, "w")
i = 0
for doc in scan(client, query={}, index=INDEX):
    # json.dump(row, fp)
    # fp.write("\n")
    # fp.flush()  # So you can tail -f the file
    i += 1
    print("old")
    pprint(doc["_source"])
    print("new")
    pprint(convert_to_new(doc["_source"], client, i))
    if i == 50:
        exit()

# fp.close()