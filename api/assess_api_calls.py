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
print(format_json(r.text))

# Recommend an SoW given a PDF.
print("Sending GET request to `/recommend_file` with a PDF.")
r = requests.post(urlRecommendFile, files=file, auth=HTTPBasicAuth(username, password))
print(format_json(r.text))

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
    "num_id": "111111",
    "code": "test-delete-later",
    "field": "test-delete-later",
    "group": "~1.0",
    "id": "~1.1.1",
    "id_": "~6",
    "link": "test",
    "new_field": "~6",
    "new_group": "~6",
    "new_standard": "1",
    "new_subgroup": "1",
    "standard": "",
    "subgroup": "1",
    "title": "This is an Example Doc",
    "type": "test_type",
    "current_status": "Awaiting_Removal",
    "datetime": "",
    "description": "Testing index ingestion!",
    "edition": "1",
    "ics": "1.1.1",
    "number_of_pages": "1",
    "preview_url": "https://example.com",
    "publication_date": "",
    "section_titles": "Test Title",
    "sections": "",
    "tc": "",
    "url": "https://example.com",
    "description_clean": "Testing index ingestion!",
}
print("Sending PUT request to `/add_standards`.")
r = requests.put(urlAddStandards, json=doc, auth=HTTPBasicAuth(username, password))
print(format_json(r.text))
time.sleep(2)

# Look up newly indexed standard.
print("Sending GET request to `/standard_info` on newly indexed standard.")
r = requests.get(urlStandardInfo + "/111111", auth=HTTPBasicAuth(username, password))
print(r.text)

# Insert the standard selected by the *user* into Elasticsearch indices. Useful for statistics.
selected = {
    "username": "test_user",
    "standard_key": [1, 2, 3],
}
print("Sending POST request to `/select_standard`.")
r = requests.post(
    urlSelectStandards, json=selected, auth=HTTPBasicAuth(username, password)
)
print(format_json(r.text))

# Set the standard selected by the *admin* into Elasticsearch.
# Allows an admin to do set a standard as a priority.
set_standards = {
    "username": "test_user",
    "standard_id": 111111,
    "priority": 100,
}

print("Sending PUT request to `set_standard`.")
r = requests.put(
    urlSetStandards, json=set_standards, auth=HTTPBasicAuth(username, password)
)
print(format_json(r.text))
