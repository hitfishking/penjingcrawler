# coding: utf-8
# ------------------------------------------
# 爬取中国知网《中国花卉盆景》杂志1985~2013年杂志目录；
# 使用配置文件，保存爬取任务参数；
# 使用mongodb存储爬取到的目录内容；
# 用urllib2获取page，用BeautifulSoup抽取数据；
# ------------------------------------------
import urllib2
from bs4 import BeautifulSoup
from pymongo import MongoClient

# Read configs from .ini file.
Year_Start = 1985
Year_End = 2013
Months = 12
Base_Url = 'http://wuxizazhi.cnki.net/Magazine/ZGHP'  # 201301.html

# Connect to mongo server, and get the magazines collection.
# url在‘NoSQL Manager for MongoDB’的UI界面的connection管理页面中获得。
db_client = MongoClient('mongodb://root:example@localhost:27017/?authSource=MagazinesDB')
db = db_client.MagazinesDB
penjing = db.penjing

### Loop through all pages on the web, construct the json data bottom-up.
for i_year in range(Year_Start,Year_End+1):
    for i_month in range(1,Months+1):
        # Make page url
        i_url = Base_Url + str(i_year) + str(i_month).zfill(2) + '.html'
        print(i_url)

        # Get page by url.
        # response = urllib2.urlopen(i_url)
        # html_doc = response.read()
        # print(html_doc)
        html_doc = urllib2.urlopen(i_url).read()

        # Parse page into Soup.
        i_page = BeautifulSoup(html_doc, 'lxml')
        list1 = i_page.find_all('span', 'litext')  # len(list1)=42   //可用ipython进行局部语句的试验
        list2 = i_page.find_all('span', 'litext2')  # len(list2)=42
        # print 'len(list1)=' + str(len(list1)), 'len(list2)=' + str(len(list2))

        ## Loop through all items in the dir; pop items into arr2.
        arr2 = []   # Act as the value of a nested sub-level document.
        for j in range(len(list1)):
            article_name = str.strip(list1[j].strong.string.encode('utf-8'))
            article_page = str.strip(list2[j].a.string.encode('utf-8'))
            # print article_name + "  " + article_page

            # Populate json2 and arr2.
            json_tmp = {}  # 每次循环构造一个此对象，append才不会受影响.
            json_tmp['article_name'] = article_name
            json_tmp['article_page'] = article_page
            arr2.append(json_tmp)

        # Construct the top-level document.
        json_tmp2 = {}
        json_tmp2.pop('_id', None)  # mongo.insert_one()时会自动增加此_id项，去除之.
        json_tmp2['year'] = str(i_year)
        json_tmp2['month'] = str(i_month)
        json_tmp2['dir'] = arr2

        # Save article info into mongodb.
        penjing.insert_one(json_tmp2)
