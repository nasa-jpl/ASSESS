import subprocess
import json
import model

lamdba=.5

sow_path=''

bashCommand = "java -cp ../standards_extraction/lib/tika-app-1.16.jar:./bin StandardsExtractor "+ \
              sow_path+" 0.75 > sow.json"
output = subprocess.check_output(['bash','-c', bashCommand])

js=json.load(open('sow.json'))
scope=js['scope']
standard_refs=js['standard_references']

model.use_system1(scope,lamdba,10)
model.use_system2(scope,lamdba,10)
