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


def transform(df):
    """
    Filter dataframe before iterating through each datapoint
    """
    X, y = [], []
    # Convert to tuples in order to use the groupby function.
    df.ics = df.ics.transform(lambda x: tuple(x))
    # If the ICS members are less than 10, remove them
    # TODO: train each X on every ICS code in the list.
    df = df.groupby('ics').filter(lambda x: len(x) > 10)
    stop = set(stopwords.words('english'))
    for item in df.itertuples():
        """This is where you customize your tokenizer and seprate labels and text,
        defining your Xs and Ys"""
        if "foreword" == item.sections[0].split()[0].lower():
            item.sections = item.sections[1:]
        if not item.ics or not item.sections or len(' '.join(item.sections)) < 10:
            continue
        # TODO: Make these parameters for input
        text = item.title + ' ' + ' '.join(item.sections)
        words = word_tokenize(text)
        text_no_stop_words_punct = [t for t in words if t not in stop and t not in string.punctuation]
        wordList = []
        for word in text_no_stop_words_punct:
            wordList.append(word)
        # TODO: Find multiple candidates for standards instead of just one standard.
        field = item.ics[0].split('.')[0:3]
        label = ".".join(field)
        X.append(wordList)
        y.append(label)
        print("* START: *")
        print(wordList)
        print("========================")
        print(field)
        print("* END *")
    return np.array(X), np.array(y)

def benchmark(model, X, y, n):
    """
    Divide into training and test data sets, train, then evaluate the score.
    """
    test_size = 1 - (n / float(len(y)))
    scores = []
    for train, test in StratifiedShuffleSplit(y, n_iter=5, test_size=test_size):
        print('.', end='')
        X_train, X_test = X[train], X[test]
        y_train, y_test = y[train], y[test]
        scores.append(accuracy_score(model.fit(X_train, y_train).predict(X_test), y_test))
    return np.mean(scores)

def plot(df):
    """Graph results from the pickled scores"""
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