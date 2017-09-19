import subprocess
import json
import model

lamdba=.5

sow_path='test.pdf'

bashCommand = "java -cp ../standards_extraction/lib/tika-app-1.16.jar:../standards_extraction/bin StandardsExtractor "+ \
              sow_path+" 0.75 > sow.json"
output = subprocess.check_output(['bash','-c', bashCommand])
standard_refs=[]
try:
    js=json.load(open('sow.json'))
    scope=js['scope']
except:
    print 'no scope available!'
    exit()
try:
    standard_refs=js['standard_references']
except:
    print 'no standard refs found!'

print '\n'.join(standard_refs)
print ''
model.use_system1(scope,lamdba,10)
print ''
model.use_system2(scope,lamdba,10)
