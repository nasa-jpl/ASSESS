from tabulate import tabulate
import numpy as np
import pandas as pd
from gensim.models.word2vec import Word2Vec
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.naive_bayes import BernoulliNB, MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.svm import SVC
from sklearn.cross_validation import cross_val_score
import dill as pickle
from vectorizers import MeanEmbedVectorizer, TfidfEmbedVectorizer
import processes
import yaml
import logging
import os
import sys
import re 
try:
    from nltk.corpus import stopwords
except ImportError:
    import nltk
    print("Downloading missing nltk resources.")
    nltk.download('stopwords')
    nltk.download('punkt')

logger = logging.getLogger(__file__)

"""Load the configuration variables and return an error if an incorrect path is found. """
with open('config.yaml', 'r') as f:
    config = yaml.load(f)
iso_path = config['data']
GLOVE_6B_50D_PATH = config['glove_small']
GLOVE_840B_300D_PATH = config['glove_big']
model_path = config['model_path']
stats = config['stats']
ready = [os.path.exists(p) for p in [iso_path, GLOVE_6B_50D_PATH, GLOVE_840B_300D_PATH, model_path, stats]]
encoding = "utf-8"
if all(ready):
    logger.info("All paths exist. Cleaning data set...")
else:
    logger.error("A config path wasn't found... Check your config.yaml settings. Exiting.")
    sys.exit(0)

"""Store the data and perform the appropriate transformations, cleaning, and tokenizing. """
#df = pd.read_json(iso_path)
df = pd.read_csv(iso_path)
fields = (df['field'])
df['field'] = df['field'].str.extract('(\d+)', expand=False)
clean_df =  df[['field', 'description_clean']]
print(len(clean_df))
clean_df = clean_df.dropna()
#field_max = clean_df.groupby["field"].transform(len)
#mask = (field_max > 3)
#clean_df = clean_df[mask]
print(len(clean_df))
#clean_df = clean_df.apply(lambda x: x.mask(x.map(x.value_counts())<3, None))
clean_df = clean_df.groupby('field').filter(lambda x : len(x)>3)
clean_df = clean_df.dropna()
print(len(clean_df))
X, y = clean_df['description_clean'].as_matrix(), clean_df['field'].as_matrix(),
print("done loading data")
logger.info("Total examples %d" % len(y))

# """Load the word2vec and glove vectorizers. """
# with open(GLOVE_6B_50D_PATH, "rb") as lines:
#     wvec = {line.split()[0].decode(encoding): np.array(line.split()[1:], dtype=np.float32)
#             for line in lines}
# glove_small = processes.glove_training(GLOVE_6B_50D_PATH, X)
# glove_big = processes.glove_training(GLOVE_840B_300D_PATH, X)
# w2v_model = Word2Vec(X, size=100, window=5, min_count=5, workers=2)
# w2v = {w: vec for w, vec in zip(w2v_model.wv.index2word, w2v_model.wv.syn0)}

# """The bayes_mult_nb pipeline uses a count vectorizer with TF along with a multinomial bayesian model. """
# mult_nb = Pipeline([
#                         ("count_vectorizer", CountVectorizer(analyzer=lambda x: x)),
#                         ("multinomial nb", MultinomialNB())
#                 ])

# """The bayes_bern_nb pipeline is a count vectorizer with TF along with a bernoulli bayesian model """
# bern_nb = Pipeline([
#                         ("count_vectorizer", CountVectorizer(analyzer=lambda x: x)),
#                         ("bernoulli nb", BernoulliNB())
#                 ])

# """The bayes_mult_nb_tfidf pipeline is using TF-IDF along with a a multinomial bayesian model. """
# mult_nb_tfidf = Pipeline([
#                             ("tfidf_vectorizer", TfidfVectorizer(analyzer=lambda x: x)),
#                             ("multinomial nb", MultinomialNB())
#      ])

# """The bayes_bern_nb_tfidf pipeline is using TF-IDF along with a bernoulli bayesian model. """
# bern_nb_tfidf = Pipeline([
#                             ("tfidf_vectorizer", TfidfVectorizer(analyzer=lambda x: x)),
#                             ("bernoulli nb", BernoulliNB())
#                     ])

# """The svc pipeline is a count vectorizer along with a linear support vector classifier. """
# svc = Pipeline([
#                     ("count_vectorizer", CountVectorizer(analyzer=lambda x: x)),
#                     ("linear svc", SVC(kernel="linear"))
#         ])

"""The svc_tfidf pipeline is a TF-IDF vectorizer along with a linear support vector classifier. """
svc_tfidf = Pipeline([
                        ("tfidf_vectorizer", TfidfVectorizer(analyzer=lambda x: x)),
                        ("linear svc", SVC(kernel="linear", probability=True))
            ])

# """The glove_small pipeline uses the glove vectorization on a 60D textfile. """
# etree_glove_small = Pipeline([
#                                 ("glove vectorizer", MeanEmbedVectorizer(glove_small)),
#                                 ("extra trees", ExtraTreesClassifier(n_estimators=200))
#             ])

# """The glove_small_tfidf pipeline uses the glove vectorization on a 50D textfile. """
# etree_glove_small_tfidf = Pipeline([
#                                         ("glove vectorizer", TfidfEmbedVectorizer(glove_small)),
#                                         ("extra trees", ExtraTreesClassifier(n_estimators=200))
#                         ])

# """The glove_big pipeline uses the glove vectorization and a 300D textfile. """
# etree_glove_big = Pipeline([
#                                 ("glove vectorizer", MeanEmbedVectorizer(glove_big)),
#                                 ("extra trees", ExtraTreesClassifier(n_estimators=200))
#                 ])

# """he glove_big_tfidf pipeline uses the glove vectorization and a 300D textfile. """
# etree_glove_big_tfidf = Pipeline([
#                                     ("glove vectorizer", TfidfEmbedVectorizer(glove_big)),
#                                     ("extra trees", ExtraTreesClassifier(n_estimators=200))
#                         ])

# """The etc_w2v pipeline uses mean embedding on a w2v classifier and a RFDT Classifier. """
# etree_w2v = Pipeline([
#                         ("word2vec vectorizer", MeanEmbedVectorizer(w2v)),
#                         ("extra trees", ExtraTreesClassifier(n_estimators=200))
#         ])

# """The w2v_tfidf pipeline uses TF-IDF with W2V and a RFDT Classifier, """
# etree_w2v_tfidf = Pipeline([
#                         ("word2vec vectorizer", TfidfEmbedVectorizer(w2v)),
#                         ("extra trees", ExtraTreesClassifier(n_estimators=200))
#                 ])

all_models = [
    #("bayes_mult_nb", mult_nb),
    #("bayes_mult_nb_tfidf", mult_nb_tfidf),
    #("bayes_bern_nb", bern_nb),
    #("bayes_bern_nb_tfidf", bern_nb_tfidf),
#    ("svc", svc),
    ("svc_tfidf", svc_tfidf),
    #("w2v", etree_w2v),
    #("w2v_tfidf", etree_w2v_tfidf),
    #("glove_small", etree_glove_small),
    #("glove_small_tfidf", etree_glove_small_tfidf),
    #("glove_big", etree_glove_big),
    #("glove_big_tfidf", etree_glove_big_tfidf),
]
print("starting scoring")
unsorted_scores = [(name, cross_val_score(model, X, y, cv=3).mean()) for name, model in all_models]
print("ending scoring")
scores = sorted(unsorted_scores, key=lambda x: -x[1])
logger.debug(tabulate(scores, floatfmt=".4f", headers=("model", 'score')))
train_sizes = [20000]
table = []

for name, model in all_models:
    print("Training.")
    for n in train_sizes:
        print("Building training set.")
        table.append({'model': name,
                      'accuracy': processes.benchmark(model, X, y, n),
                      'train_size': n})
        print(("Saving model...%s") % (name))
        filename = '%s/%s_%d.sav' % (model_path, name, n)
        pickle.dump(model, open(filename, 'wb'))

df = pd.DataFrame(table)
df.to_pickle("%s/stats.pkl" % (stats))
logger.debug("Training Complete!")
processes.plot(df)
