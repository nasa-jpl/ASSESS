import shutil
from pathlib import Path
from tempfile import NamedTemporaryFile
from typing import Callable
import yaml
from elasticsearch import Elasticsearch
from fastapi import FastAPI, File, Form, UploadFile


def connect_to_es():
    with open("conf.yaml", 'r') as stream:
        conf = yaml.safe_load(stream)
    print(conf['es_index'][0])
    es = Elasticsearch([conf['es_server'][0]])
    es_index = conf["es_index"][0]
    return es, es_index


def save_upload_file_tmp(upload_file: UploadFile) -> Path:
    try:
        suffix = Path(upload_file.filename).suffix
        with NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            shutil.copyfileobj(upload_file.file, tmp)
            tmp_path = Path(tmp.name)
    finally:
        upload_file.file.close()
    return tmp_path