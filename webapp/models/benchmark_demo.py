from tabulate import tabulate
import numpy as np
from gensim.models.word2vec import Word2Vec
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.naive_bayes import BernoulliNB, MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.svm import SVC
from sklearn.cross_validation import cross_val_score
try:
    from nltk.corpus import stopwords
except ImportError:
    import nltk
    print("Downloading missing nltk resources.")
    nltk.download('stopwords')
    nltk.download('punkt')
import dill as pickle
from vectorizers import MeanEmbedVectorizer, TfidfEmbedVectorizer
import processes
import yaml
import logging
import os, sys


with open('config.yaml', 'r') as f:
    config = yaml.load(f)

iso_path = config['data']
GLOVE_6B_50D_PATH = config['glove_small']
GLOVE_840B_300D_PATH = config['glove_big']
model_path = config['model_path']
stats = config['stats']

logger = logging.getLogger(__file__)

ready = [os.path.exists(p) for p in [iso_path, GLOVE_6B_50D_PATH, GLOVE_840B_300D_PATH, model_path, stats]]

if all(ready):
    logger.info("All paths exist. Cleaning data set...")
else:
    logger.error("* A config path wasn't found... Check your config.yaml settings. Exiting. *")
    sys.exit(0)

df = open(iso_path)
X, y = processes.transform(df)
encoding = "utf-8"

logger.info("Total examples %s" % len(y))
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


""" The bayes_mult_nb pipeline is a count vectorizer using TF along with a multinomial bayesian model. """
bayes_mult_nb = Pipeline([
                            ("count_vectorizer",
                            CountVectorizer(analyzer=lambda x: x)),
                            ("multinomial nb",
                            MultinomialNB())
                ])

""" The bayes_bern_nb pipeline is a count vectorizer using TF along with a bernoulli bayesian model """
bayes_bern_nb = Pipeline([
                            ("count_vectorizer",
                            CountVectorizer(analyzer=lambda x: x)),
                            ("bernoulli nb", BernoulliNB())
                ])

""" The bayes_mult_nb_tfidf pipeline is using TF-IDF along with a a multinomial bayesian model. """
bayes_mult_nb_tfidf = Pipeline([
                                ("tfidf_vectorizer",
                                TfidfVectorizer(analyzer=lambda x: x)),
                                ("multinomial nb",
                                MultinomialNB())
     ])

""" The bayes_bern_nb_tfidf pipeline is using TF-IDF along with a bernoulli bayesian model. """
bayes_bern_nb_tfidf = Pipeline([
                                    ("tfidf_vectorizer",
                                    TfidfVectorizer(analyzer=lambda x: x)),
                                    ("bernoulli nb",
                                     BernoulliNB())
                    ])

""" The svc pipeline is a count vectorizer along with a linear support vector classifier. """
svc = Pipeline([
                    ("count_vectorizer",
                    CountVectorizer(analyzer=lambda x: x)),
                    ("linear svc", SVC(kernel="linear"))
        ])

""" The svc_tfidf pipeline is a TF-IDF vectorizer along with a linear support vector classifier. """
svc_tfidf = Pipeline([
                        ("tfidf_vectorizer",
                        TfidfVectorizer(analyzer=lambda x: x)),
                        ("linear svc", SVC(kernel="linear"))
            ])
""" The glove_small pipeline uses the GLOVE vectorization on a 60D textfile. """
glove_small = Pipeline([
                            ("glove vectorizer",
                            MeanEmbedVectorizer(glove_small)),
                            ("extra trees",
                            ExtraTreesClassifier(n_estimators=200))
            ])

""" The glove_small_tfidf pipeline uses the GLOVE vectorization on a 60D textfile. """
glove_small_tfidf = Pipeline([
                                ("glove vectorizer",
                                TfidfEmbedVectorizer(glove_small)),
                                ("extra trees",
                                ExtraTreesClassifier(n_estimators=200))
                    ])

""" The glove_big pipeline uses the GLOVE vectorization on a 180D textfile. """
glove_big = Pipeline([
                        ("glove vectorizer",
                        MeanEmbedVectorizer(glove_big)),
                        ("extra trees",
                        ExtraTreesClassifier(n_estimators=200))
            ])
""" The glove_big_tfidf pipeline uses the GLOVE vectorization on a 180D textfile. """
glove_big_tfidf = Pipeline([
                            ("glove vectorizer",
                            TfidfEmbedVectorizer(glove_big)),
                            ("extra trees",
                            ExtraTreesClassifier(n_estimators=200))
                ])

""" The etc_w2v pipeline uses... """
etc_w2v = Pipeline([
                    ("word2vec vectorizer",
                     MeanEmbedVectorizer(w2v)),
                    ("extra trees",
                    ExtraTreesClassifier(n_estimators=200))
        ])

""" The w2v_tfidf pipeline uses... """
w2v_tfidf = Pipeline([
                        ("word2vec vectorizer",
                        TfidfEmbedVectorizer(w2v)),
                        ("extra trees", ExtraTreesClassifier(n_estimators=200))
            ])

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
logger.debug(tabulate(scores, floatfmt=".4f", headers=("model", 'score')))
# *Show preliminary data
#plt.figure(figsize=(15, 6))
#sns.barplot(x=[name for name, _ in scores], y=[score for _, score in scores])
#pylab.show()
# Training sizes- make sure they're scaled to the data
train_sizes = [800, 1600, 3200, 6400, 9200, 13200]
table = []

for name, model in all_models:
    logger.debug("Training.")
    for n in train_sizes:
        print("Building training set.")
        table.append({'model': name,
                      'accuracy': processes.benchmark(model, X, y, n),
                      'train_size': n})
        print(("Saving model...%s") % (name))
        filename = '%s/%s_%d.sav' % (model_path, name, n)
        pickle.dump(model, open(filename, 'wb'))

logger.debug("Training Complete.")
