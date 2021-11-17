import json
import logging
import os
import os.path
import shutil
import subprocess
import time
from logging.handlers import RotatingFileHandler
from typing import Optional
import yaml
import dill
import pandas as pd
import requests
import uvicorn
from elasticsearch import Elasticsearch
from fastapi import (
    Body,
    Depends,
    FastAPI,
    File,
    Form,
    HTTPException,
    Request,
    UploadFile,
)
from fastapi.encoders import jsonable_encoder
from fastapi.logger import logger as fastapi_logger
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse, ORJSONResponse
from fastapi.staticfiles import StaticFiles
import aioredis
from fastapi_limiter import FastAPILimiter
from fastapi_limiter.depends import RateLimiter
from jsonschema import validate
from pydantic import BaseModel, Field
from starlette.requests import Request
from starlette.responses import Response

from standard_extractor import find_standard_ref
from text_analysis import extract_prep
import extraction
from web_utils import connect_to_es, read_logs

# Define api settings.
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

# Define rate limiter.
rate_times = 50
rate_seconds = 1
# Connect to Elasticsearch.
es, idx_main, idx_log, idx_stats = connect_to_es()

# Make a log directory.
if not os.path.exists("log"):
    os.makedirs("log")

# Create logs.
formatter = logging.Formatter(
    '{"time": "%(asctime)s.%(msecs)03d", "type": "%(levelname)s", "thread":[%(thread)d], "msc": %(message)s}',
    "%Y-%m-%d %H:%M:%S",
)
# handler = RotatingFileHandler("log/app.log", backupCount=0)
logging.getLogger().setLevel(logging.DEBUG)
# fastapi_logger.addHandler(handler)
# handler.setFormatter(formatter)
startMsg = {}
startMsg["message"] = "*** Starting Server ***"
fastapi_logger.info(json.dumps(startMsg))


@app.on_event("startup")
async def startup():
    with open("conf.yaml", "r") as stream:
        conf = yaml.safe_load(stream)
    host = os.getenv("REDIS_SERVER", conf["redis"][0])
    redis = await aioredis.create_redis_pool(f"redis://{host}")
    await FastAPILimiter.init(redis)


class Sow(BaseModel):
    text_field: str = Field(example="Airplanes are complex.")


def log_stats(request, data=None, user=None):
    """Log detailed data in JSON for incoming/outgoing API request."""
    client_host = request.client.host
    msg = {}
    # TODO: Log user once authentication is connected. msg["user"] = str(user)
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


# @app.post(
#     "/recommend_text",
#     dependencies=[Depends(RateLimiter(times=rate_times, seconds=rate_seconds))],
# )
# async def recommend_text(request: Request, sow: Sow, size: int = 10):
#     """Given an input of Statement of Work as text,
#     return a JSON of recommended standards.
#     """
#     start = time.time()
#     in_text = sow.text_field
#     predictions = old_extract_prep.predict(in_text=in_text, size=size)
#     output = {}
#     results = {}
#     i = 0
#     for prediction in predictions["recommendations"]:
#         i += 1
#         raw_id = prediction["raw_id"]
#         res = es.search(
#             index=idx_main, body={"size": 1, "query": {"match": {"raw_id": raw_id}}}
#         )
#         for hit in res["hits"]["hits"]:
#             results = hit["_source"]
#         output[i] = results
#         output[i]["similarity"] = prediction["sim"]
#     # output["embedded_references"] = predictions["embedded_references"]
#     json_compatible_item_data = jsonable_encoder(output)
#     log_stats(request, data=in_text)
#     print(f"{time.time() - start}")
#     return JSONResponse(content=json_compatible_item_data)


@app.post(
    "/train",
    dependencies=[Depends(RateLimiter(times=rate_times, seconds=rate_seconds))],
)
async def train(index_types=["flat", "flat_sklearn"], vectorizer_types=["tf_idf"]):
    print("Starting training...")
    extraction.train(index_types, vectorizer_types)
    return True


@app.post(
    "/recommend_text",
    dependencies=[Depends(RateLimiter(times=rate_times, seconds=rate_seconds))],
)
async def recommend_text(request: Request, sow: Sow, size: int = 10):
    """Given an input of Statement of Work as text,
    return a JSON of recommended standards.
    """
    start = time.time()
    in_text = sow.text_field
    predictions = extract_prep.predict(in_text=in_text, size=size)
    output = {}
    results = {}
    i = 0
    for prediction in predictions["recommendations"]:
        i += 1
        st_id = prediction["id"]
        res = es.search(
            index=idx_main, body={"size": 1, "query": {"match": {"id": st_id}}}
        )
        for hit in res["hits"]["hits"]:
            results = hit["_source"]
        output[i] = results
        output[i]["similarity"] = prediction["sim"]
    # output["embedded_references"] = predictions["embedded_references"]
    json_compatible_item_data = jsonable_encoder(output)
    log_stats(request, data=in_text)
    print(f"{time.time() - start}")
    return JSONResponse(content=json_compatible_item_data)


@app.post(
    "/recommend_file",
    dependencies=[Depends(RateLimiter(times=rate_times, seconds=rate_seconds))],
)
async def recommend_file(request: Request, pdf: UploadFile = File(...), size: int = 10):
    """Given an input of a Statement of Work as a PDF,
    return a JSON of recommended standards.
    """
    print("File received")
    predictions = extract_prep.predict(file=pdf, size=size)
    output = {}
    results = {}
    i = 0
    for prediction in predictions["recommendations"]:
        i += 1
        st_id = prediction["id"]
        res = es.search(
            index=idx_main, body={"size": 1, "query": {"match": {"id": st_id}}}
        )
        for hit in res["hits"]["hits"]:
            results = hit["_source"]
        output[i] = results
        output[i]["similarity"] = prediction["sim"]
    # output["embedded_references"] = predictions["embedded_references"]
    json_compatible_item_data = jsonable_encoder(output)
    log_stats(request, data=pdf.filename)
    # Add line here to save file?
    return JSONResponse(content=json_compatible_item_data)


@app.post(
    "/recommend_text2",
    dependencies=[Depends(RateLimiter(times=rate_times, seconds=rate_seconds))],
)
async def recommend_text2(
    request: Request,
    sow: Sow,
    size: int = 10,
    index_types=["flat", "flat_sklearn"],
    vectorizer_types=["tf_idf"],
):
    """Given an input of Statement of Work as text,
    return a JSON of recommended standards.
    """
    start = time.time()
    in_text = sow.text_field
    # TODO Elasticsearch
    df_file = "data/feather_text"
    list_of_texts = get_list_of_text(df_file)
    vectorizers, vector_storage, vector_indexes = extraction.load_into_memory(
        index_types, vectorizer_types
    )
    list_of_predictions, scores = extraction.predict(
        in_text,
        size,
        vectorizers,
        vector_storage,
        vector_indexes,
        list_of_texts,
    )
    output = {}
    results = {}
    for i, prediction_id in enumerate(list_of_predictions):
        res = es.search(
            index=idx_main,
            body={"size": 1, "query": {"match": {"id": prediction_id}}},
        )
        print(res)
        for hit in res["hits"]["hits"]:
            results = hit["_source"]
        output[i] = results
        output[i]["similarity"] = scores[i]
    json_compatible_item_data = jsonable_encoder(output)
    log_stats(request, data=in_text)
    print(f"{time.time() - start}")
    return JSONResponse(content=json_compatible_item_data)


@app.post(
    "/recommend_file2",
    dependencies=[Depends(RateLimiter(times=rate_times, seconds=rate_seconds))],
)
async def recommend_file2(
    request: Request,
    pdf: UploadFile = File(...),
    size: int = 10,
    index_types=["flat", "flat_sklearn"],
    vectorizer_types=["tf_idf"],
):
    """Given an input of a Statement of Work as a PDF,
    return a JSON of recommended standards.
    """
    print("File received")
    in_text = extract_prep.parse_text(pdf)
    # TODO Elasticsearch
    df_file = "data/feather_text"
    list_of_texts = get_list_of_text(df_file)
    vectorizers, vector_storage, vector_indexes = extraction.load_into_memory(
        index_types, vectorizer_types
    )
    extraction.predict(
        in_text,
        size,
        vectorizers,
        vector_storage,
        vector_indexes,
        list_of_texts,
    )

    predictions = extract_prep.predict(file=pdf, size=size)
    output = {}
    results = {}
    for i, prediction_id in enumerate(list_of_predictions):
        res = es.search(
            index=idx_main,
            body={"size": 1, "query": {"match": {"id": prediction_id}}},
        )
        for hit in res["hits"]["hits"]:
            results = hit["_source"]
        output[i] = results
        output[i]["similarity"] = scores[i]
    json_compatible_item_data = jsonable_encoder(output)
    log_stats(request, data=in_text)
    print(f"{time.time() - start}")
    return JSONResponse(content=json_compatible_item_data)


@app.post(
    "/extract",
    dependencies=[Depends(RateLimiter(times=rate_times, seconds=rate_seconds))],
)
async def extract(request: Request, pdf: UploadFile = File(...)):
    """Given an input of a Statement of Work (SoW) as a PDF,
    return a JSON of extracted standards that are embedded within the SoW."""
    # filepath = save_upload_file_tmp(pdf)
    file_location = f"{pdf.filename}"
    # with open(file_location, "wb+") as file_object:
    #    shutil.copyfileobj(pdf.file, file_object)
    print({"info": f"file '{pdf.filename}' saved at '{file_location}'"})
    text = extract_prep.parse_text(file_location)
    refs = find_standard_ref(text)
    out = {}
    out["embedded_references"] = refs
    out["filename"] = pdf.filename
    json_compatible_item_data = jsonable_encoder(out)
    log_stats(request, data={"refs": refs, "filename": pdf.filename})
    return JSONResponse(content=json_compatible_item_data)


@app.get(
    "/standard_info/",
    response_class=ORJSONResponse,
    dependencies=[Depends(RateLimiter(times=rate_times, seconds=rate_seconds))],
)
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
    category: Optional[str] = None,
    text: Optional[str] = None,
    url: Optional[str] = None,
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
        # res = es.search(index=idx_main, body={"query": {"exists": {"field": sdo_key}}})
        res = es.search(
            index=idx_main,
            body={"size": size, "query": {"match": {"sdo.abbreviation": sdo}}},
        )
    elif category:
        res = es.search(
            index=idx_main,
            body={"size": size, "query": {"match": {"category": category}}},
        )
    elif text:
        res = es.search(
            index=idx_main,
            body={"size": size, "query": {"match": {"text": text}}},
        )
    elif url:
        res = es.search(
            index=idx_main,
            body={"size": size, "query": {"match": {"url": url}}},
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


@app.get(
    "/search/{searchq}",
    dependencies=[Depends(RateLimiter(times=rate_times, seconds=rate_seconds))],
)
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


@app.put(
    "/add_standards",
    response_class=HTMLResponse,
    dependencies=[Depends(RateLimiter(times=rate_times, seconds=rate_seconds))],
)
async def add_standards(request: Request, doc: dict):
    """Add standards to the main Elasticsearch index by PUTTING a JSON request here."""
    # TODO: Check Standard body.
    res = es.index(index=idx_main, body=json.dumps(doc))
    print(res)
    json_compatible_item_data = jsonable_encoder(doc)
    log_stats(request, data=doc)
    return JSONResponse(content=json_compatible_item_data)


@app.put(
    "/edit_standards",
    response_class=HTMLResponse,
    dependencies=[Depends(RateLimiter(times=rate_times, seconds=rate_seconds))],
)
async def edit_standards(request: Request, doc: dict):
    """Add standards to the main Elasticsearch index by PUTTING a JSON request here."""
    # TODO: Check Standard body. Test update.
    res = es.update(index=idx_main, body=json.dumps(doc))
    print(res)
    json_compatible_item_data = jsonable_encoder(doc)
    log_stats(request, data=doc)
    return JSONResponse(content=json_compatible_item_data)


@app.put(
    "/delete_standards",
    response_class=HTMLResponse,
    dependencies=[Depends(RateLimiter(times=rate_times, seconds=rate_seconds))],
)
async def delete_standards(request: Request, doc: dict):
    """Add standards to the main Elasticsearch index by PUTTING a JSON request here."""
    # TODO: Check Standard body. Test deletion.
    res = es.delete(index=idx_main, body=json.dumps(doc))
    print(res)
    json_compatible_item_data = jsonable_encoder(doc)
    log_stats(request, data=doc)
    return JSONResponse(content=json_compatible_item_data)


@app.post(
    "/select_standards",
    dependencies=[Depends(RateLimiter(times=rate_times, seconds=rate_seconds))],
)
async def select_standards(request: Request, selected: dict):
    """After a use likes a standard, this endpoint captures the selected standards into the database."""
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


@app.put(
    "/set_standards",
    dependencies=[Depends(RateLimiter(times=rate_times, seconds=rate_seconds))],
)
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
    log_stats(request, data=set_standards)
    return JSONResponse(content=json_compatible_item_data)


if __name__ == "__main__":
    # read_logs()
    uvicorn.run(app, host="0.0.0.0", port=8080)
