"""
create ELMO vectors for all the standards and save it: use multi-threading to make it fast
"""
import pandas as pd
import os
from webapp.text_analysis.elmo_util import *
import dask.dataframe as dd
import multiprocessing
import time


# standards_dir = '../standards/data'
# df=dd.read_csv(os.path.join(standards_dir,'iso_final_all_clean_text.csv')) # df=pd.read_csv(os.path.join(standards_dir,'iso_final_all_clean_text.csv'), index_col=0)
# df=df.compute()
# df=dd.from_pandas(df, npartitions=2*multiprocessing.cpu_count())
# df=df[df['type']=='standard'].reset_index(drop=True)
# df=df.fillna('')
# df=df.map_partitions(lambda df: df.assign(usable_text=df['description_clean'] +' ' + df['title'])).compute()
# df=df.head(1000)
# df=df.reset_index()
# df_=df['usable_text']
# df_=df_.reset_index()
# start = time.process_time()
# # https://stackoverflow.com/questions/40019905/how-to-map-a-column-with-dask
# df_=dd.from_pandas(df_, npartitions=2*multiprocessing.cpu_count())
# df['elmo']=df_.usable_text.map(lambda usable_text: give_paragraph_elmo_vector(usable_text), meta=('usable_text', str)).compute() # df['elmo'] = df.apply(lambda row: give_paragraph_elmo_vector(row['usable_text']) , axis=1)
# print(time.process_time() - start)
# df.to_csv(os.path.join(standards_dir,'iso_final_all_clean_text_w_elmo.csv'))

# the above code used dask to parallelize the operations for calculating elmo vectors. But this still uses the tf_hub on a paragraph basis. We can try one shot:
    # -- sent-tokenize the paragraphs and maintain an array to track which sentences belong to which data points.
    # -- give all sents at once to the tf_hub and extract the tokens then
    # -- implemented the above in the elmo_utils.py


standards_dir = '../standards/data'
df=dd.read_csv(os.path.join(standards_dir,'iso_final_all_clean_text.csv')) # df=pd.read_csv(os.path.join(standards_dir,'iso_final_all_clean_text.csv'), index_col=0)
df=df.compute()
df=dd.from_pandas(df, npartitions=2*multiprocessing.cpu_count())
df=df[df['type']=='standard'].reset_index(drop=True)
df=df.fillna('')
df=df.map_partitions(lambda df: df.assign(usable_text=df['description_clean'] +' ' + df['title'])).compute()
# df=df.head(100)
# df=df.reset_index()
df_splits = np.array_split(df, 31)

for df_split in df_splits:
    start = time.process_time()
    df_split['elmo'] = give_paragraph_elmo_vector_multi(list(df_split['usable_text']))
    print(time.process_time() - start)
df=pd.concat(df_splits)
df.to_csv(os.path.join(standards_dir,'iso_final_all_clean_standards_text_w_elmo.csv'))
# merge all the splits now
