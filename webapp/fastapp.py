from flask import Flask, send_from_directory, safe_join
import os
import json
import subprocess
#from flask import request
from flask_cors import CORS, cross_origin
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
from fastapi import FastAPI, File, Form, UploadFile, Request
from fastapi.encoders import jsonable_encoder
import requests
from starlette.requests import Request
from starlette.responses import Response
from pydantic import BaseModel
from elasticsearch import Elasticsearch
from web_utils import connect_to_es, read_logs
from fastapi import FastAPI, HTTPException
from fastapi.logger import logger as fastapi_logger
from logging.handlers import RotatingFileHandler
import logging


app = FastAPI()
origins = [
    "http://localhost",
]

es, es_index = connect_to_es()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class Sow(BaseModel):
    text_field: str


def log_stats(request, data=None):
    client_host = request.client.host
    msg = {}
    msg["method"] = str(request.method)
    msg["url"] = str(request.url)
    msg["host"] = str(client_host)
    msg["query_params"] = str(request.query_params)
    msg["path_params"] = str(request.path_params)
    msg["headers"] = dict(request.headers)
    msg["data"] = str(data)
    fastapi_logger.info(json.dumps(msg))


@app.get('/', response_class=HTMLResponse)
async def index(request: Request):
    log_stats(request)
    host = request.url
    recc_text_url = str(host) +'recommend_text'
    recc_file_url = str(host) +'recommend_file'
    extract_url = str(host) + 'extract'
    st_info_url = str(host) + 'standard_info'
    search_url = str(host) + 'search'
    add_url = str(host) + 'add_standards'
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
        </body>
    </html>""".format(recc_text_url=recc_text_url, recc_file_url=recc_file_url,
     extract_url=extract_url, st_info_url=st_info_url, search_url=search_url, add_url=add_url)
    return HTMLResponse(content=content, status_code=200)


@app.post('/recommend_text')
async def recommend_text(request: Request, sow: Sow):
    """
    POST from input text
    """
    in_text = sow.text_field
    prediction = extract_prep.predict(in_text=in_text)
    json_compatible_item_data = jsonable_encoder(prediction)
    log_stats(request, data=in_text)
    return JSONResponse(content=json_compatible_item_data)


@app.post('/recommend_file')
async def recommend_file(request: Request, pdf: UploadFile = File(...)):
    """
    POST from PDF
    """
    print("File received")
    prediction = extract_prep.predict(file=pdf)
    log_stats(request, data=pdf.filename)
    # Add line here to save file?
    return JSONResponse(content=prediction)


@app.post('/extract')
async def extract(request: Request, pdf: UploadFile = File(...)):
    """
    POST from PDF
    """
    #filepath = save_upload_file_tmp(pdf) 
    text = extract_prep.parse_text(pdf.filename)
    refs = find_standard_ref(text)
    json_compatible_item_data = jsonable_encoder(refs)
    log_stats(request, data={"refs": refs, "text": text, "filename": pdf.filename})
    return JSONResponse(content=json_compatible_item_data)


@app.get('/standard_info/{searchq}', response_class=ORJSONResponse)
async def standard_info(request: Request, searchq: str, size: int = 1):
    """
    GET standard info given a unique standard identifier
    """
    res = es.search(index=es_index, body={"size": size, "query": {"match": {"num_id": searchq}}})
    #print("Got %d Hits:" % res['hits']['total']['value'])
    results = {}
    for num, hit in enumerate(res['hits']['hits']):
        results[num+1] = hit["_source"]
    json_compatible_item_data = jsonable_encoder(results)
    log_stats(request, data=searchq)
    return JSONResponse(content=json_compatible_item_data)    


@app.get('/search/{searchq}', response_class=HTMLResponse)
async def search(request: Request, searchq: str, size: int = 10):
    res = es.search(index=es_index, body={"size": size, "query": {"match": {"description": searchq}}})
    #print("Got %d Hits:" % res['hits']['total']['value'])
    results = {}
    for num, hit in enumerate(res['hits']['hits']):
        results[num+1] = hit["_source"]#["num_id"]
    json_compatible_item_data = jsonable_encoder(results)
    log_stats(request, data=searchq)
    return JSONResponse(content=json_compatible_item_data)    


@app.put('/add_standards', response_class=HTMLResponse)
async def add_standards(request: Request, doc: dict):
    res = es.index(index=es_index, body=json.dumps(doc))
    print(res)
    json_compatible_item_data = jsonable_encoder(doc)
    log_stats(request, data=doc)
    return JSONResponse(content=json_compatible_item_data)


if __name__ == "__main__":
    formatter = logging.Formatter(
    "{\"time\": \"%(asctime)s.%(msecs)03d\", \"type\": \"%(levelname)s\", \"thread\":[%(thread)d], \"msc\": %(message)s}", "%Y-%m-%d %H:%M:%S"
    )
    handler = RotatingFileHandler('log/app.log', backupCount=0)
    logging.getLogger().setLevel(logging.DEBUG)
    fastapi_logger.addHandler(handler)
    handler.setFormatter(formatter)
    startMsg = {}
    startMsg["message"] = "*** Starting Server ***"
    print(json.dumps(startMsg))
    fastapi_logger.info(json.dumps(startMsg))
    #read_logs()
    #log_config = uvicorn.config.LOGGING_CONFIG
    #print(log_config)
    #log_config["formatters"]["access"]["fmt"] = "%(asctime)s - %(levelname)s - %(message)s"
    #log_config["formatters"]["default"]["fmt"] = "%(asctime)s - %(levelname)s - %(message)s"
    #print(log_config["formatters"]["default"]["fmt"])
    uvicorn.run(app, host="0.0.0.0", port=8080)
