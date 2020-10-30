"""
This is code to prepare for the analysis of standard/text retrieval based on hierarchical categorization
"""

import ast
import re
import string
import dill
import networkx as nx
import pandas as pd
from sklearn.feature_extraction import text
import spacy


nlp = spacy.load('en')

def to_string(ar):
    return str(ar)


def to_array(sr):
    return ast.literal_eval(sr)


def savemodel(model, outfile):
    with open(outfile, 'wb') as output:
        dill.dump(model, output)
    return ''


def loadmodel(infile):
    with open(infile, 'rb') as inp:
        model = dill.load(inp)
    return model


def hasNumbers(str):
    return bool(re.search(r'\d', str))


def ispun(str):
    if str in string.punctuation:
        return True
    else:
        return False


def clean_ngram(doc):
    global nlp

    stop_words = text.ENGLISH_STOP_WORDS
    for w in nlp(doc):
        if w.ent_type_ not in ['DATE', 'TIME', 'GPE', 'PERSON', 'CARDINAL'] and not hasNumbers(
                w.text) and not ispun(w.text) and w.text not in stop_words and w.pos_ == 'NOUN':
                    yield w.lemma_.lower()





def hierarchy_pos(G, root, levels=None, width=1., height=1.):
    '''If there is a cycle that is reachable from root, then this will see infinite recursion.
       G: the graph
       root: the root node
       levels: a dictionary
               key: level number (starting from 0)
               value: number of nodes in this level
       width: horizontal space allocated for drawing
       height: vertical space allocated for drawing'''
    TOTAL = "total"
    CURRENT = "current"
    def make_levels(levels, node=root, currentLevel=0, parent=None):
        """Compute the number of nodes for each level
        """
        if not currentLevel in levels:
            levels[currentLevel] = {TOTAL : 0, CURRENT : 0}
        levels[currentLevel][TOTAL] += 1
        neighbors = list(G.neighbors(node))
        for neighbor in neighbors:
            if not neighbor == parent:
                levels =  make_levels(levels, neighbor, currentLevel + 1, node)
        return levels

    def make_pos(pos, node=root, currentLevel=0, parent=None, vert_loc=0):
        dx = 1/levels[currentLevel][TOTAL]
        left = dx/2
        pos[node] = ((left + dx*levels[currentLevel][CURRENT])*width, vert_loc)
        levels[currentLevel][CURRENT] += 1
        neighbors = G.neighbors(node)
        for neighbor in neighbors:
            if not neighbor == parent:
                pos = make_pos(pos, neighbor, currentLevel + 1, node, vert_loc-vert_gap)
        return pos
    if levels is None:
        levels = make_levels({})
    else:
        levels = {l:{TOTAL: levels[l], CURRENT:0} for l in levels}
    vert_gap = height / (max([l for l in levels])+1)
    return make_pos({})


# ================================= create an graph/tree (DAG) using the data in csv


df=pd.read_csv('iso_final_all.csv',index_col=0)
ics_dict_general=loadmodel('ics_dict_general')

graph = nx.DiGraph()
for k, v in ics_dict_general.items():
    for v_ in v:
        graph.add_edge(k, v_)
        entry = df[df['id_'] == k].values
        info={}
        if len(entry) != 0:
            info={key:val for key, val in zip(df.columns, entry[0])}
        nx.set_node_attributes(graph, {k: info})

        entry = df[df['id_'] == v_].values
        info = {}
        if len(entry) != 0:
            info = {key: val for key, val in zip(df.columns, entry[0])}
        nx.set_node_attributes(graph, {v_: info})

savemodel(graph,'graph')
# print(graph.nodes(data=True))

# ================================= plot the positions for each node and edge (hierarchical plot)
pos = hierarchy_pos(graph,'~-1')
savemodel(pos,'pos_')
# print(pos)

exit()


# ============================== clean the descriptions and add to the csv
df=pd.read_csv('iso_final_all.csv',index_col=0)
df.fillna('', inplace=True)
df['description_clean'] = df['description'].apply(lambda x: ' '.join(clean_ngram(x)))
df.to_csv('iso_final_all_clean_text.csv')
exit()


