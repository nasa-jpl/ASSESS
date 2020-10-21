from elasticsearch import Elasticsearch 
import json
from elasticsearch import Elasticsearch
import requests


es = Elasticsearch(["172.19.0.2"])
es_index = "iso_final_clean"

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


def client_search(searchq):
    res = es.search(index=es_index, body={"query": {"match": {"content": searchq}}})
    print(res)
    print("%d documents found" % res['hits']['total'])
    for doc in res['hits']['hits']:
        print(doc['_source']['content'])

def search_by_text(index, searchq):
    res = es.search(index=index, body={"query": {"match": {"description":searchq}}})
    print("Got %d Hits:" % res['hits']['total']['value'])
    results = {}
    for num, hit in enumerate(res['hits']['hits']):
        results[num+1] = hit["_source"]
    json_object = json.dumps(results, indent=4)
    return json_object

def search_by_id(index, searchq):
    res = es.search(index=index, body={"query": {"match": {"num_id":searchq}}})
    print("Got %d Hits:" % res['hits']['total']['value'])
    results = {}
    for num, hit in enumerate(res['hits']['hits']):
        results[num+1] = hit["_source"]
    json_object = json.dumps(results, indent=4)
    return json_object


#client_search('localhost:9200/test-csv', 'airplanes')
print(search_by_text("machine"))
print(search_by_id("22"))

