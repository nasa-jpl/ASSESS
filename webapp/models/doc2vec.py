from gensim.models.doc2vec import Doc2Vec, TaggedDocument, LabeledSentence 
import pandas as pd
from random import shuffle
from scipy.spatial.distance import cosine

df=pd.read_csv('../standards/IEEE-standards_rev1.csv',index_col=0)

def collect(row):
        res=''
        for field in ['abstract_new','purpose_new','scope_new']:
            res+=' '+str(row[field])
        return res

data = df.apply(collect, axis = 1)

#TODO: implement with from disk streaming
class LabeledLineSentence(object):
	def __init__(self, doc_list, labels_list):
		self.labels_list = labels_list
		self.doc_list = doc_list
	def __iter__(self):
		shuffle(self.labels_list)
		for idx in self.labels_list:
			#TODO: test with spaCy tokenizer as well
			yield TaggedDocument(self.doc_list[idx].split(), [idx])

doc_labels = list(df.index.values)

doc_iterator = LabeledLineSentence(data, doc_labels)

model = Doc2Vec(vector_size = 100, window = 10, min_count = 5, workers = 8,
							alpha = 0.025, min_alpha = 0.015) #just threw in some params for now

model.build_vocab(doc_iterator)

model.train(doc_iterator, total_examples = model.corpus_count, epochs = 10)
	
model.save("trained_models/Doc2Vec_test")

#sanity check: The vector the model infers for an example in the training data should 
#should have a cosine similarity with the stored vector very close to 1

test = data[0]
p = model[0]
q = model.infer_vector(test.split())
dissimilarity = cosine(p,q)
similarity = (dissimilarity - 1)*(-1)
print(similarity)