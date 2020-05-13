# coding: utf-8
# ------------------------------------------
# 爬取中国知网《中国花卉盆景》杂志1985~2013年杂志目录；
# 使用配置文件，保存爬取任务参数；
# 使用mongodb存储爬取到的目录内容；
# 用urllib2获取page，用BeautifulSoup抽取数据；
# 存储到本地txt文件中；
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
db_client = MongoClient('mongodb://root:example@localhost:27017/?authSource=MagazinesDB')
db = db_client.MagazinesDB
magazines = db.magazines

# Open txt file.
txtfile = open('./penjing_dirs.txt','w')

### Loop through all pages on the web, construct the json data bottom-up.
for i_year in range(Year_Start,Year_End+1):
    for i_month in range(1,Months+1):
        # Make page url
        i_url = Base_Url + str(i_year) + str(i_month).zfill(2) + '.html'
        print(i_url)

        # Get page by url.
        response = urllib2.urlopen(i_url)
        html_doc = response.read()
        # print(html_doc)

        # Parse page into Soup.
        i_page = BeautifulSoup(html_doc, 'lxml')
        list1 = i_page.find_all('span', 'litext')  # len(list1)=42
        list2 = i_page.find_all('span', 'litext2')  # len(list2)=42
        # print 'len(list1)=' + str(len(list1)), 'len(list2)=' + str(len(list2))
        txtfile.write("\n--------------------------------------------\n")
        txtfile.write("年份：" + str(i_year) + "    月份：" + str(i_month) + '\n')
        txtfile.write("--------------------------------------------\n")

        ## Loop through all items in the dir; pop items into arr2.
        arr2 = []   # Act as the value of a nested sub-level document.
        for j in range(len(list1)):
            article_name = str.strip(list1[j].strong.string.encode('utf-8'))
            article_page = str.strip(list2[j].a.string.encode('utf-8'))
            # print article_name + "  " + article_page

            # Save article info into txt file.
            txtfile.write(article_name + "         " + article_page + '\n')

txtfile.flush()
txtfile.close()


