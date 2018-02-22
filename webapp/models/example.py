from classify import Classify
from trainer import Trainer
import pandas as pd


def benchmark(text, dir, model):
    """Benchmark training model against validation set."""
    df_ieee = pd.read_csv(os.path.join(dir, text), index_col=0)
    df_ieee = df_ieee.reset_index()
    df_ieee = df_ieee.fillna('')
    texts_abs = list(df_ieee['Abstract'])
    texts_scp = list(df_ieee['Scope'])
    texts_pur = list(df_ieee['Purpose'])
    texts_int = list(df_ieee['Introduction'])
    texts_all= []

    for i in range(len(texts_abs)):
        if texts_int[i][:12]=='Introduction':
            texts_int[i]=texts_int[i][12:]
        texts_all.append((texts_abs[i] + texts_scp[i] + texts_pur[i]+texts_int[i]).decode('utf-8','ignore'))

    df_ieee['Introduction']=texts_int


ieee_standards = 'IEEE-standards_rev1.csv'
standards_dir = 'standards'
benchmark(text=ieee_standards, dir=standards_dir)
