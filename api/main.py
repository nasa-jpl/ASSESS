import json
import logging
import os
import os.path
import shutil
import time
from logging.handlers import RotatingFileHandler
from typing import Optional
import yaml
import uvicorn
from fastapi import (
    BackgroundTasks,
    Depends,
    FastAPI,
    File,
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

from standards_extraction import parse
import ml_core
from utils import connect_to_es
import ast

# Define api settings.
app = FastAPI()
origins = [
    "http://localhost",
]
app.type = "00"
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
data_schema = {
    "type": "object",
    "properties": {
            "doc_number": {"type": ["string", "null"]},
            "id": {"type": ["string", "null"]},
            "raw_id": {"type": ["string", "null"]},
            "description": {"type": ["string", "null"]},
            "ingestion_date": {"type": ["string", "null"]},
            "hash": {"type": ["string", "null"]},
            "published_date": {"type": ["string", "null"]},
            "isbn": {"type": ["string", "null"]},
            "text": {"type": ["array", "null"]},
            "status": {"type": ["string", "null"]},
            "technical_committee": {"type": ["string", "null"]},
            "title": {"type": ["string", "null"]},
            "url": {"type": ["string", "null"]},
            "category": {"type": ["object", "null"]},
            "sdo": {"type": ["object", "null"]},
    },
}
vectorizers, vector_storage, vector_indexes = ml_core.load_into_memory(
    index_types=["flat"], vectorizer_types=["tf_idf"]
)


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


def str_to_ls(s):
    if type(s) is str:
        s = ast.literal_eval(s)
    return s


def run_predict(request, start, in_text, size, start_from, vectorizer_types, index_types):
    list_of_predictions, scores = ml_core.predict(
        in_text,
        size,
        start_from,
        vectorizers,
        vector_storage,
        vector_indexes,
        vectorizer_types,
        index_types,
    )
    output = {}
    # Add mget request here
    """
    res = es.mget(index = idx_main, body = {'ids': list_of_predictions})
    results = [hit["_source"] for hit in res["hits"]["hits"]]
    """
    # TODO: Refactor
    for i, prediction_id in enumerate(list_of_predictions):
        res = es.search(
            index=idx_main,
            body={"size": 1, "query": {"match": {"_id": prediction_id}}},
        )
        for hit in res["hits"]["hits"]:
            results = hit["_source"]
        j = start_from + i
        output[j] = results
        output[j]["similarity"] = scores[j]
    # End Refactor
    json_compatible_item_data = jsonable_encoder(output)
    log_stats(request, data=in_text)
    print(f"{time.time() - start}")
    return JSONResponse(content=json_compatible_item_data)


# def background_train(es, index_types, vectorizer_types):
#     ml_core.train(es, index_types, vectorizer_types)

@app.post(
    "/train",
    dependencies=[
        Depends(RateLimiter(times=rate_times, seconds=rate_seconds))],
)
async def train(request: Request, background_tasks: BackgroundTasks, index_types=["flat", "flat_sklearn"], vectorizer_types=["tf_idf"]):
    vectorizer_types = str_to_ls(vectorizer_types)
    index_types = str_to_ls(index_types)
    background_tasks.add_task(ml_core.train, es,
                              index_types, vectorizer_types)
    log_stats(request, data=None)
    #message = {}
    # if in_progress:
    print("Training task created and sent to the background...")
    # message = {'status': 'training'}
    # else:
    message = {'status': 'in_progress'}
    return JSONResponse(message)


@app.post(
    "/recommend_text",
    dependencies=[
        Depends(RateLimiter(times=rate_times, seconds=rate_seconds))],
)
async def recommend_text(
    request: Request,
    sow: Sow,
    size: int = 10,
    start_from: int = 0,
    vectorizer_types=["tf_idf"],
    index_types=["flat"],
):
    vectorizer_types = str_to_ls(vectorizer_types)
    index_types = str_to_ls(index_types)
    """Given an input of Statement of Work as text,
    return a JSON of recommended standards.
    """
    in_text = sow.text_field
    # df_file = "data/feather_text"
    return run_predict(
        request, time.time(), in_text, size, start_from, vectorizer_types, index_types,
    )


@app.post(
    "/recommend_file",
    dependencies=[
        Depends(RateLimiter(times=rate_times, seconds=rate_seconds))],
)
async def recommend_file(
    request: Request,
    pdf: UploadFile = File(...),
    size: int = 10,
    start_from: int = 0,
    vectorizer_types=["tf_idf"],
    index_types=["flat"],
):
    vectorizer_types = str_to_ls(vectorizer_types)
    index_types = str_to_ls(index_types)
    """Given an input of a Statement of Work as a PDF,
    return a JSON of recommended standards.
    """
    print("File received.")
    print(pdf.content_type)
    print(pdf.filename)
    in_text = parse.parse_pdf(pdf)
    print(in_text)
    return run_predict(
        request, time.time(), in_text, size, start_from, vectorizer_types, index_types
    )


@app.post(
    "/extract",
    dependencies=[
        Depends(RateLimiter(times=rate_times, seconds=rate_seconds))],
)
async def extract(request: Request, pdf: UploadFile = File(...)):
    """Given an input of a Statement of Work (SoW) as a PDF,
    return a JSON of extracted standards that are embedded within the SoW."""
    # filepath = save_upload_file_tmp(pdf)
    file_location = f"{pdf.filename}"
    # with open(file_location, "wb+") as file_object:
    #    shutil.copyfileobj(pdf.file, file_object)
    print({"info": f"file '{pdf.filename}' saved at '{file_location}'"})
    text = parse.tika_parse(file_location)
    refs = parse.find_standard_ref(text)
    out = {}
    out["embedded_references"] = refs
    out["filename"] = pdf.filename
    json_compatible_item_data = jsonable_encoder(out)
    log_stats(request, data={"refs": refs, "filename": pdf.filename})
    return JSONResponse(content=json_compatible_item_data)


@app.get(
    "/standard_info/",
    response_class=ORJSONResponse,
    dependencies=[
        Depends(RateLimiter(times=rate_times, seconds=rate_seconds))],
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
    start_from: int = 0,
):
    """Given a standard ID, get standard information from Elasticsearch."""
    if id:
        res = es.search(
            index=idx_main, body={"from": start_from,
                                  "size": size, "query": {"match": {"id": id}}}
        )
    elif raw_id:
        res = es.search(
            index=idx_main, body={"from": start_from, "size": size, "query": {
                "match": {"raw_id": raw_id}}}
        )
    elif isbn:
        res = es.search(
            index=idx_main, body={"from": start_from,
                                  "size": size, "query": {"match": {"isbn": isbn}}}
        )
    elif doc_number:
        res = es.search(
            index=idx_main,
            body={"from": start_from, "size": size, "query": {
                "match": {"doc_number": doc_number}}},
        )
    elif status:
        res = es.search(
            index=idx_main,
            body={"from": start_from, "size": size,
                  "query": {"match": {"status": status}}},
        )
    elif technical_committee:
        res = es.search(
            index=idx_main,
            body={
                "from": start_from,
                "size": size,
                "query": {"match": {"technical_committee": technical_committee}},
            },
        )
    elif published_date:
        res = es.search(
            index=idx_main,
            body={"from": start_from, "size": size, "query": {
                "match": {"published_date": published_date}}},
        )
    elif ingestion_date:
        res = es.search(
            index=idx_main,
            body={"from": start_from, "size": size, "query": {
                "match": {"ingestion_date": ingestion_date}}},
        )
    elif title:
        res = es.search(
            index=idx_main,
            body={"from": start_from, "size": size,
                  "query": {"match": {"title": title}}},
        )
    elif sdo:
        # res = es.search(index=idx_main, body={"query": {"exists": {"field": sdo_key}}})
        res = es.search(
            index=idx_main,
            body={"from": start_from, "size": size, "query": {
                "match": {"sdo.abbreviation": sdo}}},
        )
    elif category:
        res = es.search(
            index=idx_main,
            body={"from": start_from, "size": size,
                  "query": {"match": {"category": category}}},
        )
    elif text:
        res = es.search(
            index=idx_main,
            body={"from": start_from, "size": size,
                  "query": {"match": {"text": text}}},
        )
    elif url:
        res = es.search(
            index=idx_main,
            body={"from": start_from, "size": size,
                  "query": {"match": {"url": url}}},
        )
    elif hash:
        res = es.search(
            index=idx_main,
            body={"from": start_from, "size": size,
                  "query": {"match": {"hash": hash}}},
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
    dependencies=[
        Depends(RateLimiter(times=rate_times, seconds=rate_seconds))],
)
async def search(
    request: Request, searchq: str = Field(example="Airplanes"), size: int = 10, start_from: int = 0,
):
    """Search elasticsearch using text."""
    res = es.search(
        index=idx_main,
        body={"from": start_from, "size": size, "query": {
            "match": {"description": searchq}}},
    )
    # print("Got %d Hits:" % res['hits']['total']['value'])
    results = {}
    for num, hit in enumerate(res["hits"]["hits"]):
        results[str(num + 1)] = hit["_source"]  # ["num_id"]
    log_stats(request, data=searchq)
    return JSONResponse(content=results)


@app.post(
    "/add_standards",
    response_class=HTMLResponse,
    dependencies=[
        Depends(RateLimiter(times=rate_times, seconds=rate_seconds))],
)
async def add_standards(request: Request, doc: dict):
    """Add standards to the main Elasticsearch index by PUTTING a JSON request here."""
    validate(instance=doc, schema=data_schema)
    res = es.index(index=idx_main, body=json.dumps(doc))
    print(res)
    json_compatible_item_data = jsonable_encoder(doc)
    log_stats(request, data=doc)
    return JSONResponse(content=json_compatible_item_data)


@app.put(
    "/edit_standards",
    response_class=HTMLResponse,
    dependencies=[
        Depends(RateLimiter(times=rate_times, seconds=rate_seconds))],
)
async def edit_standards(request: Request, doc: dict):
    """Add standards to the main Elasticsearch index by PUTTING a JSON request here."""
    validate(instance=doc, schema=data_schema)
    res = es.search(
        index="assess_remap",
        query={"match": {"id": doc["id"]}},
    )
    _id = res["hits"]["hits"][0]["_id"]
    res = es.update(index=idx_main, id=_id, body={"doc": doc})
    print(res)
    json_compatible_item_data = jsonable_encoder(doc)
    log_stats(request, data=doc)
    return JSONResponse(content=json_compatible_item_data)


@app.delete(
    "/delete_standards",
    response_class=HTMLResponse,
    dependencies=[
        Depends(RateLimiter(times=rate_times, seconds=rate_seconds))],
)
async def delete_standards(request: Request, id: str):
    """Delete standards to the main Elasticsearch index by PUTTING a JSON request here."""
    # TODO: Once we are connected to LDAP, add line to verify auth of Admin.
    # res = es.delete(index=idx_main, id=id)
    res = es.delete_by_query(
        index=idx_main, body={"size": 1, "query": {"match": {"id": id}}}
    )
    print(res)
    json_compatible_item_data = jsonable_encoder(res)
    log_stats(request, data=res)
    return JSONResponse(content=json_compatible_item_data)


@app.post(
    "/select_standards",
    dependencies=[
        Depends(RateLimiter(times=rate_times, seconds=rate_seconds))],
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
    dependencies=[
        Depends(RateLimiter(times=rate_times, seconds=rate_seconds))],
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
