from jsonschema import validate
import json
import os.path
from tqdm import tqdm
import traceback
import fnmatch

# todo: maintain this a one central place!
ES_data_schema = {
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

data_dir='/Users/asitangm/PycharmProjects/techstreet/src/data'

for file_name in fnmatch.filter(os.listdir(data_dir), 'standards_metadata_*.json'):

    sdo_suffix = file_name.replace('standards_metadata_','').replace('.json','')
    print('Converting SDO:', sdo_suffix)

    date_fetched={line.split(" ", 1)[0].strip(): line.split(" ", 1)[1].strip() for line in open(os.path.join(data_dir, 'date_fetched.txt'), 'r').readlines()}

    # 1. ==== load the hierarchy in a lookup dictionary <child_category>-><parent_category>
    hierarchy=json.loads(open(os.path.join(data_dir, 'hierarchy_'+sdo_suffix+'.json'), 'r').read())
    categorical_hierarchy=hierarchy['categorical_hierarchy']
    subcat_to_cat={}
    for category, info in categorical_hierarchy.items():
        for subcat in info['subcats']:
            subcat_to_cat[subcat] = category
    sdo_name=hierarchy['SDO_name']
    sdo_url=hierarchy['SDO_url']
    """
    The hierarchy_<sdo_suffix/abbrev>.json contains the hierarchy in the following format:
    
        hierarchy={
      "SDO_name": "<SDO_name>",
      "SDO_url": "<SDO_url>",
      "categorical_hierarchy": {
        "Category_A": {
          "name": "Category_A",
          "is_leaf": "False",
          "url": "",
          "subcats": [
            "category_1",
            "category_2"
          ]
        },
        "Category_B": {
          "name": "Category_B",
          "is_leaf": "False",
          "url": "",
          "subcats": [
            "category_3"
          ]
        },
        "category_1": {
          "name": "category_1",
          "is_leaf": "True",
          "url": "",
          "subcats": [],
          "standards": [
            "standard_i",
            "standard_ii"
          ]
        },
        "category_2": {
          "name": "category_2",
          "is_leaf": "False",
          "url": "",
          "subcats": [
            "category_aa",
            "category_bb"
          ]
        },
        "category_3": {
          "name": "category_3",
          "is_leaf": "True",
          "url": "",
          "subcats": [],
          "standards": [
            "standard_i"
          ]
        },
        "category_aa": {
          "name": "category_aa",
          "is_leaf": "True",
          "url": "",
          "standards": [
            "standard_iii"
          ]
        },
        "category_bb": {
          "name": "category_bb",
          "is_leaf": "True",
          "url": "",
          "standards": [
            "standard_iv"
          ]
        }
      }
    }

    The lookup is of the following format:
    subcat_to_cat= {
    "category_1":"Category_A",
    "category_2":"Category_A",
    "category_aa":"category_2",
    "category_bb":"category_2",
    "category_3":"Category_B"
    }
    
    """
    # 2. ==== find the category lineages for standards using the lookup
    standard_to_lineages={}
    for category, info in categorical_hierarchy.items():
        if 'standards' in info.keys():
            for standard in info['standards']:
                lineage=[category]
                while True:
                    if lineage[-1] not in subcat_to_cat.keys():
                        break
                    lineage.append(subcat_to_cat[lineage[-1]])
                if standard not in standard_to_lineages.keys():
                    standard_to_lineages[standard]=[]
                standard_to_lineages[standard].append(list(reversed(lineage)))
    print('Lineages:', standard_to_lineages)

    """
    standard_to_lineages={
    "standard_i":[["Category_A", "category_1"], ["Category_B", "category_3"]], # notice this one has two lineages!
    "standard_ii":[["Category_A", "category_1"]],
    "standard_iii":[["Category_A", "category_2", "category_aa"]],
    "standard_iv":[["Category_A", "category_2", "category_bb"]],
    }
    """

    # 3. ==== load the standards metadata file
    standards_metadata=json.loads(open(os.path.join(data_dir, 'standards_metadata_'+sdo_suffix+'.json'), 'r').read())

    # 4. ==== convert the data in ES format
    all_sdo_ES_data=open(os.path.join(data_dir, 'ES_data_'+sdo_suffix+'.json'), 'w')
    for standard, info in tqdm(standards_metadata.items()):
        try:
            ES_data={}
            info['sdo_name']=sdo_name
            info['sdo_url']=sdo_url
            info['techstreet_url']=standard
            category={}
            for lineage in standard_to_lineages[standard]:
                if lineage[0] not in category.keys():
                    category[lineage[0]]=[]
                category[lineage[0]].append(lineage[1:])
            """
            let us see what this variable will be for the standard: standard_i in the above dummy example
            category={
            "Category_A": [["category_1"], ["category_3"]] # the first level of categories becomes the key here as a Top Level Category!
            }
            """
            ES_data['title']=info['Title']
            ES_data['category'] = category
            ES_data['sdo']={"abbreviation": sdo_suffix, "data": info}
            ES_data['description']=info.get('full_description', None)
            ES_data['text']=['title', 'description']
            ES_data['raw_id']=info['Id']
            ES_data['ingestion_date']=date_fetched[standard.strip()]
            # 5. ==== validate the ES json
            validate(instance=ES_data, schema=ES_data_schema)
            # 6. ==== write to file (one standard json in each line)
            all_sdo_ES_data.write(json.dumps(ES_data)+'\n')
            # print('ES_data', json.dumps(ES_data, indent=2))
        except:
            print('ERROR:, info:', info)
            traceback.print_exc()

    all_sdo_ES_data.close()