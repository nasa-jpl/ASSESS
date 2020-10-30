"""
This is code to do analysis of standard/text retrieval based on hierarchical categorization
"""

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



def savemodel(model, outfile):
    with open(outfile, 'wb') as output:
        dill.dump(model, output)
    return ''


def loadmodel(infile):
    with open(infile, 'rb') as inp:
        model = dill.load(inp)
    return model

models_dir='../../models/'
data_dir='../../standards/data/'
input_dir='../../SOW_txts/'
output_dir='../../output/'
input_file='../data/test_input_sow_text.txt'

# ============================== predict/rank all the standards (last level of the tree)
# and show the top ranking ones

df=pd.read_csv(data_dir+'iso_final_all_clean_text.csv',index_col=0)
df=df[df['type']=='standard'].reset_index(drop=True)
df.fillna('', inplace=True)

tfidftransformer=TfidfVectorizer(ngram_range=(1,1), stop_words=text.ENGLISH_STOP_WORDS)
X=tfidftransformer.fit_transform([m+' '+n for m, n in zip(df['description_clean'], df['title'])]) # using both desc and tile to predict
print('shape', X.shape)

X=normalize(X, norm='l2', axis=1)
nbrs_brute = NearestNeighbors(n_neighbors=X.shape[0], algorithm='brute', metric='cosine')

print('fitting')
nbrs_brute.fit(X.todense())
print('fitted')

# del(X)
# gc.collect()

sow=open(input_file,'r').read()
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


# ===================================================== recursively accumulate scores in the graph (mean, std, max, median)
# and create data structures for plotting

pos=loadmodel(models_dir+'pos_')
graph=loadmodel(models_dir+'graph')


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
# field_lookup=nx.get_node_attributes(graph,'field')

field_predictions={}
field_title_mapping={}

def examine(node, parent_node):
    global field_predictions, Xn, Yn, labels, values, hoverlabels, Xe, Ye, pos, filtered_nodes, df, graph, title_lookup, indices, distances

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
        if type_lookup.get(node,'~')=='field':
            field_predictions[title]=mean
            # field_title_mapping[field_lookup.get(node,'~')]=title

    return mean

print('scoring categories (at multiple levels) and plotting')
examine('~-1', '~-2')

# for k,v in field_title_mapping.items():
#     print(k,'||',v)

# ==================== Predict the Fields or the ICS based Standard Category (Top layer of the tree) based on bottom up aggregation of scores

print('Ranking the \'Fields\' (Top layer of the tree) based on bottom up aggregations')
# output_f=open(output_dir+input_file,'w')
for item in sorted(field_predictions.items() ,  key=lambda x: x[1], reverse=True):
    print(item)
    # output_f.write(str(item[0])+'||'+str(item[1])+'\n')
# output_f.close()

# ================================== plot the tree along with aggregated scores
# (a heat-map based on the scores for each node)

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