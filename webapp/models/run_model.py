import numpy as np
from nltk.corpus import stopwords
import string
import dill as pickle
import processes
import glob
import os
import sys
reload(sys)
sys.setdefaultencoding('utf8')
from sklearn.feature_extraction.text import TfidfVectorizer

path = '/Users/vishall/Downloads/SOW_txts/'

for filename in os.listdir(path):
    # Vectorize input
    vectorizer = TfidfVectorizer()
    X, y = [], []
    # do your stuff
    with open(path + filename, 'r') as file:
        text = file.read().replace('\n', '')
        #text = [line.decode('utf-8').strip() for line in title_file.readlines()]
        text = text.decode('utf-8')
    print(filename)
    #text = """
    #specifie method measurement concentration gas emission road vehicle inspection maintenance vehicle mass t ignition engine fuel oil mixture mixer method inspection garage roadside check police maintenance operation"""

    tokens = processes.tokenizer(text)
    tokens = vectorizer.fit_transform(tokens)
    X.append(tokens)
    X, y = np.array(X), np.array(y)
    #print(X)

    model_names = [
    #    "svc",
        "svc_tfidf",
    ]

    for name in model_names:
        f = open('trained_models/'+ name +'_20000.sav', 'rb')
        classifier = pickle.load(f)
        f.close()
        print(name)
        print(classifier.predict(X))
        probs = classifier.predict_proba(X)
        print(sum(probs))
        #best_n = np.argsort(probs, axis=1)[-3:]
        #print(best_n)
        print("++++++++++++++")

