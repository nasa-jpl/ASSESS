from elasticsearch import Elasticsearch
from elasticsearch.helpers import scan
import json
import requests
import uuid
import hashlib
import time
from pprint import pprint


def convert_to_hash(url):
    if url and "http" in url:
        r = requests.get(url)
        if r.status_code == 200:
            hash_object = hashlib.sha256(r.content)
            result = hash_object.hexdigest()
            return result
    return None


def strip_number(txt):
    return [int(s) for s in txt.split() if s.isdigit()]


def clean_sections(txt):
    """
    ['Foreword\nISO (the International Organization for Standardization) is a worldwide federation of national standards bodies (ISO member bodies). The work of preparing International Standards is normally carried out through ISO technical committees. Each member body interested in a subject for which a technical committee has been established has the right to be represented on that committee. International organizations, governmental and nongovernmental, in liaison with ISO, also take part in the work. ISO collaborates closely with the International Electrotechnical Commission (IEC) on all matters of electrotechnical standardization.\nDraft International Standards adopted by the technical committees are circulated to the member bodies for voting. Publication as an International Standard requires approval by at least 75 % of the member bodies casting a vote.\nInternational Standard ISO 12103-2 was prepared by Technical Committee ISO/TC 22, Road vehicles, Subcommittee SC 7, Injection equipment and filters for use on road vehicles.\nISO 12103 consists of the following parts, under the general title Road vehicles — Test dust for filter evaluation :\n— Part 1: Arizona test dust\n— Part 2: Aluminium oxide test dust\nAnnexes A to C of this part of ISO 12103 are for information only.', 'Introduction\nThis part of ISO 12103 specifies a range of inorganic test dusts, manufactured from fused aluminium oxide, primarily used for evaluating the performance of both fuel and lubricating oil filters for internal combustion engines, generally by gravimetric methods.\nThis part of ISO 12103 is to be used in conjunction with a number of other International Standards which refer to the use of these test dusts in various filter performance test procedures.', '1   Scope\nThis part of ISO 12103 specifies the particle size distribution of five inorganic test dusts used for the evaluation of filters.\nThese dust are used in conjunction with various test procedures designed to evaluate, in general, fuel and lubricating oil filters for internal combustion engines by gravimetric methods.\nThe dusts may also be used for a number of other applications, such as for abrasion tests, where distinct, known particle size distributions of hard, abrasive material are required.']

    """
    res = {}
    for section in txt:
        try:
            spl = section.split("\n")
            res[spl[0]] = spl[1]
        except Exception:
            return None
    return res


def convert_to_new(doc, client, i, new="assess_remap"):
    if doc["datetime"]:
        timestamp = doc["datetime"]
    else:
        timestamp = time.strftime("%Y/%m/%d %H:%M:%S")  # 2018-03-10 01:23:27

    mappings = {
        "_id": uuid.uuid4().hex,
        "raw_id": doc["id"].strip("~"),
        "doc_number": i,
        "description": doc["description"],
        "status": doc["current_status"],
        "technical_committee": doc["tc"],  # doc["technical_committee"]
        "sdo": {
            "ics": {
                "code": doc["code"].strip("~"),
                "field": doc["field"].strip("~"),
                "group": doc["group"].strip("~"),
                "subgroup": doc["subgroup"].strip("~"),
                "edition": strip_number(doc["edition"]),
                "number_of_pages": strip_number(doc["number_of_pages"]),
                "section_titles": doc["section_titles"],
                "sections": clean_sections(doc["sections"]),
                "new_standard": doc["new_standard"].strip("~"),
                "new_field": doc["new_field"].strip("~"),
                "new_group": doc["new_group"].strip("~"),
                "new_subgroup": doc["new_subgroup"].strip("~"),
                "type": doc["type"],
                "preview_url": doc["preview_url"],
            }
        },
        "title": doc["title"].strip("~"),
        "published_date": doc["publication_date"],
        "isbn": None,
        "url": doc["link"],
        "ingestion_date": timestamp,
        "hash": convert_to_hash(doc["link"]),
    }
    print(doc["sections"])
    return mappings


REMOTE_URL = "https://localhost:9200/"
LOCAL_FILE = "elasticsearch-dump.txt"
INDEX = "iso_final_clean"
client = Elasticsearch()

# fp = open(LOCAL_FILE, "w")
i = 0
for doc in scan(client, query={}, index=INDEX):
    # json.dump(row, fp)
    # fp.write("\n")
    # fp.flush()  # So you can tail -f the file
    i += 1
    print("old")
    pprint(doc["_source"])
    print("new")
    pprint(convert_to_new(doc["_source"], client, i))
    if i == 50:
        exit()

# fp.close()
