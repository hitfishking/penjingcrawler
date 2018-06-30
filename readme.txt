# ------------------------------------------
# 爬取中国知网《中国花卉盆景》杂志1985~2013年杂志目录；
# 使用配置文件，保存爬取任务参数；
# 使用mongodb存储爬取到的目录内容；
# 用urllib2获取page，用BeautifulSoup抽取数据；
# ------------------------------------------
http://wuxizazhi.cnki.net/Magazine/ZGHP198504.html
http://wuxizazhi.cnki.net/Magazine/ZGHP198512.html
http://wuxizazhi.cnki.net/Magazine/ZGHP201301.html
从1985~2013，每年12期；29年，348期；
每期有独立页面，url规律简单明确；
--------------------------------------------
MVC框架思想：
penjingcrawler.py只是一个普通的过程化程序；
稍微复杂后，须要纳入一个适当的框架之中。
由于本项目是一个"offline task processing"类应用，不是一个典型的，有UI，有人机交互的Web应用，
故，MVC应用框架并不适合本项目；
对于offline task processing类应用，典型的框架，应该是一个主控制器控制下的，data flow模型；
--------------------------------------------
{
    "_id" : ObjectId("5b2b9c07dab6ed3708a167e6"),
    "years" : 2013.0,
    "months" : [
        {
            "1" : [
                {
                    "article_name" : "海棠花莳养经验谈",
                    "article_page" : "(12)"
                },
                {
                    "article_name" : "水仙花期调控法",
                    "article_page" : "(13)"
                }
            ]
        }
    ]
}
1) find_one()返回的是一个json对象；python支持对python对象的灵活操作；这可以拟补pymongo对象化操作上的不足；
magazines.find_one()['months'][0]['1'][0]['article_name']
magazines.find_one()['months'][0]['1'][0]['article_page']='(99)'
2) insert杂志目录的方法：
   a) 通过循环抓取page上的item数据，构造一个json对象；
   b) magazines.insert_one(json_tmp2)
--------------------------------------------
