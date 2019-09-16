from flask import Flask, send_from_directory, safe_join
from text_analysis import model
import os
import json
import subprocess
from flask import request
from flask_cors import CORS, cross_origin
import pandas as pd
from sklearn.neighbors import NearestNeighbors
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import normalize
import ast
import re
import statistics
import string
from itertools import tee, islice
import math
import dill
import networkx as nx
import numpy as np
import pandas as pd
import plotly.graph_objs as go
import plotly.offline
from sklearn.feature_extraction import text
import spacy
from standard_extractor import find_standard_ref


app = Flask(__name__)
app.static_folder = "webui"
cors = CORS(app, resources={r"/*": {"origins": "*"}})

standards_dir = 'standards'
json_output_dir = 'output'
models_dir='models'

nlp = spacy.load('en')

def to_string(ar):
    return str(ar)


def to_array(sr):
    return ast.literal_eval(sr)


def savemodel(model, outfile):
    with open(outfile, 'wb') as output:
        dill.dump(model, output)
    return ''


def loadmodel(infile):
    with open(infile, 'rb') as inp:
        model = dill.load(inp)
    return model


def hasNumbers(str):
    return bool(re.search(r'\d', str))


def ispun(str):
    if str in string.punctuation:
        return True
    else:
        return False


def clean_ngram(doc):
    global nlp

    stop_words = text.ENGLISH_STOP_WORDS
    for w in nlp(doc):
        if w.ent_type_ not in ['DATE', 'TIME', 'GPE', 'PERSON', 'CARDINAL'] and not hasNumbers(
                w.text) and not ispun(w.text) and w.text not in stop_words and w.pos_ == 'NOUN':
                    yield w.lemma_.lower()



def hierarchy_pos(G, root, levels=None, width=1., height=1.):
    '''If there is a cycle that is reachable from root, then this will see infinite recursion.
       G: the graph
       root: the root node
       levels: a dictionary
               key: level number (starting from 0)
               value: number of nodes in this level
       width: horizontal space allocated for drawing
       height: vertical space allocated for drawing'''
    TOTAL = "total"
    CURRENT = "current"
    def make_levels(levels, node=root, currentLevel=0, parent=None):
        """Compute the number of nodes for each level
        """
        if not currentLevel in levels:
            levels[currentLevel] = {TOTAL : 0, CURRENT : 0}
        levels[currentLevel][TOTAL] += 1
        neighbors = list(G.neighbors(node))
        for neighbor in neighbors:
            if not neighbor == parent:
                levels =  make_levels(levels, neighbor, currentLevel + 1, node)
        return levels

    def make_pos(pos, node=root, currentLevel=0, parent=None, vert_loc=0):
        dx = 1/levels[currentLevel][TOTAL]
        left = dx/2
        pos[node] = ((left + dx*levels[currentLevel][CURRENT])*width, vert_loc)
        levels[currentLevel][CURRENT] += 1
        neighbors = G.neighbors(node)
        for neighbor in neighbors:
            if not neighbor == parent:
                pos = make_pos(pos, neighbor, currentLevel + 1, node, vert_loc-vert_gap)
        return pos
    if levels is None:
        levels = make_levels({})
    else:
        levels = {l:{TOTAL: levels[l], CURRENT:0} for l in levels}
    vert_gap = height / (max([l for l in levels])+1)
    return make_pos({})




# ================================================================= Prepare the predictor


pos=loadmodel(os.path.join(models_dir,'pos_'))
graph=loadmodel(os.path.join(models_dir,'graph'))

df=pd.read_csv(os.path.join(standards_dir,'iso_final_all_clean_text.csv'),index_col=0)
df=df[df['type']=='standard'].reset_index(drop=True)
df.fillna('', inplace=True)

tfidftransformer=TfidfVectorizer(ngram_range=(1,1), stop_words=text.ENGLISH_STOP_WORDS)
X=tfidftransformer.fit_transform([m+' '+n for m, n in zip(df['description_clean'], df['title'])]) # using both desc and tile to predict
print('shape', X.shape)

X=normalize(X, norm='l2', axis=1)
nbrs_brute = NearestNeighbors(n_neighbors=X.shape[0], algorithm='brute', metric='cosine')

print('fitting')
nbrs_brute.fit(X.todense())
print('fitted')



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
    global Xn, Yn, labels, values, hoverlabels, Xe, Ye, pos, df, graph, title_lookup, indices, distances

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

        print(title)
        print(description)

        to_print = [
            tfidftransformer.get_feature_names()[i]
            + ' ' +
            str(abs(np.array(sow[0].todense()).flatten()[i] - np.array(X[indx].todense()).flatten()[i]))
            for i in set(sow.indices).intersection(X[indx].indices)]
        print(' || '.join(to_print), '\n')
        result['recc'].append(
            {'title': title+' ('+standard_code.replace('~','')+')', 'description':description, 'url': link, 'sim': 100 * round(1-dist, 2)})

    print('scored standards')



    return json.dumps(result)


if __name__ == "__main__":
    app.run()

# todo: set up a search dashboard in kibana with iso data??
# todo: tune the results/ improve the model
# when searched "auronautics" in wikipedia. and I put a couple of first paragraphs from it and then the whole page. The reults vary very much.
#  Seems like the model is very sensitive (to noisy stuff). Also, how come there is some potato standards in the results when I put only a couple of
# paragraphs. So the recall and precision both are off at different times.