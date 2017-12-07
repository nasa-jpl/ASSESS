from flask import Flask, send_from_directory, safe_join
from text_analysis import model
import os
import json
import subprocess
from flask import request
from flask_cors import CORS, cross_origin
import pandas as pd

app = Flask(__name__)
app.static_folder = "webui"
cors = CORS(app, resources={r"/*": {"origins": "*"}})

standards_dir = 'standards'
json_output_dir = 'output'
ieee_standards='IEEE-standards_rev1.csv'
df_ieee = pd.read_csv(os.path.join(standards_dir, 'IEEE-standards_rev1.csv'), index_col=0)

@app.route('/')
def index():
    #return 'ASSESS app is online now!'
    return send_from_directory('webui/', 'index.html')

@app.route('/<any(css, js, img, fonts, sound):folder>/<path:filename>')
def toplevel_static(folder, filename):
    filename = safe_join(folder, filename)
    cache_timeout = app.get_send_file_max_age(filename)
    return send_from_directory(app.static_folder, filename, cache_timeout=cache_timeout)

@app.route('/<path:filename>')
def public(filename):
    return send_from_directory('webui/', filename)

@app.route('/train')
def train():
    global df_ieee

    # run the tika extractor and produce the jsons


    # for filename in os.listdir(standards_dir):
    #     print filename
    #     pathname_in = os.path.join(standards_dir, filename)
    #     pathname_out = os.path.join(json_output_dir,filename+'.json')
    #     bashCommand = "java -cp standards_extraction/lib/tika-app-1.16.jar:standards_extraction/bin StandardsExtractor \"" + pathname_in + "\" 0.75 > \"" + pathname_out + "\""
    #     print subprocess.check_output(['bash','-c', bashCommand])

    # read the ieee standards into a pandas dataframe

    df_ieee = pd.read_csv(os.path.join(standards_dir, 'iso_ieee.csv'), index_col=0)
    df_ieee=df_ieee.reset_index()
    # read the json and extract the scopes

    # texts_all = []
    # title_all = []
    # scope=''
    # for filename in os.listdir(json_output_dir):
    #     try:
    #         js = json.load(open(os.path.join(json_output_dir, filename)))
    #         scope = js['scope']
    #     except:
    #         print 'error reading'
    #     texts_all.append(scope)
    #     title_all.append(filename)

    # get all the text from abstract

    texts_abs = list(df_ieee['abstract_new'])
    texts_scp = list(df_ieee['scope_new'])
    texts_pur = list(df_ieee['purpose_new'])
    texts_all= []

    for i in range(len(texts_abs)):
        texts_ab = str(texts_abs[i])
        if texts_ab == 'nan':
            texts_ab = ''
        texts_sc = str(texts_scp[i])
        if texts_sc == 'nan':
            texts_sc = ''
        texts_pu = str(texts_pur[i])
        if texts_pu == 'nan':
            texts_pu = ''

        texts_all.append((texts_ab + texts_sc + texts_pu).decode('utf-8','ignore'))

    # build models for system 1 and system 2

    print 'building model 1...'
    model.build_system1(texts_all, 2)
    print 'model 1 ready.'
    # print 'building model 2...'
    # model.build_system2(texts_all)
    # print 'model 2 ready.'
    return 'model built'

@app.route('/predict',methods=['GET','POST'])
def predict():
    global df_ieee

    scope = ''
    standard_refs = []

    lbd_sys1 = float(request.args.get('lbd_sys1', 1))
    lbd_sys2 = float(request.args.get('lbd_sys2', 1))


    if request.method == 'GET':

        text=request.args.get('text','')
        filename='temp_text'
        file=open(filename,'w')
        file.write(text.encode('utf-8','ignore'))
        file.flush()
        file.close()
        scope=text

        try:
            bashCommand = "java -cp standards_extraction/lib/tika-app-1.16.jar:standards_extraction/bin StandardsExtractor " + \
                          filename + " 0.75 > "+filename+".json"
            output = subprocess.check_output(['bash', '-c', bashCommand])
            print output

        except:

            try:
                js = json.load(open(filename + '.json'))
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

        bashCommand = "java -cp standards_extraction/lib/tika-app-1.16.jar:standards_extraction/bin StandardsExtractor \"" + filename + "\" 0.75 > \"" + filename + ".json\""
        output = subprocess.check_output(['bash', '-c', bashCommand])

        standard_refs = []
        try:
            js = json.load(open(filename+".json"))
            scope = js['text']
        except:
            return 'no scope available!'
        try:
            standard_refs = js['standard_references']
        except:
            print 'no standard refs found!'

    print '\n'.join(standard_refs)
    result_index_sys1,result_sim_sys1=model.use_system1(scope, lbd_sys1, 10)
    # result_index_sys1, result_sim_sys1=model.use_system2(scope, lbd_sys2, 10)

    result={}
    result['refs']=standard_refs
    result['system1_titles'] = [str(x).decode('utf-8','ignore') for x in list(df_ieee.ix[result_index_sys1]['Publication Title'])]
    result['system1_abstracts'] = [str(x).decode('utf-8','ignore') for x in list(df_ieee.ix[result_index_sys1]['abstract_new'])]
    result['system1_links'] = list(df_ieee.ix[result_index_sys1]['PDF Link'])
    result['system1_sim'] = result_sim_sys1

    return json.dumps(result)


if __name__ == "__main__":
    train()
    app.run(host="0.0.0.0", port=5000)
