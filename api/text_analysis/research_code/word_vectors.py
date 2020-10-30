from gensim.models import KeyedVectors

# convert the Glove file format to w2v format
from gensim.scripts.glove2word2vec import glove2word2vec
glove_input_file = 'glove.6B.300d.txt'
word2vec_output_file = 'glove.6B.300d.txt.word2vec'
glove2word2vec(glove_input_file, word2vec_output_file)
exit()

filename = 'GoogleNews-vectors-negative300.bin'
model_w2v = KeyedVectors.load_word2vec_format(filename, binary=True)
# load the Stanford GloVe model
filename = 'glove.6B.100d.txt.word2vec'
model_glove = KeyedVectors.load_word2vec_format(filename, binary=False)