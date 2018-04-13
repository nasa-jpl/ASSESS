import numpy as np
from nltk.corpus import stopwords
import string
import dill as pickle
import processes


# Vectorize input
X, y = [], []
text = """
The program is establishing a federated enterprise information sharing architecture for data sharing and decision support tools for cross‐organizational collaboration that is cost effective and adaptable for current and future technologies. As shown in the figure below, the program is focused on technologies with a nexus to the land domain which are interoperable with other data sources and decision support tools.
The core technology is being leveraged from an S&T coastal situational awareness project, reducing the lifecycle cost and risk while also enabling information sharing across border domains (i.e. land, coastal).
The program is pursuing a mix of government‐of‐the‐shelf (GOTS) and Homeland Security Industrial Base decision support tools as a risk pooling strategy that manages cost and ensures some capability is delivered while also making some investments in innovative, higher risk technologies.
"""
tokens = processes.tokenizer(text)
X.append(tokens)
X, y = np.array(X), np.array(y)
print(X)

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

