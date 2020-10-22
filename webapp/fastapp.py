from flask import Flask, send_from_directory, safe_join
import os
import json
import subprocess
from flask import request
from flask_cors import CORS, cross_origin
from sklearn.neighbors import NearestNeighbors
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import normalize
import dill
import pandas as pd
from sklearn.feature_extraction import text
from standard_extractor import find_standard_ref
#from text_analysis.utils import loadmodel
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
import shutil
from pathlib import Path
from tempfile import NamedTemporaryFile
from typing import Callable


app = FastAPI()
#app.static_folder = "webui"
origins = [
    "http://localhost",
]
es = Elasticsearch(["172.19.0.2"])
es_index = "iso_final_clean"
#es = Elasticsearch()
#es_index = "test-csv"

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Sow(BaseModel):
    text_field: str

"""BEGIN
@app.get('/')
def index():    #return send_from_directory('webui/', 'index.html')
    webapi = FastAPI(openapi_url="index.html")
    webapi.mount("/webui", StaticFiles(directory="webui"))
    app.mount("/static", StaticFiles(directory="webui/"), name="webui")
    #return HTMLResponse(pkg_resources.resource_string(__name__, 'static/index.html'))
    return HTMLResponse(content=html_content, status_code=200)
END"""

@app.get('/', response_class=HTMLResponse)
async def index(request: Request):
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
            <h2>API Endpoints</h2>
            <p>{recc_text_url}</p>
            <p>{recc_file_url}</p>
            <p>{extract_url}</p>
            <p>{st_info_url}</p>
            <p>{search_url}</p>
            <p>{add_url}</p>
        </body>
    </html>""".format(recc_text_url=recc_text_url, recc_file_url=recc_file_url,
     extract_url=extract_url, st_info_url=st_info_url, search_url=search_url, add_url=add_url)
    return HTMLResponse(content=content, status_code=200)


@app.post('/recommend_text')
async def recommend_text(sow: Sow):
    """
    POST from input text
    """
    in_text = sow.text_field
    prediction = extract_prep.predict(in_text=in_text)
    json_compatible_item_data = jsonable_encoder(prediction)
    return JSONResponse(content=json_compatible_item_data)


@app.post('/recommend_file')
async def recommend_file(pdf: UploadFile = File(...)):
    """
    POST from PDF
    """
    print("File received")
    prediction = extract_prep.predict(file=pdf)
    #json_compatible_item_data = jsonable_encoder(prediction)
    return JSONResponse(content=prediction)


@app.post('/extract')
async def extract(pdf: UploadFile = File(...)):
    """
    POST from PDF
    """

    #filepath = save_upload_file_tmp(pdf) 

    text = extract_prep.parse_text(pdf.filename)
    refs = find_standard_ref(text)
    json_compatible_item_data = jsonable_encoder(refs)
    return JSONResponse(content=json_compatible_item_data)


@app.get('/standard_info/{searchq}', response_class=ORJSONResponse)
async def standard_info(searchq: str, size: int = 1):
    """
    GET standard info given a unique standard identifier
    """
    res = es.search(index=es_index, body={"size": size, "query": {"match": {"num_id":searchq}}})
    #print("Got %d Hits:" % res['hits']['total']['value'])
    results = {}
    for num, hit in enumerate(res['hits']['hits']):
        results[num+1] = hit["_source"]
    json_compatible_item_data = jsonable_encoder(results)
    return JSONResponse(content=json_compatible_item_data)    

# incomplete
@app.get('/save_activity', response_class=HTMLResponse)
async def save_activity():
    return


@app.get('/search/{searchq}', response_class=HTMLResponse)
async def search(searchq: str, size: int = 10):
    res = es.search(index=es_index, body={"size": size, "query": {"match": {"description":searchq}}})
    #print("Got %d Hits:" % res['hits']['total']['value'])
    results = {}
    for num, hit in enumerate(res['hits']['hits']):
        results[num+1] = hit["_source"]#["num_id"]
    json_compatible_item_data = jsonable_encoder(results)
    return JSONResponse(content=json_compatible_item_data)    


@app.put('/add_standards', response_class=HTMLResponse)
async def add_standards(doc: dict):
    #print(doc)
    res = es.index(index=es_index, body=json.dumps(doc))
    print(res)
    json_compatible_item_data = jsonable_encoder(doc)
    return JSONResponse(content=json_compatible_item_data)


# def save_upload_file_tmp(upload_file: UploadFile) -> Path:
#     try:
#         suffix = Path(upload_file.filename).suffix
#         with NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
#             shutil.copyfileobj(upload_file.file, tmp)
#             tmp_path = Path(tmp.name)
#     finally:
#         upload_file.file.close()
#     return tmp_path


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
    #prediction = extract_prep.predict(in_text="airplane testing")
    #print(prediction)
