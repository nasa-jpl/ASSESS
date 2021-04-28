# Automatic Semantic Search Engine for Suitable Standards

## Getting Started

There are a few main components to ASSESS:

- A React front-end
- A FastAPI server
- An Elastcisearch server with 3 data indices (main index, system logs, and user statistics)
- Kibana for viewing data

`docker-compose.yml` shows the software stack. You can run the stack using `docker-compose up -d`. Please note, you need the Elasticsearch index data in order to actually have these components working.

Make sure you edit `api/conf.yaml` with the correct server/port locations for elasticsearch.

To understand the backend code, look at the API in [main.py](https://github.com/nasa-jpl/ASSESS/blob/master/api/main.py)

## Testing the stack

You can test the Rest API with [assess_api_calls.py](https://github.com/nasa-jpl/ASSESS/blob/master/api/assess_api_calls.py)
