# first do this: https://www.elastic.co/guide/en/elasticsearch/reference/current/docker.html#docker-cli-run
# https://tryolabs.com/blog/2015/02/17/python-elasticsearch-first-steps/
# https://www.elastic.co/guide/en/elasticsearch/reference/current/settings.html

import requests
res = requests.get('http://localhost:9200')
print(res.content)

import datetime

from elasticsearch import Elasticsearch
es = Elasticsearch([{'host': 'localhost', 'port': 9200}])


doc = {
    'author': 'kimchy',
    'text': 'Elasticsearch: cool. bonsai cool.',
}

res = es.index(index="test-index", doc_type='tweet', id='1', body=doc)
print res

res = es.get(index="test-index", doc_type='tweet', id='1')
print(res['_source'])

es.indices.refresh(index="test-index")

res = es.search(index="test-index", body={"query": {"match_all": {}}})
print res
