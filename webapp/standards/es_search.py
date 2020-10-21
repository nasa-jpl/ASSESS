from elasticsearch import Elasticsearch 
import json
from elasticsearch_dsl import Search
import requests


es = Elasticsearch(["172.19.0.2"])
es_index = "iso_final_clean"
search = Search(using=es)

def search_test(uri, term):
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


def client_search(searchq, n):
    return es.search(index=es_index, body={"query": {"match": {"description":searchq}, size=n)


def search_by_text(searchq):
    res = es.search(index=es_index, body={"query": {"match": {"description":searchq}}})
    print("Got %d Hits:" % res['hits']['total']['value'])
    results = {}
    for num, hit in enumerate(res['hits']['hits']):
        results[num+1] = hit["_source"]
    json_object = json.dumps(results, indent=4)
    return json_object

def search_by_id(searchq):
    res = es.search(index=es_index, body={"query": {"match": {"num_id":searchq}}})
    print("Got %d Hits:" % res['hits']['total']['value'])
    results = {}
    for num, hit in enumerate(res['hits']['hits']):
        results[num+1] = hit["_source"]
    json_object = json.dumps(results, indent=4)
    return json_object


#client_search('localhost:9200/test-csv', 'airplanes')
print(search_by_text("machine"))
print(search_by_id("22"))
print(client_search("test", 3))
