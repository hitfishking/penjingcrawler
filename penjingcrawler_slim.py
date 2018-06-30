# coding: utf-8
# ------------------------------------------
# 爬取中国知网《中国花卉盆景》杂志1985~2013年杂志目录；
# 使用配置文件，保存爬取任务参数；
# 使用mongodb存储爬取到的目录内容；
# 用urllib2获取page，用BeautifulSoup抽取数据；
# ---------------
# 利用utility文件，尽可能让data flow模式更简洁，明了；
# 在"slim"层面编程，所用到的action，到下层utlity中作为函数实现；
# 主程序中，由controller + monitor构成；
# ------------------------------------------
from utility import *
from aop_monitors import *

@timer   # monitor
def app_contoller():
    init_base_platform()

    Year_Start = int(website_meta.get("year_start"))
    Year_End = int(website_meta.get("year_end"))
    Months = int(website_meta.get("months"))

    for i_year in range(Year_Start, Year_End + 1):
        for i_month in range(1, Months + 1):

            # step1 ~ step4
            html_doc = get_htmldoc_from_web(i_year, i_month)

            list1, list2 = get_datalist_from_soup(html_doc)

            json_level1 = make_json_from_lists(list1, list2, i_year, i_month)

            insert_json_to_mongodb(json_level1)

# Start the controller (decorated with monitor)
app_contoller()

