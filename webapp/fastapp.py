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


app = FastAPI()
#app.static_folder = "webui"
origins = [
    "http://localhost",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
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
    print(recc_text_url)
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
        </body>
    </html>""".format(recc_text_url=recc_text_url, recc_file_url=recc_file_url,
     extract_url=extract_url, st_info_url=st_info_url)
    return HTMLResponse(content=content, status_code=200)


@app.post('/recommend_text')
async def recommend_text(sow: Sow):
    """
    POST from input text
    """
    print(sow)
    in_text = sow.text_field
    prediction = extract_prep.predict(in_text=in_text)
    json_compatible_item_data = jsonable_encoder(prediction)
    return JSONResponse(content=json_compatible_item_data)

@app.post('/recommend_file')
async def recommend_file(pdf: bytes = File(...)):
    """
    POST from PDF
    """
    prediction = extract_prep.predict(files=pdf)
    json_compatible_item_data = jsonable_encoder(prediction)
    return JSONResponse(content=json_compatible_item_data)


@app.post('/extract')
async def extract(pdf: bytes = File(...)):
    """
    POST from PDF
    """
    refs = extract_prep.extract_standard_ref(filename=pdf)
    json_compatible_item_data = jsonable_encoder(refs)
    return JSONResponse(content=json_compatible_item_data)


@app.get('/standard_info/{pdf_location}', response_class=ORJSONResponse)
async def standard_info(pdf_location: str):
    """
    GET standard info given a unique standard identifier
    """
    standard_details = [{"id": pdf_location}]
    json_compatible_item_data = jsonable_encoder(standard_details)
    return JSONResponse(content=json_compatible_item_data)


# Incomplete
@app.get('/save_activity', response_class=HTMLResponse)
async def save_activity():
    return


# Incomplete
@app.get('/search', response_class=HTMLResponse)
async def search():
    return


# Incomplete
@app.get('/add_standards', response_class=HTMLResponse)
async def add_standards():
    return


if __name__ == "__main__":
    uvicorn.run(app)
    #prediction = extract_prep.predict(in_text="airplane testing")
    #print(prediction)
