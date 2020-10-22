from webapp.text_analysis.utils.hplotprecdict import *
from webapp.text_analysis.utils.utils import *
import pandas as pd
import os

models_dir='../models/'
standards_dir='../standards/data/'
data_dir='data/'
output_dir='output/'
temp_dir='temp/'

pos = loadmodel(models_dir + 'pos_')
graph = loadmodel(models_dir + 'graph')
text_sow=open(data_dir+'test_input_sow_text.txt','r').read()

standards_df = pd.read_csv(os.path.join(standards_dir, 'iso_final_all_clean_standards_text_w_elmo.csv'), index_col=0)
standards_df = standards_df[standards_df['type'] == 'standard'].reset_index(drop=True)
standards_df.fillna('', inplace=True)
standards_df['id']=standards_df.index

def print_items(inpt):
    for item in inpt:
        print(item[0], '||', item[1])

field_predictions_collect={}
print('starting to predict (bottom up)')
field_predictions=bottom_up_hpredict(text_sow, standards_df, pos, graph, algo='cosine-sim', plot_name=output_dir+'cosine_sim_hcat.html')
field_predictions_collect['cosine-sim']=field_predictions
print_items(field_predictions)
field_predictions=bottom_up_hpredict(text_sow, standards_df, pos, graph, algo='elmo-sim', plot_name=output_dir+'elmo_sim_hcat.html')
field_predictions_collect['elmo-sim']=field_predictions
print_items(field_predictions)
field_predictions=bottom_up_hpredict(text_sow, standards_df, pos, graph, algo='glove-sim', plot_name=output_dir+'glove_sim_hcat.html')
field_predictions_collect['glove-sim']=field_predictions
print_items(field_predictions)
field_predictions=bottom_up_hpredict(text_sow, standards_df, pos, graph, algo='w2v-sim', plot_name=output_dir+'w2v_sim_hcat.html')
field_predictions_collect['w2v-sim']=field_predictions
print_items(field_predictions)
savemodel(field_predictions_collect, 'field_predictions_collect')
exit()

"""
Todos: 
-get top 50 from each type of recall algo, combine them and then create a heatmap for correlations between all the algorithms (recall and rerank)
-also, find heat map of rankings of the categories for the recall algorithms
-should we also try to remove the min/max from the vector glove and w2v

--do the heatmaps for categories (4 algorithms)
--have a T-SNE for all the standards with their vectors (for fast 4 algorithms). Color based on categories and see which ones make most sense.
- complete the code below and create heatmaps for 7 algorithms

- wmd calculations for the 7 algorithms are very slow. So we can use soft cosine. Implement it, since we cannot use the implementations
 already there as they will not work for elmo.
"""

import plotly.graph_objects as go
from plotly.offline import plot
from scipy import stats

field_predictions_collect=loadmodel('field_predictions_collect')
algorithms=list(field_predictions_collect.keys())
for algo in algorithms:
    rankings=[item[1] for item in sorted(field_predictions_collect[algo], key=lambda x: x[0], reverse=True)]
    field_predictions_collect[algo]=rankings

result_matrix=np.zeros(shape=(len(algorithms),len(algorithms)))

for i, algo_a in enumerate(algorithms):
    for j, algo_b in enumerate(algorithms):
        if algo_a==algo_b:
            result_matrix[i][j]=1
        else:
            tau, p_value = stats.weightedtau(field_predictions_collect[algo_a], field_predictions_collect[algo_b])
            result_matrix[i][j] = tau


fig = go.Figure(data=go.Heatmap(
                   z=result_matrix,
                   x=algorithms,
                   y=algorithms,
                    colorscale='aggrnyl',
reversescale=True))

plot(fig, filename=output_dir+'categorical_rankin_heatmap.html')
exit()

import plotly.express as px
from sklearn.manifold import TSNE
from plotly.offline import plot

vec_types=['elmo','w2v','glove']
for vec in vec_types:
    standards_df_mod=get_paragraph_vectors(standards_df, vec)
    X = np.array(list(standards_df_mod[vec]))
    print('data shape', X.shape)

    X_embedded = TSNE(n_components=2).fit_transform(X)
    standards_df_mod['x_axis'] = X_embedded[:, 0]
    standards_df_mod['y_axis'] = X_embedded[:, 1]

    fig = px.scatter(standards_df_mod, x='x_axis', y='y_axis', color="field")
    plot(fig, filename=output_dir+'T_SNE_'+vec+'.html')

exit()

# collect top n Ids from each fast algorithm
collect_results={}
results_count=50
algos=['cosine-sim', 'elmo-sim', 'w2v-sim', 'glove-sim']
for algo in algos:
    ids, distances, _, _= get_similar_standards(text_sow, standards_df, algo=algo)
    collect_results[algo]=(ids[:results_count],distances[:results_count])
    print(ids, distances)

savemodel(collect_results, temp_dir+'collect_results')
exit()


collect_results=loadmodel(temp_dir+'collect_results')
# merge all the Ids and rank using all slow and fast algorithms
all_ids=[]
for k,v in collect_results.items():
    ids=v[0]
    all_ids+=ids

standards_df_top=standards_df[standards_df['id'].isin(all_ids)]
standards_df_top=standards_df_top.reset_index()

collect_results_2={}
algos=['w2v-wmd-sim', 'elmo-wmd-sim', 'glove-wmd-sim', 'cosine-sim', 'elmo-sim', 'w2v-sim', 'glove-sim']
for algo in algos:
    ids, distances, _, _= get_similar_standards(text_sow, standards_df_top, algo=algo)
    collect_results_2[algo]=(ids, distances)
    print(ids, distances)

savemodel(collect_results_2, temp_dir+'collect_results_2')
exit()


# calculate pairwise (for each pair of algorithms) correlations of the rankings:
import plotly.graph_objects as go
from plotly.offline import plot
from scipy import stats


collect_results_2=loadmodel(temp_dir+'collect_results_2')
algorithms=list(collect_results_2.keys())

for algo in algorithms:
    rankings=[item[1] for item in sorted(zip(collect_results_2[algo][0], collect_results_2[algo][1] ), key=lambda x: x[0])]
    collect_results_2[algo]=rankings

result_matrix=np.zeros(shape=(len(algorithms), len(algorithms)))

for i, algo_a in enumerate(algorithms):
    for j, algo_b in enumerate(algorithms):
        if algo_a==algo_b:
            result_matrix[i][j]=1
        else:
            tau, p_value = stats.weightedtau(collect_results_2[algo_a], collect_results_2[algo_b])
            result_matrix[i][j] = tau
            print(tau, algo_a, algo_b)


fig = go.Figure(data=go.Heatmap(
                   z=result_matrix,
                   x=algorithms,
                   y=algorithms,
                    colorscale='aggrnyl',
                    reversescale=True))

plot(fig, filename=output_dir+'algorithms_comparison_heatmap.html')
exit()

"""
Note: the results above show that elmo-sim is most similar to elmo-wmd-sim, giving some confidence for having this as a recall algorithm.
-Think about an two step algorithm. Use fast to get to an area and then do slow matches to find related ones around!!
"""