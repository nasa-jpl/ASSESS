import requests
import json
import time

# Define endpoints
root = "https://assess-api.jpl.nasa.gov/"
#root = "http://0.0.0.0:8080/"
urlRec = root + "recommend_text"
urlRecFile = root + "recommend_file"
urlExtract = root + "extract"
urlSearch = root + "search"
urlAdd = root + "add_standards"
urlStandardInfo = root + "standard_info"
urlSelect = root + "select_standards"
urlSet = root + "set_standards"
# Specify file location of an SOW.
files = {'pdf': open('/Users/user/prog/assess-root/test.pdf', 'rb')}

## Get request to root endpoint.
print("Testing root.")
r = requests.get(root)
print(r.text)

# Recommend SoW given string "This is for airplanes".
print("Testing recommend_text.")
jsonLoad = {"text_field": "This is for airplanes"}
r = requests.post(urlRec, json=jsonLoad)
print(r.text)

# Recommend an SoW given a PDF.
print("Testing recommend_file.")
r = requests.post(urlRecFile, files=files)
print(r.text)

# Extract standard reference from PDF.
print("Testing extract.")
r = requests.post(urlExtract, files=files)
print(r.text)

# Get standard references.
print("Testing search.")
r = requests.get(urlSearch + "/airplanes%20technology" + "?size=3")
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
	"description_clean": "Testing index ingestion!"
}
print("Testing add_standards")
r = requests.put(urlAdd, json=doc)
print(r.text)
time.sleep(2)

# Look up newly indexed standard.
print("Testing standard_info on newly indexed standard")
r = requests.get(urlStandardInfo + "/111111")
print(r.text)

# Insert the standard selected by the user into Elasticsearch indices for stats and logs.
selected = {
		"username" : "test_user",
		"standard_key" : [1,2,3],
}
print("Testing user selected standard.")
r = requests.post(urlSelect, json=selected)
print(r.text)

# Insert the standard selected by the admin into Elasticsearch.
set_standards = { 
"username" : "test_user",
"standard_key": 111111,
"priority" : 100,
}
print("Testing Admin set standard.")
r = requests.put(urlSet, json=set_standards)
print(r.text)