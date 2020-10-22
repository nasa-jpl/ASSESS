import requests
import json

# Endpoints

root = "https://assess-api.jpl.nasa.gov/"
#root = "http://0.0.0.0:8080/"
urlRec = root + "recommend_text"
urlRecFile = root + "recommend_file"
urlExtract = root + "extract"
urlSearch = root + "search"
urlAdd = root + "add_standards"
urlStandardInfo = root + "standard_info"
# Specify file location of an SOW
files = {'pdf': open('/Users/user/prog/assess-root/test.pdf', 'rb')}

## Try root endpoint:
print("Testing root.")
r = requests.get(root)
print(r.text)

# ## Try to recommend text string "This is for airplanes"
print("Testing recommend_text.")
jsonLoad = {"text_field": "This is for airplanes"}
r = requests.post(urlRec, json=jsonLoad)
print(r.text)

## Try to recommend a statement of work PDF 
## ! Remember to add a correct file path !
print("Testing recommend_file.")
r = requests.post(urlRecFile, files=files)
print(r.text)

## PDF standard reference extract.
print("Testing extract.")
r = requests.post(urlExtract, files=files)
print(r.text)

## Get standard references
print("Testing search.")
r = requests.get(urlSearch + "/airplanes%20technology" + "?size=3")
print(r.text)

## Add/Ingest Standard
doc = {
		"num_id": "666666",
		"code": "test-delete-later",
		"field": "test-delete-later",
		"group": "~0.0",
		"id": "~6.6.6",
		"id_": "~6",
		"link": "test",
		"new_field": "~6",
		"new_group": "~6",
		"new_standard": "",
		"new_subgroup": "",
		"standard": "",
		"subgroup": "",
		"title": "test test test test",
		"type": "test",
		"current_status": "",
		"datetime": "",
		"description": "",
		"edition": "",
		"ics": "",
		"number_of_pages": "",
		"preview_url": "",
		"publication_date": "",
		"section_titles": "",
		"sections": "",
		"tc": "",
		"url": "",
		"description_clean": "Testing index ingestion!"
}
print("Testing add_standards")
r = requests.put(urlAdd, json=doc)
print(r.text)

# Look up newly indexed standard
print("Testing standard_info on newly indexed standard")
r = requests.get(urlStandardInfo + "/666666" + "?size=1")
print(r.text)