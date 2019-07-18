from selenium import webdriver
from selenium.common import exceptions

from selenium.webdriver import DesiredCapabilities

import csv
import json
import argparse
import logging
import re


class Node(object):
    def __init__(self, code, field, url):
        self.code = code
        self.field = field
        self.url = url
        self.children = []

    def add_child(self, obj):
        self.children.append(obj)


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-f", "--fields", required=False, help="comma-separated list of ISO fields to be collected")
ap.add_argument("-o", "--output", required=False, help="path to the output CSV file")
ap.add_argument("-j", "--json", required=False, help="path to the output JSON file")
args = vars(ap.parse_args())

fields = args["fields"].split(",") if args["fields"] else []
csv_output = args["output"] if args["output"] else "standards.csv"
json_output = args["json"] if args["json"] else "standards.json"

driver = webdriver.Remote(command_executor='http://localhost:4444/wd/hub', desired_capabilities=DesiredCapabilities.CHROME)

# Standards catalogue
iso_url = "https://www.iso.org/standards-catalogue/browse-by-ics.html"

css_selectors = ["datatable-ics", "datatable-ics-children", "datatable-ics-projects"]

root_ics = Node("0", "ICS", iso_url)

tree_ics = {"code": 0, "field": "ICS", "url": iso_url, "children": []}

def preorder_visit(node, prefix, filewriter):
    code = node.code if node.code == "0" else "0." + str(node.code)
    if str(node.code).startswith("ISO"):
        code = "0." + str(prefix) + "." + str(node.code)

    filewriter.writerow([code.encode('ascii', errors='replace'), node.url, node.field.encode('ascii', errors='replace')])

    prefix = str(node.code)

    for child in node.children:
        preorder_visit(child, prefix, filewriter)


def get_link_text(link):
    text = ""
    try:
        text = link.find_element_by_css_selector("td.sorting_1 a").text
    except:
        text = link.find_element_by_css_selector("td.sorting_1").text
        pass

    return text


def get_link_href(link):
    text = ""
    try:
        text = link.find_element_by_css_selector("td.sorting_1 a").get_attribute("href")
    except:
        pass

    return text


def get_ics(url, node_ics, node_ics_json):
    driver.get(url)

    parent_ics = node_ics

    parent_ics_json = node_ics_json

    for selector in css_selectors:
        try:
            ics_table = driver.find_element_by_id(selector)
            break
        except exceptions.NoSuchElementException as ex:
           print(ex.message)

    ics_table_id = ics_table.get_attribute("id")

    if ics_table_id != "datatable-ics-projects":
        links = ics_table.find_elements_by_css_selector("tbody tr")

        urls = {get_link_text(link): [link.find_element_by_css_selector("td[data-title='Field']").text.replace('\n', ' '), get_link_href(link)] for link in links}
        for key, url in urls.iteritems():
            if url[1] and (ics_table_id != "datatable-ics" or not fields or key in fields):
                logger.info("Processing field/group/subgroup " + key)

                child_ics = Node(key, url[0], url[1])
                parent_ics.add_child(child_ics)

                child_ics_json = {"code": key, "field": url[0], "url": url[1], "children": []}
                parent_ics_json["children"].append(child_ics_json)

                get_ics(url[1], child_ics, child_ics_json)

    else:
        ics_rows = ics_table.find_elements_by_css_selector("tbody tr")
        standards, standards_json = get_standards(ics_rows)

        for standard in standards:
            parent_ics.add_child(standard)

        for standard_json in standards_json:
            parent_ics_json["children"].append(standard_json)

    return


def get_standards(ics_rows):
    standards = []
    standards_json = []
    for row in ics_rows:
        if row.get_attribute("class") == "ng-hide odd" or row.get_attribute("class") == "ng-hide even":
            continue
        standard = row.find_element_by_css_selector("td[data-title='Standard and/or project']")
        standard_id = standard.find_element_by_tag_name("a").text
        standard_url = standard.find_element_by_tag_name("a").get_attribute("href")

        standard_title = ""
        try:
            standard_title = standard.find_element_by_css_selector("div.entry-summary").text
        except:
            logger.info(standard_id + " does not provide a description")
            pass

        standard_node = Node(standard_id, standard_title, standard_url)
        standard_json = {"code": re.sub(r"\.", "\.", standard_id), "field": standard_title, "url": standard_url}

        standards.append(standard_node)
        standards_json.append(standard_json)

    return standards, standards_json


get_ics(iso_url, root_ics, tree_ics)

logger.info("ISO links have been visited")

with open(csv_output, 'a') as csvfile:
    csvwriter = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
    preorder_visit(root_ics, "", csvwriter)

with open(json_output, 'a') as jsonwriter:
    jsonwriter.write(json.dumps(tree_ics, indent=True))
    jsonwriter.close()