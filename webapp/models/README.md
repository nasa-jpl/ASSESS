# The current pipeline

Currently we are benchmarking the performance of multiple supervised and unsupervised methods using sklearn pipeline:
TODO: Add descriptions and full names 
- "bayes_mult_nb"
- "bayes_mult_nb_tfidf"
- "bayes_bern_nb"
- "bayes_bern_nb_tfidf"
- "svc"
- "svc_tfidf"
- "w2v"
- "w2v_tfidf"
- "glove_small"
- "glove_small_tfidf"
- "glove_big", etree_glove_big"
- "glove_big_tfidf", etree_glove_big_tfidf"



# Running the pipeline
In order to get the pipeline running, you'll need to download and unzip 2 large datasets for the GLOVE training:
```
wget http://nlp.stanford.edu/data/glove.6B.zip
wget http://nlp.stanford.edu/data/glove.840B.300d.zip
```
You'll also need to download some of NLTK's extra libraries:

```
import nltk
nltk.download('punkt')
nltk.download('stopwords')
```