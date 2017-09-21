import dill
from textblob import TextBlob
import math
x=float('nan')
math.isnan(x)

def get_cosine(vec1, vec2):
    import math

    intersection = set(vec1.keys()) & set(vec2.keys())
    numerator = sum([vec1[x] * vec2[x] for x in intersection if not (math.isnan(float(vec1[x])) or math.isnan(float(vec2[x]))) ])
    product={x:vec1[x] * vec2[x] for x in intersection if not (math.isnan(float(vec1[x])) or math.isnan(float(vec2[x]))) }
    sum1 = sum([vec1[x] ** 2 for x in vec1.keys()])
    sum2 = sum([vec2[x] ** 2 for x in vec2.keys()])

    denominator = math.sqrt(sum1) * math.sqrt(sum2)

    if denominator==0 or math.isnan(float(denominator)):
        return 0.0,{}
    else:
        return float(numerator) / denominator,product

def savemodel(model,outfile):
    with open(outfile, 'wb') as output:
        dill.dump(model, output)
    return ''

def loadmodel(infile):
    model=''
    with open(infile, 'rb') as inp:
        model = dill.load(inp)
    return model

def noun_tokenize(x):
    blob = TextBlob(x)
    phrases = blob.noun_phrases
    return phrases
