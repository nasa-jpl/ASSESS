# Automatic Semantic Search Engine for Suitable Standards

ASSESS allows you to run an API server that performs document similarity for large troves of text documents as well as manage an application pipeline that allows for ingestion, search, inspection, deletion, training, logging, and editing documents. 

The problem: Given an SoW, the goal is to produce standards that may be related to that SoW. 

To understand the backend code, view the API in [main.py](https://github.com/nasa-jpl/ASSESS/blob/master/api/main.py)
To understand the ML code, view [ml-core.py](https://github.com/nasa-jpl/ASSESS/blob/master/api/ml-core.py)

## Getting Started

There are a few main components to ASSESS:
- A FastAPI server
- An Elastcisearch server with 3 data indices (main index, system logs, and user statistics)
- Kibana for viewing data
- A redis service for in-memory data storage and rate limiting

Make sure you edit `api/conf.yaml` with the correct server/port locations for elasticsearch. `docker-compose.yml` shows the software stack. You can run the stack using `docker-compose up -d`. Please note, you need the corresponding feather data in order to actually have everything working and ingested into Elasticsearch

## Testing the stack
You can test the Rest API with [assess_api_calls.py](https://github.com/nasa-jpl/ASSESS/blob/master/api/scripts/assess_api_calls.py)
