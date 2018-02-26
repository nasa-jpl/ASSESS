from classify import Classify
from trainer import Trainer, Word2Vec, DemoClass
import pandas as pd
import os

def build(data, model):
    """Build a model using training data."""
    model = DemoClass(data)
    return model.demo_function()

def transform(text, dir=None):
    """Given a text, transform to prepare for training."""
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
    return text_all


raw_data = """Lorem ipsum dolor sit amet, consectetuer adipiscing elit. 
Aenean commodo ligula eget dolor. Aenean massa. Cum sociis natoque penatibus et 
magnis dis parturient montes, nascetur ridiculus mus. Donec quam felis, ultricies 
nec, pellentesque eu, pretium quis, sem."""
#training_data = transform(raw_data)
model = build(raw_data, "demo")
print model
