from elasticsearch import Elasticsearch 
import json
from elasticsearch import Elasticsearch
import requests


es = Elasticsearch()

def search(uri, term):
    """Simple Elasticsearch Query"""
    query = json.dumps({
        "query": {
            "match": {
                "content": term
            }
        }
    })
    response = requests.get(uri, data=query)
    results = json.loads(response.text)
    return results


def client_search(index, searchq):
    res = es.search(index=index, body={"query": {"match": {"content": searchq}}})
    print(res)
    print("%d documents found" % res['hits']['total'])
    for doc in res['hits']['hits']:
        print(doc['_source']['content'])

def search_by_text(index, searchq):
    res = es.search(index=index, body={"query": {"match": {"description":searchq}}})
    print("Got %d Hits:" % res['hits']['total']['value'])
    for hit in res['hits']['hits']:
        return(hit["_source"])
    #print(len(res["hits"]["hits"]))

def search_by_id(index, searchq):
    res = es.search(index=index, body={"query": {"match": {"num_id":searchq}}})
    print("Got %d Hits:" % res['hits']['total']['value'])
    for hit in res['hits']['hits']:
        return(hit["_source"])
    #print(len(res["hits"]["hits"]))


#client_search('localhost:9200/test-csv', 'airplanes')
print(search_by_text("test-csv", "machine"))
print(search_by_id("test-csv", "22"))

