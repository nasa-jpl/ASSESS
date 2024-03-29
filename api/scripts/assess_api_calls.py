import json
import os.path
import pprint
import time
from os import path

import requests
import yaml
from requests.auth import HTTPBasicAuth


def format_json(jsonText):
    parsed = json.loads(jsonText)
    return json.dumps(parsed, indent=4)


def train():
    print("Sending POST request to `/train`.")
    r = requests.post(
        f"{root}/train",
    )
    print(format_json(r.text))


def recommend_text():
    # Recommend an SoW given text.
    print("Sending GET request to `/recommend_text`.")
    jsonLoad = {"text_field": "Example text about airplanes"}
    r = requests.post(
        f"{root}/recommend_text?size=10&start_from=5",
        json=jsonLoad,
        # auth=HTTPBasicAuth(username, password),
    )
    print(format_json(r.text))


def recommend_file():
    # Recommend an SoW given a PDF.
    # Specify file location of an SOW.
    location = "../data/sow.pdf"
    file = {"pdf": open(location, "rb")}
    print("Sending POST request to `/recommend_file` with a PDF.")
    r = requests.post(
        f"{root}/recommend_file", files=file, auth=HTTPBasicAuth(username, password)
    )
    print(format_json(r.text))


def add():
    print("Sending POST request to `/add_standards`.")
    r = requests.post(
        f"{root}/add_standards", json=doc, auth=HTTPBasicAuth(username, password)
    )
    print(format_json(r.text))
    time.sleep(1)


def standard_info():
    # Look up newly indexed standard.
    # You can search by `id`, `raw_id`, `isbn`, `doc_number`, `technical committee`, `status`,
    # `published_date`, `ingestion_date`, `title`, and `hash` individually as a query parameter.
    # You can also specify a `size` for the query in the results.
    print("Sending GET request to `/standard_info` on ID just added.")
    r = requests.get(
        f"{root}/standard_info/?id=x0288b9ed144439f8ad8fa017d604eac",
        auth=HTTPBasicAuth(username, password),
    )
    print(format_json(r.text))

    # Search by raw_id
    print("Sending GET request to `/standard_info` using raw_id.")
    r = requests.get(
        f"{root}/standard_info/?raw_id=ISO%2044-2:2015",
        auth=HTTPBasicAuth(username, password),
    )
    print(format_json(r.text))

    # Search by doc_number
    print("Sending GET request to `/standard_info` using doc_number field.")
    r = requests.get(
        f"{root}/standard_info/?doc_number=200", auth=HTTPBasicAuth(username, password)
    )
    print(format_json(r.text))

    # Search by status with size 10
    print("Sending GET request to `/standard_info` using published field.")
    r = requests.get(
        f"{root}/standard_info/?status=Published&size=10",
        auth=HTTPBasicAuth(username, password),
    )
    print(format_json(r.text))

    # Search by status with SDO ISO and return 10
    print("Sending GET request to `/standard_info` using sdo == `iso` Key.")
    r = requests.get(
        f"{root}/standard_info/?sdo=iso&size=10",
        auth=HTTPBasicAuth(username, password),
    )
    print(format_json(r.text))


def delete():
    print("Sending DELETE request to `/delete_standard`.")
    r = requests.delete(
        f"{root}/delete_standards?id=x0288b9ed144439f8ad8fa017d604eac",
        auth=HTTPBasicAuth(username, password),
    )
    print(format_json(r.text))
    time.sleep(1)


def edit():
    print("Sending PUT request to `/edit_standards`.")
    r = requests.put(
        f"{root}/edit_standards",
        json=doc,
        auth=HTTPBasicAuth(username, password),
    )
    print(format_json(r.text))
    time.sleep(1)


def select():
    # Insert the standard selected by the *user* into Elasticsearch indices. Useful for statistics.
    selected = {
        "username": "test_user",
        "selected_ids": ["x0288b9ed144439f8ad8fa017d604eac"],
    }
    print("Sending POST request to `/select_standard`.")
    r = requests.post(
        f"{root}/select_standards",
        json=selected,
        auth=HTTPBasicAuth(username, password),
    )
    print(format_json(r.text))


def set_standard():
    set_standards = {
        "username": "test_user",
        "standard_id": "x0288b9ed144439f8ad8fa017d604eac",
        "priority": 100,
    }

    print("Sending PUT request to `set_standard`.")
    r = requests.put(
        f"{root}/set_standards",
        json=set_standards,
        auth=HTTPBasicAuth(username, password),
    )
    print(format_json(r.text))


if __name__ == "__main__":
    doc = {
        "id": "x0288b9ed144439f8ad8fa017d604eac",
        "raw_id": "ISO 44-2:2015",
        "description": "ISO 000 is a dummy standard I am adding that is made up.",
        "ingestion_date": "2018-03-10 13:07:45",
        "hash": "7c8dc19cfbb38a573090c4b0b2c6d3b4f4d68f98ed55506aed936f78cfc71590",
        "published_date": "2020-12",
        "isbn": None,
        "text": ["description"],
        "status": "TO_DELETE",
        "technical_committee": "ISO/TC 1111",
        "title": "This is dummy data",
        "url": "https://www.iso.org/standard/123123.html",
        "category": {"ics": "['43.060.20']"},
        "sdo": {
            "abbreviation": "iso",
            "data": {
                "code": "0.30.010.10.ISO/IEC 10592:1992",
                "edition": [
                    2,
                ],
                "field": "1",
                "group": "1.1",
                "number_of_pages": [1],
                "preview_url": "https://www.iso.org/obp/ui/#!iso:std:123123:en",
                "section_titles": [
                    "Foreword",
                    "Introduction",
                    "1   Scope",
                    "2   Normative references",
                    "3   Terms and definitions",
                ],
                "sections": None,
                "subgroup": "1.1.1",
                "type": "standard",
            },
        },
    }
    # Insert username, password, and ASSESS root url into `conf.yaml`
    with open("../conf.yaml", "r") as stream:
        conf = yaml.safe_load(stream)
    username = conf.get("username")
    password = conf.get("password")
    root = conf.get("url")
    pp = pprint.PrettyPrinter(indent=4)
    print(
        "Running with username: %s, password: %s, and root_url: %s"
        % (username, password, root)
    )
    recommend_text()
    # recommend_file()
    add()
    standard_info()
    edit()
    delete()
    set_standard()
    # train()
