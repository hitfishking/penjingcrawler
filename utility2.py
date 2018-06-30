# coding: utf-8
# ------------------------------------------
# 本项目是"offline task processing"类应用，data flow各环节应尽量模块化，遵循一套处理框架；
# utility文件就是将基本功能提炼出来，走出软件设计模式化的第一步。
# 区别于utility.py之处在于，使用mongoengine mongodb框架，大幅简化了代码；
# ------------------------------------------
import urllib2
from bs4 import BeautifulSoup
from database import *
import ConfigParser

# Read configs from .ini file.
website_meta = {}   # visible in host file.
mongodb_meta = {}

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

    def get_mongo_collection():
        connect(host=mongodb_meta.get('db_url2'))

    read_configs()
    get_mongo_collection()

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

# Save lists info into mongodb through MongoEngine ORM embedded document mechanism.
def save_lists_by_mongoengine(list1, list2, i_year, i_month):
    i_magazine = Magazine()
    i_magazine.year = str(i_year)
    i_magazine.month = str(i_month)

    for j in range(len(list1)):
        article_name = str.strip(list1[j].strong.string.encode('utf-8'))
        article_page = str.strip(list2[j].a.string.encode('utf-8'))

        i_dir = Dir()
        i_dir.article_name = article_name
        i_dir.article_page = article_page
        i_magazine.dir.append(i_dir)   # Append a single dir item.

    i_magazine.save()
