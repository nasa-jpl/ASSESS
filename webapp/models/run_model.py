import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from nltk.tokenize import sent_tokenize
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import string
import dill as pickle
from sklearn import datasets


# Vectorize input
stop = set(stopwords.words('english'))
all_stops = stop | set(string.punctuation)
encoding="utf-8"
X, y = [], []

# Specify input
text = """
The program is establishing a federated enterprise information sharing architecture for data sharing and decision support tools for cross‐organizational collaboration that is cost effective and adaptable for current and future technologies. As shown in the figure below, the program is focused on technologies with a nexus to the land domain which are interoperable with other data sources and decision support tools.

The core technology is being leveraged from an S&T coastal situational awareness project, reducing the lifecycle cost and risk while also enabling information sharing across border domains (i.e. land, coastal).

The program is pursuing a mix of government‐of‐the‐shelf (GOTS) and Homeland Security Industrial Base decision support tools as a risk pooling strategy that manages cost and ensures some capability is delivered while also making some investments in innovative, higher risk technologies.

"""
words = word_tokenize(text)
text_no_stop_words_punct = [t for t in words if t not in stop and t not in string.punctuation]
wordList = []
for word in text_no_stop_words_punct:
    wordList.append(word)
X.append(wordList)
X, y = np.array(X), np.array(y)
print(X)

# List of models
model_names = [
    "bayes_mult_nb",
    "bayes_mult_nb_tfidf",
    "bayes_bern_nb",
    "bayes_bern_nb_tfidf",
    "svc",
    "svc_tfidf",
    "w2v",
    "w2v_tfidf",
    "glove_small",
    "glove_small_tfidf",
    "glove_big",
    "glove_big_tfidf",
]

for name in model_names:
    f = open('trained_models/'+ name +'_8000.sav', 'rb')
    classifier = pickle.load(f)
    f.close()
    print(name)
    print(classifier.predict(X))
    #probs = classifier.predict_proba(X)
    #print(sum(probs))
    #best_n = np.argsort(probs, axis=1)[-3:]
    #print(best_n)
    print("++++++++++++++")

