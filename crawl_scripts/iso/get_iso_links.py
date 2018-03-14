from selenium import webdriver
from selenium.common import exceptions

from selenium.webdriver import DesiredCapabilities

import csv
import argparse
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-f", "--fields", required=False, help="comma-separated list of ISO fields to be collected")
#ap.add_argument("-o", "--output", required=True, help="path to the output CSV file")
args = vars(ap.parse_args())

fields = args["fields"].split(",") if args["fields"] else []

driver = webdriver.Remote(command_executor='http://localhost:4444/wd/hub',
                                  desired_capabilities=DesiredCapabilities.CHROME)

# Standards catalogue
iso_url = "https://www.iso.org/standards-catalogue/browse-by-ics.html"

css_selectors = ["datatable-ics", "datatable-ics-children", "datatable-ics-projects"]

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


def get_ics(url, list):
    driver.get(url)
    for selector in css_selectors:
        try:
            ics_table = driver.find_element_by_id(selector)
            break
        except exceptions.NoSuchElementException as ex:
           print(ex.message)

    ics_table_id = ics_table.get_attribute("id")
    ics_list = list

    if ics_table_id != "datatable-ics-projects":
        # links = ics_table.find_elements_by_css_selector("tbody tr td.sorting_1 a")
        links = ics_table.find_elements_by_css_selector("tbody tr")

        urls = {get_link_text(link): [link.find_element_by_css_selector("td[data-title='Field']").text.replace('\n', ' '), get_link_href(link)] for link in links}
        for key, url in urls.iteritems():
            if url[1] and (ics_table_id != "datatable-ics" or not fields or key in fields):
                logger.info("Processing field/group/subgroup " + key)
                ics_list.append(key)
                ics_list.append(url[0])
                ics_list.append(url[1])

                get_ics(url[1], ics_list)

    else:
        # ics_value = driver.find_element_by_css_selector("div.heading-condensed h2 strong").text
        ics_rows = ics_table.find_elements_by_css_selector("tbody tr")
        # standards = get_standards(ics_rows, ics_value)
        standards = get_standards(ics_rows, list)
        with open('standards.csv', 'a') as csvfile:
            filewriter = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            for standard in standards:
                filewriter.writerow(standard)

    return;


def get_standards(ics_rows, list):
    standards = []
    for row in ics_rows:
        if row.get_attribute("ng-show") == "wChecked":
            continue
        ics = row.find_element_by_css_selector("td[data-title='Standard and/or project']").find_element_by_tag_name("a")
        standard_url = ics.get_attribute("href")
        standard_title = ics.get_attribute("title")
        stage = row.find_element_by_css_selector("td[data-title='Stage']").find_element_by_tag_name("a")
        # stage_url = stage.get_attribute("href")
        stage_text = stage.text
        tc = row.find_element_by_css_selector("td[data-title='TC']").find_element_by_tag_name("a")
        tc_url = tc.get_attribute("href")
        tc_text = tc.text

        # standards.append([ics_value,ics_text, ics_url, stage_text, stage_url, tc_text, tc_url])

        standard_list = list + [ics, standard_title, standard_url, stage_text, tc_text, tc_url]

        standards.append(standard_list)

    return standards;


get_ics(iso_url, [])

logger.info("ISO links have been visited")
