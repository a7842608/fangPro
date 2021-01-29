import scrapy
import json
import uuid
import pymysql
import time
########
from fangPro.spiders.MyDb import MyDb


import urllib
import requests
from lxml import etree
import json

import scrapy
from fangPro.spiders.MyDb import MyDb
class XjxfSpider(scrapy.Spider):
    name = 'xjxf'
    allowed_domains = ['land.zzhz.zjol.com.cn']
    start_urls = ['http://land.zzhz.zjol.com.cn/lands_data_list?year=2008']

    def parse(self, response):
        time.sleep(1)
        sites = json.loads(response.body_as_unicode())
        objs = sites['data']
        for obj in objs:
            cityName = obj['cityName']
            print(cityName)
            sql = "insert into diKuai(city_name,year1,cr_date,dk_code,dk_name,lmj,cjj,jddw,yjl,rongl,yt,rmj) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);"
            #               连接数据库
            test = MyDb('localhost', 'root', 'root', 'fang_data')
            test.insertInfo(sql, (obj['cityName'], 2020, obj['yu_endTime'], obj['num'], obj['name'], obj['build_price'], obj['payPrice'], obj['owner'], obj['premium_ratio'], obj['far'], obj['planName'], obj['t_area']))
            test.close()
            years = ["2009", "2010", "2011", "2012", "2013", "2014", "2015", "2016", "2017", "2018", "2019", "2020"]
            for year in years:
                yield scrapy.Request("http://land.zzhz.zjol.com.cn/lands_data_list?year="+year, callback=self.parse)


# 四, 查看周边二手房的价格


