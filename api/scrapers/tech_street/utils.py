# -*- coding: utf-8 -*-
import time
import requests
import os
import datetime
from bs4 import BeautifulSoup
import urllib
from os.path import exists
import random
import csv

BASE_URL = "https://www.techstreet.com"
BASE_URL_LEN = len(BASE_URL)
TMP_DIR = "http-cache"
out_dir='data'

USER_AGENTS = [
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
    "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
    "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
    "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
    "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
    "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
    "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
    "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52",
]

WORKERS_COUNT = 20


def load_proxy(file_name):
    proxys = []
    with open(file_name) as csvfile:
        proxyreader = csv.reader(csvfile, delimiter=",", quotechar="|")
        for row in proxyreader:
            proxys.append({"http": row[0], "failed_count": 0, "success_count": 0})
    return proxys


PROXY_LIST = load_proxy("proxy.csv")


def load_html(url, attempts=6, timeout=100, use_splash=True, use_cache_if_avail=True, silent=False):

    """

    Gets (fetches from web or loads from the disk cache) the Beautiful souped version of HTML of the page!
    and Saves the fetched date and time for a particular page with its link in a flat file called date_fetched.txt

    :param url: the url of the page to be fetched
    :param attempts: used if splash is not used
    :param timeout: used if splash is not used
    :param use_splash: if True, and splash is running on port 8050, uses splash to render and extract page conteent
    :param use_cache_if_avail: if True, Uses a cached version of the webpage to create the soup.
    :return:
    """
    content = None
    shortened_file_name = None

    date_fetched=open(os.path.join(out_dir, 'date_fetched.txt'), 'a+')

    if url.startswith(BASE_URL):
        scheme, netloc, path, qs, anchor = urllib.parse.urlsplit(url)
        path = urllib.parse.quote(path, "/%")
        qs = urllib.parse.quote_plus(qs, ":&=")
        file_name = TMP_DIR + path + qs + anchor
        if '/standards/' in path and 'product_id' in qs:
            shortened_file_name=TMP_DIR+'/standards/'+qs
        else:
            shortened_file_name=file_name

        available_file_path=None
        if use_cache_if_avail:
            if exists(os.path.join(out_dir, file_name)):
                available_file_path=os.path.join(out_dir, file_name)
            elif exists(os.path.join(out_dir, shortened_file_name)):
                available_file_path=os.path.join(out_dir, shortened_file_name)
            if available_file_path is not None:
                with open(available_file_path, "r") as f:
                    if not silent:
                        print('HTML copy on disk is available, loading from:', available_file_path)
                    content = f.read()

    if not content:
        cap = 5
        base = 1.5
        attempt = 0
        proxy = None
        if use_splash:
            while attempt < attempts:
                try:
                    if not silent:
                        print('Fetching the HTML page from the web... (using splash)', url)
                    response = requests.post("http://127.0.0.1:8050/render.html", # this is the url for the local splash server
                                    json={"url": url})
                    print('DBG:', response.status_code)
                    response.raise_for_status()
                    content = response.content
                    date_fetched.write(url+' '+str(datetime.datetime.now())+'\n')
                    date_fetched.flush()
                    break
                except:
                    wait_time = attempt * 30
                    print('Fetched nothing...waiting', wait_time, 'seconds before attempting:', url)
                    attempt = +1
                    time.sleep(wait_time)
        else:
            while attempt < attempts:
                attempt += 1
                try:
                    agent = random.choice(USER_AGENTS)
                    headers = {"user-agent": agent}
                    proxies = None
                    if attempt < 5:
                        # for the first 4 tries, use proxy
                        # look for a 'good' (with a 'failed_count' of less than 10) random proxy
                        proxy_count = 0
                        while proxy_count < 10:
                            proxy = random.choice(PROXY_LIST)
                            proxy_count += 1
                            if proxy["failed_count"] < 10:
                                break
                    if proxy:
                        proxies = {
                            "http": "http://" + proxy["http"],
                            "https": "http://" + proxy["http"],
                        }
                    if not silent:
                        print('Fetching the HTML page from the web...')
                        print('url:', url, '||', 'headers:', headers, '||', 'proxies:', proxies)
                    response = requests.get(
                        url, headers=headers, timeout=timeout, proxies=proxies
                    )
                    response.raise_for_status()
                    content = response.content
                    date_fetched.write(url + ' ' + str(datetime.datetime.now())+'\n')
                    date_fetched.flush()
                    proxy["failed_count"] -= 1
                    break
                except:
                    proxy["failed_count"] += 1
                    wait_time = min(cap, base * 2 ** attempt)
                    print(f"Retry {url} attempt {attempt} after waiting {wait_time} secs...")
                    time.sleep(wait_time)

        # store the html content on disk
        path_index = shortened_file_name.rfind("/")
        directory = shortened_file_name[0:path_index]
        os.makedirs(os.path.join(out_dir, directory), mode=511, exist_ok=True)
        try:
            if os.path.exists(os.path.join(out_dir, shortened_file_name)):
                print('File already present; filenames are not unique: fix implementation!')
                raise FileExistsError
            with open(os.path.join(out_dir, shortened_file_name), "wb") as file:
                file.write(content)
        except:
            print("Couldn't save file: " + str(shortened_file_name))
            raise RuntimeError

    soup = BeautifulSoup(content, "html.parser")
    date_fetched.close()

    return soup


def get_category_urls(sdo_url, fresh=False):

    # """    takes as input the url to the SDO main page and extracts the categories listed and their links
    #     if unavaialable --> saves the "new products" link instead!
    #
    #     return: a list of dicts of category names and urls to their search page
    # """
    """
    takes as input the url to the SDO main page and extracts the categories listed and their links
    if unavaialable --> saves the "new products" link instead!
    :param sdo_url: the url to the SDO main page
    :return: a list of dicts of category names and urls to their main search pages (which is the same page for each top level category!)
    """

    org_soup = load_html(sdo_url, use_cache_if_avail=not fresh)
    caturls = []
    try:
        view_all = org_soup.find("div", {"id": "explore_products"})
        for sublink in view_all.find("ul").find_all("li"):
            sublink_anchor = sublink.find("a", href=True)
            sublink_name = str(sublink_anchor.text.rstrip().lstrip())
            if "view all" in str(sublink_name).lower():
                sublink_name = "All"
            val = {"name": sublink_name, "link": BASE_URL + str(sublink_anchor["href"])}
            caturls.append(val)

        if len(caturls) == 0:
            val = {
                "name": "All",
                "link": BASE_URL
                + str(
                    org_soup.find("div", {"id": "new_products"}).find("a", href=True)[
                        "href"
                    ]
                ),
            }
            caturls.append(val)
    except:
        val = {
            "name": "All",
            "link": BASE_URL
            + str(
                org_soup.find("div", {"id": "new_products"}).find("a", href=True)[
                    "href"
                ]
            ),
        }
        caturls.append(val)
    return caturls


def get_sdo_urls(all_SDOs_url):

    """
    :param all_SDOs_url: link to the main publishers page, which contains a list of all the SDOs in techstreet (https://www.techstreet.com/publishers/list)
    :return: a list of dict containing name of the SDO and a url to its main page
    """
    sdo_page_soup = load_html(all_SDOs_url)

    SDO_list=[]
    for list_mem in sdo_page_soup.find("ul", {"class": "logos"}).find_all("li"):
        anchors = list_mem.find("p").find("a", href=True)
        link_ext = anchors["href"]
        name = str(anchors.text.rstrip().lstrip())
        url = BASE_URL + str(link_ext)
        SDO_list.append({'name': name, 'sdo_url': url})
    return SDO_list



def get_standards_list(cat_link, fresh=False):

    """
    :param cat_link: url ot the search page for a particular selection of a (sub)category
    :return: paginates through the link and returns a list of all standard links for this (sub)category
    """

    next_page=cat_link
    standards_list=[]
    page=1

    while True:

        try:
            print('Going to a new page:', page, '('+next_page+')')
            cat_page_soup = load_html(next_page, use_cache_if_avail=not fresh)
            list_of_standards_current_page = cat_page_soup.find("ol", {"class": "products_list"}).find_all(
                "li"
            )
        except:
            print('Could not load the next page or find the list of standards. Terminating...')
            return standards_list


        for standard in list_of_standards_current_page:
            try:
                link = (
                    BASE_URL
                    + standard.find("div", {"class": "product_detail"}).find(
                        "a", href=True
                    )["href"]
                )
                print('link:', link)
                standards_list.append(link)
            except:
                pass
        try:
            next_page = BASE_URL + str(
                cat_page_soup.find("div", {"class": "pagination"}).find(
                    "a", {"class": "next_page"}
                )["href"]
            )
            page+=1
        except:
            print('No new pages found. Terminating...')
            return standards_list



def get_standard_details(link, silent=True, fresh=False):
    """
    :param link: the url to the standards page
    :param silent: if True, it will not print any logs
    :return: returns a dictionary containing all the metadata about the standard extracted from its page
    """

    all_metadata={}

    # gets all the details about the standard
    soup = load_html(link, silent=False, use_cache_if_avail=not fresh)
    product_detail = soup.find("div", {"class": "product_detail details"}).find(
        "hgroup"
    )

    try:
        all_metadata['Id']= (
            (product_detail.find("h1").text)
            .replace("\n", "")
            .lstrip()
            .rstrip()
        )
    except:
        all_metadata['Id'] = "N/A"


    try:
        all_metadata['Title'] = product_detail.find("h2").text
    except:
        all_metadata['Title'] = "N/A"


    try:
        fd = soup.find("div", {"class": "about"})
        description = fd.findChildren(recursive=False)
        for i,_ in enumerate(description):
            if i<2 or i%2!=0:
                continue
            if description[i].name[0] == 'h' and description[i+1].name=='div':
                all_metadata[description[i].text]=description[i+1].text
            elif description[i].name=='div':
                all_metadata["full_description"] = description[i].text
    except:
        pass

    try:
        metadata = soup.find("section", {"class": "metadata"}).find("dl").findChildren(recursive=False)
        for i,_ in enumerate(metadata):
            if i%2!=0:
                continue
            if metadata[i].name == 'dt' and metadata[i+1].name=='dd':
                all_metadata[metadata[i].text]=metadata[i+1].text
    except:
        pass

    history = []
    try:
        for link in soup.find("section", {"class": "history"}).find("ol").find_all("a", recursive=True):
            if link.has_attr('href'):
                history.append(link['href'])
        all_metadata['history']= history
    except:
        pass


    return all_metadata


def _find_link_info(soup):
    anchor = soup.find("a", href=True)
    name = anchor.text.replace("+", "").lstrip().rstrip()
    if anchor['href'] == '#':
        is_leaf_node = False
        url=''
    else:
        is_leaf_node = True
        url = BASE_URL + anchor["href"]
    return {'name': name, 'is_leaf': str(is_leaf_node), 'url': url, 'subcats': []}


def _recrusive_dive(cat_soup, hierarchy):

    link_info=_find_link_info(cat_soup)
    name=link_info['name']

    print('link_info:', link_info)

    if name not in hierarchy.keys():
        hierarchy[name] = link_info

    if cat_soup.find("ul"):
        child_cats=cat_soup.find("ul").find_all("li", recursive=False)
        for child_cat_soup in child_cats:
            print('going in...')
            child_cat_name=_recrusive_dive(child_cat_soup, hierarchy)
            print('returns:', child_cat_name, 'to:', name)
            hierarchy[name]['subcats'].append(child_cat_name)

    print('back at:', name, hierarchy[link_info['name']]['subcats'])

    return name

def extract_hierarchy(url, fresh=False):

    """

    :param url: the url to an SDOs search page
    :return: a dict of the categories, their subcategories (to any level of depth) with the standards links in those subcategories
    """

    hierarchy={}
    soup = load_html(url, use_cache_if_avail=not fresh)
    try:
        top_level_categories = soup.find("ul", {"class": "subgroups"}).find_all(
            "li", {"class": "top_level"}
        )
    except:
        # when there are no categories:
        return {'N/A':
        {"name": "N/A",
      "is_leaf": "True",
      "url": url,
      "subcats": []}
                }

    for tlc_soup in top_level_categories:
        _recrusive_dive(tlc_soup, hierarchy)

    return hierarchy

