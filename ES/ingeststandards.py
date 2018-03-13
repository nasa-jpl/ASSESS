import pandas as pd
from pandas.io.tests.parser import index_col
import sys
reload(sys)
sys.setdefaultencoding('UTF8')
import traceback
import json

def checknan(val):
    if str(val)=='nan':
        return True
    return False

def iso():
    all_global_fields = ['standard_id', 'title', 'publisher', 'ics', 'url', 'current_status', 'publication_date',
                         'number_of_pages', 'edition', 'abstract', 'purpose', 'introduction', 'keywords',
                         'crawl_datetime']

    local_blacklist = []

    int_fields = ['Year', 'number_of_pages']


def ieee():

    all_global_fields=['standard_id','title','publisher','ics','url','current_status','publication_date',
                       'number_of_pages','edition','abstract','purpose','introduction','keywords','crawl_datetime']

    local_blacklist=[]

    int_fields=['Year','number_of_pages']

    ## get the mapping file that maps local to global schema

    schemafile='ieee_schema.csv'
    schema=pd.read_csv('schemas/'+schemafile,index_col=0)
    global_to_local={}

    for index,row in schema.iterrows():
        global_to_local[row['global']]=row['local']



    ## read the data
    data = pd.read_csv('../webapp/standards/IEEE-standards_rev1.csv', index_col=0)

    uid=0

    for index,row in data.iterrows():

        # create a flattened object with local schema

        row=dict(row)

        ## convert the local to global


        # the local fields that are in the *_schema.csv will be changed to global names.
        # the ones that say derived : the values will be derived from other local fields.

        for global_field in global_to_local.keys():
            local_field=global_to_local[global_field]
            value=''
            if local_field=='derived':
                if global_field=='number_of_pages':
                    if not checknan(row['End Page']) and not checknan(row['Start Page']):
                        try:
                            value= int(row['End Page']) - int(row['Start Page']) + 1
                        except:
                            value=0
                if global_field=='keywords':
                    if not checknan(row['Author Keywords']):
                        value =row['Author Keywords'].split(';')
                if global_field=='crawl_datetime':
                    value='2017-09-01' # format : yyyy-MM-dd
                if global_field=='publication_date':
                    if not checknan(row['Date Added To Xplore']):
                        value=str(row['Date Added To Xplore'])
                        value=value[0:4]+'-'+value[4:6]+'-'+value[6:8]
                row[global_field] = value
            else:
                value = row[local_field]
                row.pop(local_field, None)
                row[global_field] = value


        # the left out global fields will be added with a value: 'N/A'

        for global_field in set(all_global_fields)-set(global_to_local.keys()):
            value='N/A'
            row[global_field]=value

        # blacklist some fields from the local

        for local_field in local_blacklist:
            row.pop(local_field,None)

        # deal with missing values for final set of fields and fix encodings for strings

        for field in row.keys():
            if checknan(row[field]):
                if field in int_fields:
                    row[field]=0
                else:
                    row[field]='N/A'
            else:
                # correct the utf
               if isinstance(row[field], basestring):
                    row[field]=row[field].decode('utf-8',errors='ignore')
                    # json.dumps({'test':row[field]})
        # use a unique ID and and push to the elastic search

        uid+=1

        yield str(uid)+'_ieee', row



# ingest ieee standards
from elasticsearch import Elasticsearch
es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
index='assess_standards'

for uid, doc in ieee():
    res=''
    try:
        res = es.index(index=index, doc_type='standard', id=uid, body=doc)
    except:
        print str(traceback.print_exc())
        print res
        print doc
        raise Exception('read it and solve it!')


