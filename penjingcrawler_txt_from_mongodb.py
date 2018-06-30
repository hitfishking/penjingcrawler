# coding: utf-8
# ------------------------------------------
# 爬取中国知网《中国花卉盆景》杂志1985~2013年杂志目录；
# 使用配置文件，保存爬取任务参数；
# 使用mongodb存储爬取到的目录内容；
# 用urllib2获取page，用BeautifulSoup抽取数据；
# 直接从mongodb中读取文件，存储到本地txt文件中；
# ------------------------------------------
from pymongo import MongoClient
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


# Connect to mongo server, and get the collection named 'magazines'.
db_client = MongoClient('mongodb://root:example@192.168.183.129:27017')
db = db_client.MagazinesDB
magazines = db.magazines

# Open txt file.
txtfile = open('./penjing_dirs2.txt','w')

for doc in magazines.find({}):
    i_year = doc['year']
    i_month = doc['month']

    txtfile.write("\n--------------------------------------------\n")
    txtfile.write("年份：" + str(i_year) + "    月份：" + str(i_month) + '\n')
    txtfile.write("--------------------------------------------\n")

    for item in doc['dir']:
        article_name = item['article_name']
        article_page = item['article_page']
        # print article_name + "  " + article_page
        txtfile.write(article_name + "         " + article_page + '\n')

txtfile.flush()
txtfile.close()


