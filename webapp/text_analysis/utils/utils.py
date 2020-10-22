import dill
# from textblob import TextBlob
import math
import spacy
import re
from sklearn.feature_extraction import text

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

nlp = spacy.load('en')
# python3 -m spacy download en_core_web_sm
# python3 -m spacy download en

def hasNumbers(str):
    return bool(re.search(r'\d', str))

def has_non_alpha(str):
    if re.search('[^a-zA-Z]', str)==None:
        return False
    return True

def has_camelcase_alpha(str):
    if len(str)==1:
        return False

    if len(re.findall('[A-Z]', str[1:]))==0:
        return False
    return True


def clean_text(txt, no_pos=True):
    # todo: check again the no_pos logic once
    txt_=[]
    for w in nlp(txt):
        if w.ent_type_ not in ['DATE', 'TIME', 'GPE', 'PERSON', 'CARDINAL', 'ORG', 'LOC'] and\
                not has_non_alpha(w.text) and not has_camelcase_alpha(w.text) and w.text not in text.ENGLISH_STOP_WORDS and (no_pos or w.pos_ not in ['ADV','DET','ADP','X']): # and (w.pos_ == 'NOUN' or w.pos_ == 'VERB'): # and w.text not in stop_words and w.pos_ == 'NOUN':
            txt_.append(w.text)
    return ' '.join(txt_)

# def noun_tokenize(x):
#     blob = TextBlob(x)
#     phrases = blob.noun_phrases
#     return phrases
