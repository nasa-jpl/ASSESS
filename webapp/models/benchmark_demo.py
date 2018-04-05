from tabulate import tabulate
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from gensim.models.word2vec import Word2Vec
from collections import Counter, defaultdict
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.naive_bayes import BernoulliNB, MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score
from sklearn.cross_validation import cross_val_score
from sklearn.cross_validation import StratifiedShuffleSplit
from nltk.tokenize import sent_tokenize
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import string
import pylab
from functools import wraps
import errno
import os
import signal
import dill as pickle


# We can use later for decorating functions with a timeout.
class TimeoutError(Exception):
    pass

def timeout(seconds=10, error_message=os.strerror(errno.ETIME)):
    def decorator(func):
        def _handle_timeout(signum, frame):
            raise TimeoutError(error_message)

        def wrapper(*args, **kwargs):
            signal.signal(signal.SIGALRM, _handle_timeout)
            signal.alarm(seconds)
            try:
                result = func(*args, **kwargs)
            finally:
                signal.alarm(0)
            return result

        return wraps(func)(wrapper)
    return decorator


class MeanEmbedVectorizer(object):
    def __init__(self, word2vec):
        self.word2vec = word2vec
        if len(word2vec) > 0:
            self.dim = len(word2vec[next(iter(glove_small))])
        else:
            self.dim = 0

    def fit(self, X, y):
        return self

    def transform(self, X):
        return np.array([
            np.mean([self.word2vec[w] for w in words if w in self.word2vec]
                    or [np.zeros(self.dim)], axis=0)
            for words in X
        ])


class TfidfEmbedVectorizer(object):
    def __init__(self, word2vec):
        self.word2vec = word2vec
        self.word2weight = None
        if len(word2vec) > 0:
            self.dim = len(word2vec[next(iter(glove_small))])
        else:
            self.dim = 0

    def fit(self, X, y):
        tfidf = TfidfVectorizer(analyzer=lambda x: x)
        tfidf.fit(X)
        max_idf = max(tfidf.idf_)
        self.word2weight = defaultdict(
            lambda: max_idf,
            [(w, tfidf.idf_[i]) for w, i in tfidf.vocabulary_.items()])

        return self

    def transform(self, X):
        return np.array([
            np.mean([self.word2vec[w] * self.word2weight[w]
                     for w in words if w in self.word2vec] or
                    [np.zeros(self.dim)], axis=0)
            for words in X
        ])

"""
TODO:
Clean up this section into it's own pre-processing function.
"""
# Using csv instead of ES index for now.
path = "YOUR_GLOVE_PATH"
df = pd.read_json("../../iso_flat.json")
# Convert to tuples in order to use the groupby function.
df.ics = df.ics.transform(lambda x: tuple(x))
df.sections = df.sections.transform(lambda x: x[1:])
# In order to run this you need Tuples.
df = df[df.groupby('ics').sections.transform(len) > 10]
labels = df.ics
stop = set(stopwords.words('english'))
all_stops = stop | set(string.punctuation)

GLOVE_6B_50D_PATH = path + "glove.6B.50d.txt"
GLOVE_840B_300D_PATH = path + "glove.840B.300d.txt"
encoding="utf-8"

X, y = [], []

for item in df.itertuples():
    """This is where you customize your tokenizer and seprate labels and text,
    defining your Xs and Ys"""
    if not item.ics or not item.sections or len(item.sections) < 1 or len(' '.join(item.sections)) < 10:
        continue
    text = item.sections
    # Include the title. check how many standards have scope.
    text = item.description + ' ' + ' '.join(text)
    words = word_tokenize(text)
    text_no_stop_words_punct = [t for t in words if t not in stop and t not in string.punctuation]
    wordList = []
    for word in text_no_stop_words_punct:
        wordList.append(word)
    field = item.ics[0].split('.')[0:3]
    field = ".".join(field)
    X.append(wordList)
    y.append(field)
    print(field)
    print("### START: Input text ###")
    print(wordList)
    print("========================")
    print(field)
    print("### END ###")

X, y = np.array(X), np.array(y)
print ("total examples %s" % len(y))
with open(GLOVE_6B_50D_PATH, "rb") as lines:
    wvec = {line.split()[0].decode(encoding): np.array(line.split()[1:], dtype=np.float32)
            for line in lines}

glove_small = {}
all_words = set(w for words in X for w in words)
with open(GLOVE_6B_50D_PATH, "rb") as infile:
    for line in infile:
        parts = line.split()
        word = parts[0].decode(encoding)
        if (word in all_words):
            nums = np.array(parts[1:], dtype=np.float32)
            glove_small[word] = nums

glove_big = {}
with open(GLOVE_840B_300D_PATH, "rb") as infile:
    for line in infile:
        parts = line.split()
        word = parts[0].decode(encoding)
        if word in all_words:
            nums = np.array(parts[1:], dtype=np.float32)
            glove_big[word] = nums

# Train word2vec
model = Word2Vec(X, size=100, window=5, min_count=5, workers=2)
w2v = {w: vec for w, vec in zip(model.wv.index2word, model.wv.syn0)}

bayes_mult_nb = Pipeline([("count_vectorizer", CountVectorizer(analyzer=lambda x: x)), ("multinomial nb", MultinomialNB())])
bayes_bern_nb = Pipeline([("count_vectorizer", CountVectorizer(analyzer=lambda x: x)), ("bernoulli nb", BernoulliNB())])
bayes_mult_nb_tfidf = Pipeline(
    [("tfidf_vectorizer", TfidfVectorizer(analyzer=lambda x: x)), ("multinomial nb", MultinomialNB())])
bayes_bern_nb_tfidf = Pipeline([("tfidf_vectorizer", TfidfVectorizer(analyzer=lambda x: x)), ("bernoulli nb", BernoulliNB())])
svc = Pipeline([("count_vectorizer", CountVectorizer(analyzer=lambda x: x)), ("linear svc", SVC(kernel="linear"))])
svc_tfidf = Pipeline(
    [("tfidf_vectorizer", TfidfVectorizer(analyzer=lambda x: x)), ("linear svc", SVC(kernel="linear"))])
# Extra Trees classifier is like random forrest
glove_sm = Pipeline([("glove vectorizer", MeanEmbedVectorizer(glove_small)),
                              ("extra trees", ExtraTreesClassifier(n_estimators=200))])
glove_sm_tfidf = Pipeline([("glove vectorizer", TfidfEmbedVectorizer(glove_small)),
                                    ("extra trees", ExtraTreesClassifier(n_estimators=200))])
glove_big = Pipeline([("glove vectorizer", MeanEmbedVectorizer(glove_big)),
                            ("extra trees", ExtraTreesClassifier(n_estimators=200))])
glove_big_tfidf = Pipeline([("glove vectorizer", TfidfEmbedVectorizer(glove_big)),
                                  ("extra trees", ExtraTreesClassifier(n_estimators=200))])
etc_w2v = Pipeline([("word2vec vectorizer", MeanEmbedVectorizer(w2v)),
                      ("extra trees", ExtraTreesClassifier(n_estimators=200))])
w2v_tfidf = Pipeline([("word2vec vectorizer", TfidfEmbedVectorizer(w2v)),
                            ("extra trees", ExtraTreesClassifier(n_estimators=200))])
all_models = [
    ("bayes_mult_nb", bayes_mult_nb),
    ("bayes_mult_nb_tfidf", bayes_mult_nb_tfidf),
    ("bayes_bern_nb", bayes_bern_nb),
    ("bayes_bern_nb_tfidf", bayes_bern_nb_tfidf),
    ("svc", svc),
    ("svc_tfidf", svc_tfidf),
    ("w2v", etc_w2v),
    ("w2v_tfidf", w2v_tfidf),
    ("glove_small", glove_small),
    ("glove_small_tfidf", glove_small_tfidf),
    ("glove_big", glove_big),
    ("glove_big_tfidf", glove_big_tfidf),

]

unsorted_scores = [(name, cross_val_score(model, X, y, cv=5).mean()) for name, model in all_models]
scores = sorted(unsorted_scores, key=lambda x: -x[1])
print(tabulate(scores, floatfmt=".4f", headers=("model", 'score')))
# *Show preliminary data
#plt.figure(figsize=(15, 6))
#sns.barplot(x=[name for name, _ in scores], y=[score for _, score in scores])
#pylab.show()

def benchmark(model, X, y, n):
    test_size = 1 - (n / float(len(y)))
    scores = []
    for train, test in StratifiedShuffleSplit(y, n_iter=5, test_size=test_size):
        print('.', end='')
        X_train, X_test = X[train], X[test]
        y_train, y_test = y[train], y[test]
        scores.append(accuracy_score(model.fit(X_train, y_train).predict(X_test), y_test))
    return np.mean(scores)

# Training sizes- make sure they're scaled to the data
train_sizes = [800, 1600, 3200, 6400, 8200, 12500, 15000]
table = []

for name, model in all_models:
    for n in train_sizes:
        print("Training.")
        table.append({'model': name,
                      'accuracy': benchmark(model, X, y, n),
                      'train_size': n})
        print(("Saving model...%s") % (name))
        filename = 'trained_models/%s_%d.sav' % (name, n)
        pickle.dump(model, open(filename, 'wb'))
print("Graphing results...")
df = pd.DataFrame(table)
plt.figure(figsize=(15, 6))
fig = sns.pointplot(x='train_size', y='accuracy', hue='model',
                    data=df[df.model.map(lambda x: x in ["bayes_mult_nb", "bayes_mult_nb_tfidf", "bayes_bern_nb",
                                                         "bayes_bern_nb_tfidf", "svc", "svc_tfidf", "w2v", "w2v_tfidf",
                                                         "glove_small", "glove_small_tfidf", "glove_big", "glove_big_tfidf",
                                                        ])])
sns.set_context("notebook", font_scale=1.5)
fig.set(ylabel="accuracy")
fig.set(xlabel="labeled training examples")
fig.set(title="ASSESS Machine learning benchmark")
fig.set(ylabel="accuracy")
pylab.show()
