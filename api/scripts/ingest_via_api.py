import os
import pandas as pd
from jsonschema import validate
import json
import time
import requests

root = "http://ec2-3-236-240-230.compute-1.amazonaws.com:8080"
schema = {
    "type": "object",
    "properties": {
        "doc_number": {"type": ["string", "null"]},
        "id": {"type": ["string", "null"]},
        "raw_id": {"type": ["string", "null"]},
        "description": {"type": ["string", "null"]},
        "ingestion_date": {"type": "string"},
        "hash": {"type": ["string", "null"]},
        "published_date": {"type": ["string", "null"]},
        "isbn": {"type": ["string", "null"]},
        "text": {"type": ["array", "null"]},
        "status": {"type": ["string", "null"]},
        "technical_committee": {"type": ["string", "null"]},
        "title": {"type": ["string", "null"]},
        "url": {"type": ["string", "null"]},
        "category": {"type": ["object", "null"]},
        "sdo": {"type": ["object", "null"]},
    },
}


def format_json(jsonText):
    parsed = json.loads(jsonText)
    return json.dumps(parsed, indent=4)


def ingest(doc):
    validate(instance=doc, schema=schema)
    #print("Sending POST request to `/add_standards`.")
    r = requests.post(f"{root}/add_standards", json=doc)
    print(format_json(r.text))


def search_by_id(id):
    print("Sending GET request to `/standard_info` on ID.")
    r = requests.get(
        f"{root}/standard_info/?id={id}",
    )
    print(format_json(r.text))


def search_by_description(q):
    print("Sending GET request to `/search` on description.")
    r = requests.get(
        f"{root}/search/{q}/?size=1",
    )
    print(format_json(r.text))


def delete_by_id(id):
    print("Sending DELETE request to `/delete_standard`.")
    r = requests.delete(
        f"{root}/delete_standards?id={id}",
    )
    print(format_json(r.text))
    time.sleep(1)


def test(id):
    print("Search ID.")
    search_by_id(id)
    print("Search Description.")
    search_by_description("radionuclides")
    # print("Delete.")
    # delete_by_id(id)


# test("xed8b332415d488f873938e36bda8a4c")
path_to_json = '../data/crawler'
json_files = [pos_json for pos_json in os.listdir(
    path_to_json) if pos_json.endswith('.json')]
for file in json_files:
    print(file)
    docs = pd.read_json(path_to_json + "/" + file, lines=True)
    # print(docs.to_json)
    doc_list = docs.apply(lambda x: x.to_json(), axis=1)
    for doc in doc_list:
        doc = json.loads(doc)
        print(dict(doc))
        ingest(doc)
        time.sleep(0.1)
