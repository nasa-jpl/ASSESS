from flask import Flask
from text_analysis import model
import os
import json
import subprocess
from flask import request

app = Flask(__name__)
standards_dir = 'standards'
json_output_dir = 'output'

@app.route('/')
def hello_world():
    return 'ASSESS app is online now!'


@app.route('/train')
def train():

    # run the tika extractor and produce the jsons


    for filename in os.listdir(standards_dir):
        print filename
        bashCommand = "java -cp standards_extraction/lib/tika-app-1.16.jar:standards_extraction/bin StandardsExtractor "+\
                      os.path.join(standards_dir,filename)+" 0.75 >"+os.path.join(json_output_dir,filename+'.json')
        print subprocess.check_output(['bash','-c', bashCommand])

    # read the json and extract the scopes

    texts_all = []
    title_all = []
    scope=''
    for filename in os.listdir(json_output_dir):
        try:
            js = json.load(open(os.path.join(json_output_dir, filename)))
            scope = js['scope']
        except:
            print 'error reading'
        texts_all.append(scope)
        title_all.append(filename)

    # build models for system 1 and system 2

    print 'building model 1...'
    model.build_system1(texts_all, title_all, 2)
    print 'model 1 ready.'
    print 'building model 2...'
    model.build_system2(texts_all, title_all)
    print 'model 2 ready.'
    return 'model built'

@app.route('/predict',methods=['GET','POST'])
def predict():

    scope = ''

    lbd_sys1=float(request.args.get('lbd_sys1',''))
    lbd_sys2 = float(request.args.get('lbd_sys2',''))


    if request.method == 'GET':

        text=request.args.get('text','')
        filename='temp_text'
        file=open(filename,'w')
        file.write(text)
        file.flush()
        file.close()

        bashCommand = "java -cp standards_extraction/lib/tika-app-1.16.jar:standards_extraction/bin StandardsExtractor " + \
                      filename + " 0.75 > "+filename+".json"
        output = subprocess.check_output(['bash', '-c', bashCommand])
        print output

        standard_refs = []
        try:
            js = json.load(open('sow.json'))
            scope = js['scope']
        except:
            print 'no scope available!'
            scope=text
        try:
            standard_refs = js['standard_references']
        except:
            print 'no standard refs found!'

    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            return 'no file in request!'
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            return 'no selected file!'
            return redirect(request.url)
        if file :
            filename=file.filename
            file.save(filename)

        bashCommand = "java -cp standards_extraction/lib/tika-app-1.16.jar:standards_extraction/bin StandardsExtractor " + \
                      filename + " 0.75 > "+filename+".json"
        output = subprocess.check_output(['bash', '-c', bashCommand])
        print output

        standard_refs = []
        try:
            js = json.load(open('sow.json'))
            scope = js['scope']
        except:
            return 'no scope available!'
        try:
            standard_refs = js['standard_references']
        except:
            print 'no standard refs found!'

    print '\n'.join(standard_refs)
    result_title_sys1,result_sim_sys1=model.use_system1(scope, lbd_sys1, 10)
    # result_title_sys2, result_sim_sys2=model.use_system2(scope, lbd_sys2, 10)

    result={}
    result['refs']=standard_refs
    result['system1_titles']=result_title_sys1
    # result['system2_titles'] = result_title_sys2
    result['system1_sim'] = result_sim_sys1
    # result['system2_sim'] = result_sim_sys2
    return json.dumps(result)


if __name__ == "__main__":
    app.run()