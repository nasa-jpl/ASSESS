import os
import json
import subprocess
from sklearn.neighbors import NearestNeighbors
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import normalize
import dill
import pandas as pd
from sklearn.feature_extraction import text
from standard_extractor import find_standard_ref
from text_analysis import extract_prep
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, ORJSONResponse, JSONResponse
from fastapi import FastAPI, File, Form, UploadFile, Request, Body
from fastapi.encoders import jsonable_encoder
import requests
from starlette.requests import Request
from starlette.responses import Response
from pydantic import BaseModel, Field
from elasticsearch import Elasticsearch
from web_utils import connect_to_es, read_logs
from fastapi import FastAPI, HTTPException
from fastapi.logger import logger as fastapi_logger
from logging.handlers import RotatingFileHandler
import logging
from jsonschema import validate
import time

app = FastAPI()
origins = [
    "http://localhost",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Connect to Elasticsearch
es, idx_main, idx_log, idx_stats = connect_to_es()

if not os.path.exists("log"):
    os.makedirs("log")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class Sow(BaseModel):
    text_field: str = Field(example="Airplanes are complex.")


def log_stats(request, data=None, user=None):
    """Log detailed data in JSON for incoming/outgoing API request."""
    client_host = request.client.host
    msg = {}
    # TODO: Log user once authentication is connected.
    # msg["user"] = str(user)
    # request.state.time_started = time.time()
    msg["time_started"] = str(time.time())
    msg["method"] = str(request.method)
    msg["url"] = str(request.url)
    msg["host"] = str(client_host)
    msg["query_params"] = str(request.query_params)
    msg["path_params"] = str(request.path_params)
    msg["headers"] = dict(request.headers)
    msg["data"] = str(data)
    fastapi_logger.info(json.dumps(msg))
    es.index(index=idx_log, body=json.dumps(msg))
    return


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    host = request.url
    recc_text_url = str(host) + "recommend_text"
    recc_file_url = str(host) + "recommend_file"
    extract_url = str(host) + "extract"
    st_info_url = str(host) + "standard_info"
    search_url = str(host) + "search"
    add_url = str(host) + "add_standards"
    content = """
    <html>
        <head>
            <title>ASSESS API</title>
        </head>
        <body>
            <h1>Welcome to the ASSESS API </h1>
            <h2>Functional API Endpoints</h2>
            <p>{recc_text_url}</p>
            <p>{recc_file_url}</p>
            <p>{extract_url}</p>
            <p>{st_info_url}</p>
            <p>{search_url}</p>
            <p>{add_url}</p>
            <br><br><br>
            <h2>Other Links</h2>
            <p>https://assess-old.jpl.nasa.gov</p>
            <p>https://assess-kb.jpl.nasa.gov</p>
            <p>https://assess-api.jpl.nasa.gov/redoc</p>
            <p>https://assess-api.jpl.nasa.gov/docs</p>
        </body>
    </html>""".format(
        recc_text_url=recc_text_url,
        recc_file_url=recc_file_url,
        extract_url=extract_url,
        st_info_url=st_info_url,
        search_url=search_url,
        add_url=add_url,
    )
    return HTMLResponse(content=content, status_code=200)


@app.post("/recommend_text")
async def recommend_text(request: Request, sow: Sow):
    """Recommend standards from input text."""
    in_text = sow.text_field
    prediction = extract_prep.predict(in_text=in_text)
    json_compatible_item_data = jsonable_encoder(prediction)
    log_stats(request, data=in_text)
    return JSONResponse(content=json_compatible_item_data)


@app.post("/recommend_file")
async def recommend_file(request: Request, pdf: UploadFile = File(...)):
    """Recommend standards from PDF."""
    print("File received")
    prediction = extract_prep.predict(file=pdf)
    log_stats(request, data=pdf.filename)
    # Add line here to save file?
    return JSONResponse(content=prediction)


@app.post("/extract")
async def extract(request: Request, pdf: UploadFile = File(...)):
    """Extract standards from PDF."""
    # filepath = save_upload_file_tmp(pdf)
    text = extract_prep.parse_text(pdf.filename)
    refs = find_standard_ref(text)
    json_compatible_item_data = jsonable_encoder(refs)
    log_stats(request, data={"refs": refs, "text": text, "filename": pdf.filename})
    return JSONResponse(content=json_compatible_item_data)


@app.get("/standard_info/{info_key}", response_class=ORJSONResponse)
async def standard_info(request: Request, info_key: str, size: int = 1):
    """GET standard info given a primary key."""
    res = es.search(
        index=idx_main, body={"size": size, "query": {"match": {"num_id": info_key}}}
    )
    # print("Got %d Hits:" % res['hits']['total']['value'])
    results = {}
    for num, hit in enumerate(res["hits"]["hits"]):
        results[str(num + 1)] = hit["_source"]
    jsonResults = json.dumps(results, indent=4)
    json_compatible_item_data = jsonable_encoder(jsonResults)
    log_stats(request, data=info_key)
    return JSONResponse(content=json_compatible_item_data)


@app.get("/search/{searchq}")
async def search(
    request: Request, searchq: str = Field(example="Airplanes"), size: int = 10
):
    """Search elasticsearch."""
    res = es.search(
        index=idx_main,
        body={"size": size, "query": {"match": {"description": searchq}}},
    )
    # print("Got %d Hits:" % res['hits']['total']['value'])
    results = {}
    for num, hit in enumerate(res["hits"]["hits"]):
        results[str(num + 1)] = hit["_source"]  # ["num_id"]
    log_stats(request, data=searchq)
    return JSONResponse(content=results)


@app.put("/add_standards", response_class=HTMLResponse)
async def add_standards(request: Request, doc: dict):
    """Add standards to main ES index."""
    res = es.index(index=idx_main, body=json.dumps(doc))
    print(res)
    json_compatible_item_data = jsonable_encoder(doc)
    log_stats(request, data=doc)
    return JSONResponse(content=json_compatible_item_data)


@app.post("/select_standards")
async def select_standards(request: Request, selected: dict):
    """Capture selected standards."""
    schema = {
        "type": "object",
        "properties": {
            "username": {"type": "string"},
            "standard_key": {"type": "array"},
        },
    }
    # validate(instance={"username" : "user123", "selected" : [1, 2 ,3]}, schema=schema)
    validate(instance=selected, schema=schema)
    json_compatible_item_data = jsonable_encoder(selected)
    res = es.index(index=idx_stats, body=json.dumps(selected))
    print(res)
    log_stats(request, data=selected)
    return JSONResponse(content=json_compatible_item_data)


@app.put("/set_standards")
async def set_standards(request: Request, set_standards: dict):
    """Validate and set preference of standards (done by Admin)."""
    # TODO: Once we are connected to LDAP, add line to verify auth of Admin.
    schema = {
        "type": "object",
        "properties": {
            "username": {"type": "string"},
            "standard_key": {"type": "number"},
            "priority": {"type": "number"},
        },
    }
    validate(instance=set_standards, schema=schema)
    json_compatible_item_data = jsonable_encoder(set_standards)
    es.index(index=idx_stats, body=json.dumps(set_standards))
    # TODO: Update the priority of the selected standards, ES code to update an item to {"priority": 100}
    # es.index(index=idx_main, body=json.dumps(selected))
    log_stats(request, data=set_standards)
    return JSONResponse(content=json_compatible_item_data)


if __name__ == "__main__":
    formatter = logging.Formatter(
        '{"time": "%(asctime)s.%(msecs)03d", "type": "%(levelname)s", "thread":[%(thread)d], "msc": %(message)s}',
        "%Y-%m-%d %H:%M:%S",
    )
    handler = RotatingFileHandler("log/app.log", backupCount=0)
    logging.getLogger().setLevel(logging.DEBUG)
    fastapi_logger.addHandler(handler)
    handler.setFormatter(formatter)
    startMsg = {}
    startMsg["message"] = "*** Starting Server ***"
    print(json.dumps(startMsg))
    fastapi_logger.info(json.dumps(startMsg))
    # read_logs()
    uvicorn.run(app, host="0.0.0.0", port=8080)
