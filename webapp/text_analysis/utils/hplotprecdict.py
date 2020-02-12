import statistics
import networkx as nx
import plotly.graph_objs as go
import plotly.offline
from webapp.text_analysis.utils.retrieve import *



def bottom_up_hpredict(text_input, standards_df, pos, graph, algo='cosine-sim', plot_name='plot.html_'):

    """
    algo: cosine-sim, elmo-sim, glove-sim, w2v-sim
    """

    # ===================================================== recursively accumulate scores in the graph (mean, std, max, median)
    # and create data structures for plotting

    def examine(node, parent_node, indices, distances, Xn,  Yn, Xe, Ye, values, hoverlabels, field_predictions):

        neighbours = [n for n in graph.neighbors(node)]
        scores = []

        if len(neighbours) == 0:
            # check if leaf node: if score available send it up, or send a zero
            index_found = -1
            try:
                index_found = indices.index(standards_df[standards_df['id_'] == node].index[0])
            except:
                pass

            if index_found != -1:
                # check if a score available
                if 1 - distances[index_found] != 0:
                    # score=math.pow(100, -distances[index_found]) # convert to exponential scale to spread the higher values
                    score = 1 - distances[index_found]
                else:
                    score = 0
                return score
            else:
                return 0

        # dive deeper if not the terminal node
        for neighbour in neighbours:
            scores.append(examine(neighbour, node, indices, distances, Xn,  Yn, Xe, Ye, values, hoverlabels, field_predictions))

        if len(scores) == 0:
            mean = 0
        else:
            scores = list(filter(lambda num: num != 0, scores))  # remove zeros and then calculate mean
            if len(scores) != 0:
                mean = statistics.mean(scores)
            else:
                mean = 0

        if mean != 0 and nx.get_node_attributes(graph, 'type').get(node, '~') != 'subgroup':
            # activate plotly nodes and edges
            Xn += [pos[node][0]]
            Yn += [pos[node][1]]

            if node != '~-1':  # no need to connect the root node to its parent
                Xe += [pos[parent_node][0], pos[node][0], None]
                Ye += [pos[parent_node][1], pos[node][1], None]

            values += [mean]
            title = nx.get_node_attributes(graph, 'title').get(node, '')
            hoverlabels += [str(title) + "  " + str(round(mean, 3))]
            if nx.get_node_attributes(graph, 'type').get(node, '~') == 'field':
                field_predictions[title] = mean
                # field_title_mapping[field_lookup.get(node,'~')]=title

        return mean


    # calculate distances between standards and the sow
    indices, distances, _, _= get_similar_standards(text_input, standards_df, algo=algo)

    Xn = []
    Yn = []
    values = []
    hoverlabels = []
    Xe = []
    Ye = []
    # field_lookup=nx.get_node_attributes(graph,'field')

    field_predictions = {}
    # field_title_mapping = {}

    print('scoring categories (at multiple levels) and plotting')
    examine('~-1', '~-2', indices, distances, Xn,  Yn,Xe, Ye, values, hoverlabels, field_predictions)

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

    plotly.offline.plot(fig, filename=plot_name)
    return sorted(field_predictions.items() ,  key=lambda x: x[1], reverse=True)

