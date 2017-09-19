import subprocess
import os
import json
import model




# run the tika extractor and produce the jsons

standards_dir='standards/NASA/NASA'
json_output_dir='output'
for filename in os.listdir(standards_dir):
    print filename
    bashCommand = "java -cp ../standards_extraction/lib/tika-app-1.16.jar:../standards_extraction/bin StandardsExtractor "+\
                  os.path.join(standards_dir,filename)+" 0.75 >"+os.path.join(json_output_dir,filename+'.json')
    print subprocess.check_output(['bash','-c', bashCommand])

# read the json and extract the scopes

texts_all = []
title_all = []
for filename in os.listdir(json_output_dir):
    print filename
    try:
        js=json.load(open(os.path.join(json_output_dir,filename)))
        scope=js['scope']
    except:
        print 'error reading'
    texts_all.append(scope)
    title_all.append(filename)

# build models for system 1 and system 2

print 'building model 1...'
model.build_system1(texts_all,title_all,2)
print 'model 1 ready...'
print 'building model 2...'
model.build_system2(texts_all,title_all)
print 'model 2 ready...'

