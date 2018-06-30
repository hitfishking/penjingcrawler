# coding: utf-8
# ------------------------------------------
# 本项目是"offline task processing"类应用，data flow各环节应尽量模块化，遵循一套处理框架；
# utility文件就是将基本功能提炼出来，走出软件设计模式化的第一步。
# ------------------------------------------
import urllib2
from bs4 import BeautifulSoup
from pymongo import MongoClient
import ConfigParser

# Read configs from .ini file.
website_meta = {}   # visible in host file.
mongodb_meta = {}
coll = None

# Initialize the platform which controller based on.
# Read config info; get connected to dbs;
def init_base_platform():
    def read_configs():
        cf = ConfigParser.ConfigParser()
        cf.read('./config.ini')

        for item in cf.items('website'):
            website_meta[str(item[0])] = item[1]
        for item in cf.items('mongodb'):
            mongodb_meta[str(item[0])] = item[1]
        # print website_meta, mongodb_meta

    def get_mongo_collection():
        db_client = MongoClient(mongodb_meta.get('db_url'))
        test2 = db_client.MagazinesDB.test2
        return test2

    read_configs()
    global coll
    coll = get_mongo_collection()

#----------------------------------------------------
# Get html page from website.
def get_htmldoc_from_web(i_year, i_month):
    # Make page url
    i_url = website_meta.get("base_url") + str(i_year) + str(i_month).zfill(2) + '.html'
    print(i_url)

    # Get page by url.
    response = urllib2.urlopen(i_url)
    html_doc = response.read()
    return html_doc

# Parse page by Soup into lists.
def get_datalist_from_soup(html_doc):

    page_dom = BeautifulSoup(html_doc, 'lxml')
    list1 = page_dom.find_all('span', 'litext')   # len(list1)=42
    list2 = page_dom.find_all('span', 'litext2')  # len(list2)=42

    return list1, list2

# Parse lists into json.
def make_json_from_lists(list1, list2, i_year, i_month):

    arr2 = []
    for j in range(len(list1)):
        article_name = str.strip(list1[j].strong.string.encode('utf-8'))
        article_page = str.strip(list2[j].a.string.encode('utf-8'))
        # print article_name + "  " + article_page

        # Construct level2 document json.
        json_level2 = {}
        json_level2['article_name'] = article_name
        json_level2['article_page'] = article_page
        arr2.append(json_level2)

    # Construct level1 document json.
    json_level1 = {}
    json_level1.pop('_id', None)  # mongo.insert()时会自动增加此_id项，去除之.
    json_level1['year'] = str(i_year)
    json_level1['month'] = str(i_month)
    json_level1['dir'] = arr2

    return json_level1

# Insert level1 json to mongodb.
def insert_json_to_mongodb(p_json):
    coll.insert_one(p_json)