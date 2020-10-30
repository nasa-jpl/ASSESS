import ast
import re
import statistics
import string
import dill
import networkx as nx
import numpy as np
import pandas as pd
import plotly.graph_objs as go
import plotly.offline
from sklearn.feature_extraction import text
import spacy

from sklearn.neighbors import NearestNeighbors
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import normalize


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


# ================================= create an graph/tree (DAG)


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

# ================================= plot the positions for each node and edge
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



# ============================== predict/rank

pos=loadmodel('pos_')
graph=loadmodel('graph')

df=pd.read_csv('iso_final_all_clean_text.csv',index_col=0)
df=df[df['type']=='standard'].reset_index(drop=True)
df.fillna('', inplace=True)

tfidftransformer=TfidfVectorizer(ngram_range=(1,1), stop_words=text.ENGLISH_STOP_WORDS.union(Z[:10]))
X=tfidftransformer.fit_transform([m+' '+n for m, n in zip(df['description_clean'], df['title'])]) # using both desc and tile to predict
print('shape', X.shape)

X=normalize(X, norm='l2', axis=1)
nbrs_brute = NearestNeighbors(n_neighbors=X.shape[0], algorithm='brute', metric='cosine')

print('fitting')
nbrs_brute.fit(X.todense())
print('fitted')

# del(X)
# gc.collect()

sow=open('input.txt','r').read()
sow=tfidftransformer.transform([sow])
sow=normalize(sow, norm='l2', axis=1)

print('scoring standards')
distances, indices=nbrs_brute.kneighbors(sow.todense())
distances=list(distances[0])
indices=list(indices[0])

for indx in indices[:10]:
    print(df.iloc[indx]['title'])
    print(df.iloc[indx]['description'])

    to_print=[
              tfidftransformer.get_feature_names()[i]
              +' '+
              str(abs(np.array(sow[0].todense()).flatten()[i] - np.array(X[indx].todense()).flatten()[i]))
                 for i in set(sow.indices).intersection(X[indx].indices)]
    print(' || ' .join(to_print),'\n')


print('scored standards')






# =====================================================, add and aggregate scores in the graph
# recursively accumulate scores (mean, std, max, median) and create data structures for plotting

Xn=[]
Yn=[]
labels=[]
values=[]
hoverlabels=[]
filtered_nodes=set()
Xe=[]
Ye=[]
title_lookup = nx.get_node_attributes(graph, 'title')
type_lookup = nx.get_node_attributes(graph, 'type')


def examine(node, parent_node):
    global Xn, Yn, labels, values, hoverlabels, Xe, Ye, pos, filtered_nodes, df, graph, title_lookup, indices, distances

    neighbours = [n for n in graph.neighbors(node)]
    scores=[]

    if len(neighbours)==0:
        # check if leaf node: if score available send it up, or send a zero
        index_found=-1
        try:
            index_found=indices.index(df[df['id_']==node].index[0])
        except:
            pass

        if index_found!=-1:
            # check if a score available
            if 1-distances[index_found]!=0:
                # score=math.pow(100, -distances[index_found]) # convert to exponential scale to spread the higher values
                score=1-distances[index_found]
            else:
                score=0
            return score
        else:
            return 0


    # dive deeper if not the terminal node
    for neighbour in neighbours:
        scores.append(examine(neighbour, node))


    if len(scores)==0:
        mean=0
    else:
        scores=list(filter(lambda num: num != 0, scores)) # remove zeros and then calculate mean
        if len(scores)!=0:
            mean=statistics.mean(scores)
        else:
            mean=0

    if mean!=0 and type_lookup.get(node,'~')!='subgroup':
        # activate plotly nodes and edges
        Xn += [pos[node][0]]
        Yn += [pos[node][1]]

        if node!='~-1': # no need to connect the root node to its parent
            Xe += [pos[parent_node][0], pos[node][0], None]
            Ye += [pos[parent_node][1], pos[node][1], None]

        values += [mean]
        title = title_lookup.get(node,'')
        hoverlabels += [str(title)+"  "+str(round(mean, 3))]

    return mean

print('scoring categories and plotting')
examine('~-1', '~-2')






# ================================== plot the tree

fig = go.Figure()
fig.add_trace(go.Scatter(x=Xe,
                   y=Ye,
                   mode='lines',
                   line=dict(color='rgb(210,210,210)', width=1),
                   ))
fig.add_trace(go.Scatter(x=Xn,
                  y=Yn,
                  mode='markers+text',
                  name='graph',
                  marker=dict(symbol='circle-dot',
                                size=18,
                                line=dict(color='rgb(50,50,50)', width=1),
                              color=values,
        colorbar=dict(
            title="Colorbar"
        ),
                colorscale='Blues',
                # reversescale=True
                # colorscale=[[0, "rgb(255,255,255)"],
                # [0.2, "rgb(202, 207, 210)"],
                # [0.1, "rgb(255, 160, 122)"],
                # [0.95, "rgb(205, 92, 92)"],
                # [1, "rgb(31,120,180)"]]
                                ),
                # text=labels,
    hovertext=hoverlabels,
    hoverinfo="text",
                  opacity=0.8,
textposition="bottom center"
                  ))

plotly.offline.plot(fig, filename='plot.html_')
