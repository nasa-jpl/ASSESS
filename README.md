# Automatic Semantic Search Engine for Suitable Standards 

## Getting Started
There are a few main components ASSESS provides:
- React front-end applications
- Fast API server
- Elastcisearch server with data indices
- Redis server for quick in-memory storage of user data

`docker-compose.yml` shows the software stack. You can connect to the stack using `docker-compose up`

Make sure you edit `conf.yaml` with the correct server/port locations for elasticsearch, as well as the correct index.

## Testing the stack
You can test the Rest API with `assess_api_calls.py`

If running locally, open `http://0.0.0.0:3000` with your web browser and then upload a SoW to extract standard references and suitable standards.