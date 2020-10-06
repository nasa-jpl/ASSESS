import requests
import json


urlRoot = "https://assess-api.jpl.nasa.gov/"
urlRec = urlRoot + "recommend_text"
urlRecFile = urlRoot + "recommend_file"
urlExtract = urlRoot + "extract"
urlStandardInfo = urlRoot + "standard_info"

assessCred = ('portal', '***REMOVED***')

# r = requests.get(urlRoot)
# print(r.text)

# jsonLoad = {'text_field': "This is for airplanes"}
# r = requests.post(urlRec, data=json.dumps(jsonLoad), auth=assessCred)
# print(r.text)


files = {'pdf': open('test.pdf', 'rb')}
# print(files)
# r = requests.post(urlRecFile, files=files, auth=assessCred)
# print(r.status_code)

# r = requests.post(urlExtract, files=files, auth=assessCred)
# print(r.text)

r = requests.post(urlStandardInfo, files=files, auth=assessCred)
print(r.text)