from flask import Flask, send_from_directory, safe_join
import os
import json
import subprocess
from flask import request
from flask_cors import CORS, cross_origin
from sklearn.neighbors import NearestNeighbors
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import normalize
import dill
import pandas as pd
from sklearn.feature_extraction import text
from standard_extractor import find_standard_ref
from text_analysis.utils import loadmodel

app = Flask(__name__)
app.static_folder = "webui"
cors = CORS(app, resources={r"/*": {"origins": "*"}})

standards_dir = 'standards/data'
json_output_dir = 'output'
models_dir='models'



# ================================================================= Prepare the predictor (when the app starts)


pos=loadmodel(os.path.join(models_dir,'pos_'))
graph=loadmodel(os.path.join(models_dir,'graph'))

df=pd.read_csv(os.path.join(standards_dir,'iso_final_all_clean_text.csv'),index_col=0)
df=df[df['type']=='standard'].reset_index(drop=True)
df.fillna('', inplace=True)

tfidftransformer=TfidfVectorizer(ngram_range=(1,1), stop_words=text.ENGLISH_STOP_WORDS)
X=tfidftransformer.fit_transform([m+' '+n for m, n in zip(df['description_clean'], df['title'])]) # using both desc and tile to predict

# tfidftransformer=TfidfVectorizer(ngram_range=(1,1))
# X=tfidftransformer.fit_transform([m+' '+n for m, n in zip(df['description'], df['title'])]) # using both desc and tile to predict

print('shape', X.shape)

X=normalize(X, norm='l2', axis=1)
nbrs_brute = NearestNeighbors(n_neighbors=X.shape[0], algorithm='brute', metric='cosine')

print('fitting')
nbrs_brute.fit(X.todense())
print('fitted')

# =================================================================




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
    js = json.load(open(filename + '.json'))
    standard_refs=[]
    if 'standard_references' in js.keys():
        standard_refs = js['standard_references']
    print('no standard refs found!')
    return standard_refs


def parse_text(filepath):

    if os.path.exists(filepath+'_parsed.txt'):
        # todo: remove this. Caches the parsed text.
        return str(open(filepath+'_parsed.txt', 'r').read())

    bashCommand = "java -jar standards_extraction/lib/tika-app-1.16.jar -t " + filepath
    output=''
    try:
        output = subprocess.check_output(['bash', '-c', bashCommand])
        file=open(filepath + '_parsed.txt', 'wb')
        file.write(output)
        file.close()
    except subprocess.CalledProcessError as e:
        print(e.output)


    return str(output)


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
            text=parse_text(filename)
            print('parsed')
    else:
        text=request.form.get('text')
        file = open(filename, 'w')
        file.write(str(text.encode('utf-8', 'ignore')))
        file.flush()
        file.close()

    print('extracting standards')
    # standard_refs=extract_standard_ref(filename)
    standard_refs=find_standard_ref(text)
    print('standards extracted')

    # ======================== find the recommended standards

    result={}
    result['refs'] = standard_refs
    result['recc'] = []

    sow = tfidftransformer.transform([text])
    sow = normalize(sow, norm='l2', axis=1)

    print('scoring standards')
    distances, indices = nbrs_brute.kneighbors(sow.todense())
    distances = list(distances[0])
    indices = list(indices[0])

    for indx, dist in zip(indices[:10],distances[:10]):
        title=df.iloc[indx]['title']
        description=df.iloc[indx]['description']
        link=df.iloc[indx]['link']
        standard_code = df.iloc[indx]['standard']

        # todo: this code calculates the word importances for the top results (slows the operation, hence commented)
        # print(title)
        # print(description)
        #
        # to_print = [
        #     tfidftransformer.get_feature_names()[i]
        #     + ' ' +
        #     str(abs(np.array(sow[0].todense()).flatten()[i] - np.array(X[indx].todense()).flatten()[i]))
        #     for i in set(sow.indices).intersection(X[indx].indices)]
        # print(' || '.join(to_print), '\n')


        result['recc'].append(
            {'title': title+' ('+standard_code.replace('~','')+')', 'description':description, 'url': link, 'sim': 100 * round(1-dist, 2)})

    print('scored standards')



    return json.dumps(result)


if __name__ == "__main__":
    app.run()


# todo: make this the main version of api. Add the endpoint for creating the graph.
