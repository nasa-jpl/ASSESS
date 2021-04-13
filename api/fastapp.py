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
from typing import Optional
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
import shutil

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


@app.post("/recommend_text")
async def recommend_text(request: Request, sow: Sow):
    """Given an input of Statement of Work as text,
    return a JSON of recommended standards."""
    in_text = sow.text_field
    predictions = extract_prep.predict(in_text=in_text)
    output = {}
    results = {}
    i = 0
    for prediction in predictions["recommendations"]:
        i += 1
        raw_id = prediction["raw_id"]
        code = prediction["code"]
        res = es.search(
            index=idx_main, body={"size": 1, "query": {"match": {"raw_id": raw_id}}}
        )
        for hit in res["hits"]["hits"]:
            results = hit["_source"]
        output[i] = results
        output[i]["similarity"] = prediction["sim"]
    output["embedded_references"] = predictions["embedded_references"]
    json_compatible_item_data = jsonable_encoder(output)
    log_stats(request, data=in_text)
    return JSONResponse(content=json_compatible_item_data)


@app.post("/recommend_file")
async def recommend_file(request: Request, pdf: UploadFile = File(...)):
    """Given an input of a Statement of Work as a PDF,
    return a JSON of recommended standards."""
    print("File received")
    predictions = extract_prep.predict(file=pdf)
    output = {}
    results = {}
    i = 0
    for prediction in predictions["recommendations"]:
        i += 1
        raw_id = prediction["raw_id"]
        res = es.search(
            index=idx_main, body={"size": 1, "query": {"match": {"raw_id": raw_id}}}
        )
        for hit in res["hits"]["hits"]:
            results = hit["_source"]
        output[i] = results
        output[i]["similarity"] = prediction["sim"]
    output["embedded_references"] = predictions["embedded_references"]
    json_compatible_item_data = jsonable_encoder(output)
    log_stats(request, data=pdf.filename)
    # Add line here to save file?
    return JSONResponse(content=json_compatible_item_data)


@app.post("/extract")
async def extract(request: Request, pdf: UploadFile = File(...)):
    """Given an input of a Statement of Work (SoW) as a PDF,
    return a JSON of extracted standards that are embedded within the SoW."""
    # filepath = save_upload_file_tmp(pdf)
    text = extract_prep.parse_text(pdf.filename)
    print("test pdf@@@@@@@@@")
    print(pdf)
    print("test text")
    print(text)
    print("file test")
    file_location = f"{pdf.filename}"
    with open(file_location, "wb+") as file_object:
        shutil.copyfileobj(pdf.file, file_object)
    print({"info": f"file '{pdf.filename}' saved at '{file_location}'"})
    refs = find_standard_ref(text)
    out = {}
    out["embedded_references"] = refs
    out["filename"] = pdf.filename
    out["text"] = text
    json_compatible_item_data = jsonable_encoder(out)
    log_stats(request, data={"refs": refs, "text": text, "filename": pdf.filename})
    return JSONResponse(content=json_compatible_item_data)


@app.get("/standard_info/", response_class=ORJSONResponse)
async def standard_info(
    request: Request,
    id: Optional[str] = None,
    raw_id: Optional[str] = None,
    isbn: Optional[str] = None,
    doc_number: Optional[int] = None,
    status: Optional[str] = None,
    technical_committee: Optional[str] = None,
    published_date: Optional[str] = None,
    ingestion_date: Optional[str] = None,
    title: Optional[str] = None,
    sdo: Optional[str] = None,
    hash: Optional[str] = None,
    size: int = 1,
):
    """Given a standard ID, get standard information from Elasticsearch."""
    if id:
        res = es.search(
            index=idx_main, body={"size": size, "query": {"match": {"id": id}}}
        )
    elif raw_id:
        res = es.search(
            index=idx_main, body={"size": size, "query": {"match": {"raw_id": raw_id}}}
        )
    elif isbn:
        res = es.search(
            index=idx_main, body={"size": size, "query": {"match": {"isbn": isbn}}}
        )
    elif doc_number:
        res = es.search(
            index=idx_main,
            body={"size": size, "query": {"match": {"doc_number": doc_number}}},
        )
    elif status:
        res = es.search(
            index=idx_main,
            body={"size": size, "query": {"match": {"status": status}}},
        )
    elif technical_committee:
        res = es.search(
            index=idx_main,
            body={
                "size": size,
                "query": {"match": {"technical_committee": technical_committee}},
            },
        )
    elif published_date:
        res = es.search(
            index=idx_main,
            body={"size": size, "query": {"match": {"published_date": published_date}}},
        )
    elif ingestion_date:
        res = es.search(
            index=idx_main,
            body={"size": size, "query": {"match": {"ingestion_date": ingestion_date}}},
        )
    elif title:
        res = es.search(
            index=idx_main,
            body={"size": size, "query": {"match": {"title": title}}},
        )
    elif sdo:
        res = es.search(
            index=idx_main,
            body={"size": size, "query": {"exists": {"field": sdo}}},
        )
    elif hash:
        res = es.search(
            index=idx_main,
            body={"size": size, "query": {"match": {"hash": hash}}},
        )
    # print("Got %d Hits:" % res['hits']['total']['value'])
    results = {}
    for num, hit in enumerate(res["hits"]["hits"]):
        results[str(num + 1)] = hit["_source"]
    # jsonResults = json.dumps(results)
    json_compatible_item_data = jsonable_encoder(results)
    log_stats(request, data=id)
    return JSONResponse(content=json_compatible_item_data)


@app.get("/search/{searchq}")
async def search(
    request: Request, searchq: str = Field(example="Airplanes"), size: int = 10
):
    """Search elasticsearch using text."""
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
    """Add standards to the main Elasticsearch index by PUTTING a JSON request here."""
    # TODO: Check Standard body.
    res = es.index(index=idx_main, body=json.dumps(doc))
    print(res)
    json_compatible_item_data = jsonable_encoder(doc)
    log_stats(request, data=doc)
    return JSONResponse(content=json_compatible_item_data)


@app.post("/select_standards")
async def select_standards(request: Request, selected: dict):
    """After a use likes a standard, this endpoint captures the selected standards into the database"""
    schema = {
        "type": "object",
        "properties": {
            "username": {"type": "string"},
            "standard_id": {"type": "array"},
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
            "standard_id": {"type": "string"},
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
