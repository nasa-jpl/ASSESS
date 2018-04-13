import numpy as np
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import string
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import pylab
from sklearn.cross_validation import StratifiedShuffleSplit
from sklearn.metrics import accuracy_score
import itertools, collections


def transform(df):
    """
    Clean, append, and tokenize data to final set.
    """
    X, y = [], []
    # Convert to tuples in order to use the groupby function.
    df.ics = df.ics.transform(lambda x: tuple(x))
    # If ics members are less than 10, remove them
    df = df.groupby('ics').filter(lambda x: len(x) > 10)
    stop = set(stopwords.words('english'))
    for item in df.itertuples():
        """This is where you customize your tokenizer and seprate labels and text,
        defining your Xs and Ys"""
        if item.sections and "foreword" == item.sections[0].split()[0].lower():
            section = item.sections[1:]
        if not item.ics or not section or len(' '.join(section)) < 10:
            continue
        text = item.title + ' ' + ' '.join(section)
        words = word_tokenize(text)
        text_no_stop_words_punct = [t for t in words if t not in stop and t not in string.punctuation]
        wordList = []
        for word in text_no_stop_words_punct:
            wordList.append(word)
        for label in item.ics:
            X.append(wordList)
            y.append(label)
            print(wordList)
            print("========================")
            print(label)
    return (np.array(X), np.array(y))


def benchmark(model, X, y, n):
    """
    Divide into training and test sets, train, then evaluate the score.
    """
    test_size = 1 - (n / float(len(y)))
    scores = []
    for train, test in StratifiedShuffleSplit(y, n_iter=5, test_size=test_size):
        X_train, X_test = X[train], X[test]
        y_train, y_test = y[train], y[test]
        scores.append(accuracy_score(model.fit(X_train, y_train).predict(X_test), y_test))
    return np.mean(scores)


def glove_training(path, X, encoding="utf-8"):
    all_words = set(w for words in X for w in words)
    glove = {}
    with open(path, "rb") as infile:
        for line in infile:
            parts = line.split()
            word = parts[0].decode(encoding)
            if word in all_words:
                nums = np.array(parts[1:], dtype=np.float32)
                glove[word] = nums
    return glove


def get_samples(df):
    counter = collections.Counter(itertools.chain(*list(df["field"])))
    return counter


def plot(df):
    """
    Graph results from the pickled scores.
    """
    print("Graphing results...")
    df = pd.read_pickle()
    df.to_pickle(df)
    plt.figure(figsize=(15, 6))
    fig = sns.pointplot(x='train_size', y='accuracy', hue='model',
                        data=df[df.model.map(lambda x: x in [
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
                                            )
                            ]
                        )
    sns.set_context("notebook", font_scale=1.5)
    fig.set(ylabel="accuracy")
    fig.set(xlabel="labeled training examples")
    fig.set(title="ASSESS Machine learning benchmark")
    fig.set(ylabel="accuracy")
    pylab.show()
