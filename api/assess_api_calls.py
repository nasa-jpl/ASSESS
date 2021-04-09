import json
import time
import requests
from requests.auth import HTTPBasicAuth
import yaml
import os.path
from os import path
from web_utils import format_json

# Insert username, password, and ASSESS root url into `conf.yaml`
with open("conf.yaml", "r") as stream:
    conf = yaml.safe_load(stream)
username = conf.get("username")
password = conf.get("password")
root = conf.get("url")
print(
    "Running with username: %s, password: %s, and root_url: %s"
    % (username, password, root)
)

if None in [username, password, root]:
    print("Define variables in ./conf.yaml. Exiting.")
    exit()

# Define API endpoints.
urlRecommendText = root + "/recommend_text"
urlRecommendFile = root + "/recommend_file"
urlExtract = root + "/extract"
urlSearch = root + "/search"
urlAddStandards = root + "/add_standards"
urlStandardInfo = root + "/standard_info"
urlSelectStandards = root + "/select_standards"
urlSetStandards = root + "/set_standards"

# Specify file location of an SOW.
location = "/Users/vishall/prog/assess-root/test.pdf"
file = {"pdf": open(location, "rb")}

# Recommend SoW given text "Example text about airplanes.".
print("Sending GET request to `/recommend_text`.")
jsonLoad = {"text_field": "Example text about airplanes"}
r = requests.post(
    urlRecommendText, json=jsonLoad, auth=HTTPBasicAuth(username, password)
)
print(r.text)

# Recommend an SoW given a PDF.
print("Sending GET request to `/recommend_file` with a PDF.")
r = requests.post(urlRecommendFile, files=file, auth=HTTPBasicAuth(username, password))
print(r.text)

# Extract standard reference from PDF.
print("Sending POST request to `/extract` using a PDF.")
r = requests.post(urlRecommendFile, files=file, auth=HTTPBasicAuth(username, password))
print(format_json(r.text))


# Get standard references.
print("Sending GET request to `/search`.")
r = requests.get(
    urlSearch + "/airplanes%20technology" + "?size=3",
    auth=HTTPBasicAuth(username, password),
)
print(r.text)

## Add/Ingest Standard.
doc = {
    "id": "A123456Z",
    "raw_id": "ICS-TEST",
    "doc_number": 0,
    "description": "Testing, delete",
    "status": "Awaiting_Removal",
    "technical_committee": "1.2.3",
    "sdo": {
        "ics": {
            "raw_ics": None,
            "code": None,
            "field": None,
            "group": None,
            "subgroup": None,
            "edition": None,
            "number_of_pages": None,
            "section_titles": None,
            "sections": None,
            "new_standard": None,
            "new_field": None,
            "new_group": None,
            "new_subgroup": None,
            "type": None,
            "preview_url": None,
        }
    },
    "title": "Test Title- Delete Later",
    "published_date": None,
    "isbn": None,
    "url": None,
    "ingestion_date": None,
    "hash": None,
}
print("Sending PUT request to `/add_standards`.")
r = requests.put(urlAddStandards, json=doc, auth=HTTPBasicAuth(username, password))
print(format_json(r.text))
time.sleep(2)

# Look up newly indexed standard.
print("Sending GET request to `/standard_info` on newly indexed standard.")
r = requests.get(urlStandardInfo + "/A123456Z", auth=HTTPBasicAuth(username, password))
print(r.text)

# Insert the standard selected by the *user* into Elasticsearch indices. Useful for statistics.
selected = {
    "username": "test_user",
    "selected_ids": ["A123456Z"],
}
print("Sending POST request to `/select_standard`.")
r = requests.post(
    urlSelectStandards, json=selected, auth=HTTPBasicAuth(username, password)
)
print(format_json(r.text))

# Set the standard selected by the *admin* into Elasticsearch.
# Allows an admin to give a standard priority.
set_standards = {
    "username": "test_user",
    "standard_id": "A123456Z",
    "priority": 100,
}

print("Sending PUT request to `set_standard`.")
r = requests.put(
    urlSetStandards, json=set_standards, auth=HTTPBasicAuth(username, password)
)
print(format_json(r.text))
