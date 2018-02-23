import pandas as pd
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import argparse

import exceptions
import json
import datetime
import traceback

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--input", required=True, help="comma-separated list of ISO standards to be collected")
ap.add_argument("-o", "--output", required=True, help="path to the output JSON file")
args = vars(ap.parse_args())

input_file = args['input']
output_file = args['output']

phantomjs_exec_path='/usr/local/bin/phantomjs'

# Create a new instance of Firefox driver.
driver = webdriver.Firefox()


def get_standard_info(url):
    standard = {}

    driver.get(url)

    try:
        heading = driver.find_element_by_css_selector("div.heading-condensed")
        id = heading.find_element_by_id("itemReference").text
        title = heading.find_element_by_css_selector("h3[itemprop='description']").text

        preview_url = ""
        try:
            preview_url = heading.find_element_by_css_selector("a").get_attribute("href")
        except:
            pass

        par_description = driver.find_elements_by_css_selector("div.col-md-7 div[itemprop='description'] p")
        description = ""
        if par_description is not None and len(par_description) > 1:
            description = par_description[1].text

        general_info = driver.find_element_by_xpath('//div[@class="well clearfix"]')
        rows = general_info.find_elements_by_css_selector("ul.refine li div.row div.col-sm-6")
        current_status = rows[0].find_element_by_tag_name("span").text
        publication_date = ""
        try:
            publication_date = rows[1].find_element_by_tag_name("span").text
        except:
            pass
        edition = rows[2].text
        number_of_pages = ""
        try:
            number_of_pages = rows[3].text
        except:
            pass

        tc = general_info.find_element_by_css_selector("div.clearfix")
        tc_a = tc.find_element_by_xpath('//div[@class="entry-name entry-block"]').find_element_by_tag_name("a")
        tc_name = tc_a.text
        tc_url = tc_a.get_attribute("href")
        tc_title = tc.find_element_by_css_selector("div.entry-title").text

        ics_all = general_info.find_elements_by_xpath('//dl[@class="dl-inline no-bottom-margin"]/dd')
        ics_list = []

        for ics in ics_all:
            ics_a = ics.find_element_by_xpath('//div[@class="entry-name entry-block"]').find_element_by_tag_name("a")
            ics_name = ics_a.text
            ics_url = ics_a.get_attribute("href")
            ics_title = tc.find_element_by_css_selector("div.entry-title").text

            ics_list.append({'name': ics_name, 'url': ics_url, 'title': ics_title})

        #stage = driver.find_element_by_xpath('//li[@class="active"]/a/span[@class="stage-code"]').text

        sections_list = get_preview(preview_url)

        standard['datetime'] = str(datetime.datetime.utcnow()).split('.')[0]
        standard['url'] = url
        standard['id'] = id
        standard['title'] = title
        standard['description'] = description
        standard['general_information'] = {
            'current_status': current_status,
            'publication_date': publication_date,
            'edition': edition,
            'number_of_pages': number_of_pages,
            'tc': {'name': tc_name, 'url': tc_url, 'title': tc_title},
            'ics': ics_list
        }
        #standard['stage'] = stage
        standard['preview'] = {
            'url': preview_url,
            'sections': sections_list
        }

    except:
        error = traceback.format_exc()
        print("Error occurred while crawling " + url + " - Message: " + error)

    return standard


def get_preview(url):
    sections_list = []

    try:
        driver.get(url)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME,"sts-standard")))

        sections_all = driver.find_elements_by_xpath('//div[@class="sts-standard"]/div[@class="sts-section"]')

        for section in sections_all:
            section_name = section.find_element_by_class_name("sts-sec-title").text
            section_text = section.text
            sections_list.append({'name': section_name, 'text': section_text})
    except:
        pass

    return sections_list


df = pd.read_csv(input_file, header=None)

# urls are expected to be in the second column
urls=set(df[2])

with open(output_file,'w') as tempwrite:
    tempwrite=open(output_file, 'w')
    standards_list = []

    tempwrite.write("[")
    first_row=True

    for url in list(urls):
        print("Processing " + url)
        standard = get_standard_info(url)
        if standard:
            # standards_list.append(standard)
            if not first_row:
                tempwrite.write(",")
            tempwrite.write(json.dumps(standard, indent=True))
            first_row=False

    # TODO Write json iteratively
    # json_list = json.dumps(standards_list, indent=True)
    # tempwrite.write(json_list)
    tempwrite.write("]")
    tempwrite.close()