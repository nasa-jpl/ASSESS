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

# prepare the predictor

df_lookup = pd.read_csv(os.path.join(standards_dir,'ics_separated.csv'), index_col=0)
df = pd.read_csv(os.path.join(standards_dir,'json_to_csv.csv'), index_col=0)
df.fillna('', inplace=True)
model.build_cosine(df['description'])


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

def extract_standard_ref(filename):

    bashCommand = "java -cp standards_extraction/lib/tika-app-1.16.jar:standards_extraction/bin StandardsExtractor " + \
                  filename + " 0.75 > " + filename + ".json"
    output = subprocess.check_output(['bash', '-c', bashCommand])
    print(output)
    js = json.load(open(filename + '.json'))
    standard_refs=[]
    if 'standard_references' in js.keys():
        standard_refs = js['standard_references']
    print('no standard refs found!')
    return standard_refs


@app.route('/predict',methods=['POST'])
def predict():

    text=''
    # ======================== find the referenced standards
    filename='temp_text'
    # check if the post request has the file part
    if 'file' in request.files:
        file = request.files['file']
    # if user does not select file, browser also
    # submit a empty part without filename
        if file.filename == '':
            return 'no selected file!'
            # return redirect(request.url)
        if file :
            filename=file.filename
            file.save(filename)
            # todo: here we will have to parse the file using tika and not just read it
            text=open(filename,'r')
    else:
        text=request.form.get('text')
        file = open(filename, 'w')
        file.write(str(text.encode('utf-8', 'ignore')))
        file.flush()
        file.close()

    standard_refs=extract_standard_ref(filename)


    # ======================== find the recommended standards

    result={}
    result['refs'] = standard_refs
    result['recc'] = []

    indices, distances= model.predict_cosine(text, 10)
    print(distances)

    for distance, index in zip(distances, indices):
        sim=1-distance
        row = df_lookup[df_lookup['link'] == df.loc[index, 'url']]

        title=row['title'].values
        if len(title)==0:
            title=''
        else:
            title=title[0]

        link = row['link'].values
        if len(link) == 0:
            link = ''
        else:
            link = link[0]

        result['recc'].append({'title':title, 'description':df.loc[index, 'description'], 'url': link, 'sim':100 * round(sim, 2)})
        # print('bah',{'title':row['title'].values[0], 'description':df.loc[index, 'description'].values[0], 'url':row['link'].values[0], 'sim':distance})

    return json.dumps(result)


if __name__ == "__main__":
    app.run()

# todo: set up a search dashboard in kibana with iso data??
# todo: tune the results/ improve the model
# when searched "auronautics" in wikipedia. and I put a couple of first paragraphs from it and then the whole page. The reults vary very much.
#  Seems like the model is very sensitive (to noisy stuff). Also, how come there is some potato standards in the results when I put only a couple of
# paragraphs. So the recall and precision both are off at different times.