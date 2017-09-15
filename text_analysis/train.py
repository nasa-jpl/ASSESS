import subprocess
import os
import json
import model




# run the tika extractor and produce the jsons

standards_dir=''
json_output_dir=''
for filename in os.listdir(standards_dir):
    bashCommand = "java -cp ../standards_extraction/lib/tika-app-1.16.jar:./bin StandardsExtractor "+\
                  os.path.join(standards_dir,filename)+" 0.75 >"+os.path.join(json_output_dir,filename+'.json')
    output = subprocess.check_output(['bash','-c', bashCommand])

# read the json and extract the scopes

texts_all = []
title_all = []
for filename in os.listdir(json_output_dir):
    js=json.load(open(os.path.join(json_output_dir,filename)))
    scope=js['scope']
    texts_all.append(scope)
    title_all.append(filename)

# build models for system 1 and system 2

model.build_system1(texts_all,title_all,2)
model.build_system2(texts_all,title_all)

