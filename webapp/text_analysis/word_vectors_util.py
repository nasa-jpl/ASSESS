from gensim.models import KeyedVectors
import numpy as np

filename = 'GoogleNews-vectors-negative300.bin'
model_w2v = KeyedVectors.load_word2vec_format(filename, binary=True)
# load the Stanford GloVe model
filename = 'glove.6B.300d.txt.word2vec'
model_glove = KeyedVectors.load_word2vec_format(filename, binary=False)

def get_w2v_para(text_tokens, model_type='w2v'):
    "takes as input a list of tokens and returns a single paragraph vector for the whole text"
    # todo: get rid of min and max and see the results!

    model=None
    if model_type=='w2v':
        model=model_w2v
    elif model_type=='glove':
        model=model_glove
    document_vec=[]
    for token in text_tokens:
        if token in model:
            document_vec.append(model[token])
    if len(document_vec)==0:
        return ''
    document_vec=np.array(document_vec)
    document_vec_mean = np.mean(document_vec, axis=0)
    document_vec_max = np.max(document_vec, axis=0)
    document_vec_min = np.min(document_vec, axis=0)
    document_vec = np.concatenate((document_vec_mean, document_vec_max, document_vec_min))
    return list(document_vec)

# text='hello my name is Tom Cat and I am a sever'
# w2_vec=get_w2v_para(text.split(), model_type='w2v')
# print(w2_vec)

