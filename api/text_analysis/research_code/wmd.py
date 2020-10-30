"""
This is research code to try out Word Mover's Distance implementations

"""

# ======================================================================================================================
## load word2vec model
# ======================================================================================================================

# sentence_A = 'Obama speaks to the media in Illinois'
# sentence_B = 'The president greets the press in Chicago'

# sentence_A = 'american bank is the best financial institution'
sentence_B = 'bank of this river is overflowing'
sentence_A = 'bank has agreed to give us money'

def preprocess(sentence, model):
    return [item for item in sentence.lower().split() if item in model]

import gensim.downloader as api
model = api.load('word2vec-google-news-300')

# print(model['president'])


sentence_A = preprocess(sentence_A, model)
sentence_B = preprocess(sentence_B, model)

# ======================================================================================================================
## WMD Using Gensim
# ======================================================================================================================

# distance = model.wmdistance(sentence_obama, sentence_president)
# print('distance = %.4f' % distance)
# sentence_orange = preprocess('Oranges are my favorite fruit')
# distance = model.wmdistance(sentence_obama, sentence_orange)
# print('distance = %.4f' % distance)
#
# exit()


# ======================================================================================================================
## WMD Using PulP solver
# ======================================================================================================================
from api.text_analysis.wmd_util import *

print('stated calculating wmd....')
prob = word_mover_distance_probspec(sentence_A, sentence_B, model)
print(pulp.value(prob.objective))
for v in prob.variables():
    if v.varValue!=0:
        print(v.name, '=', v.varValue)



