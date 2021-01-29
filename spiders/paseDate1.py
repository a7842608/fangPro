import scrapy
import requests
import urllib
import requests
from lxml import etree
import json
import time
import scrapy
from fangPro.spiders.MyDb import MyDb
class Pasedate1Spider(scrapy.Spider):
    name = 'paseDate1'
    allowed_domains = ['hz.ke.com']
    start_urls = ['http://hz.ke.com/']

    def parse(self, response):
    	# time.sleep(1)
        post_param = {'action': '', 'start': '0', 'limit': '1'}
        return_data = requests.get(
            "https://ajax.ke.com/map/search/ershoufang/?callback=jQuery111106799895903561037_1595584416215&city_id=330100&group_type=community&max_lat=30.251196&min_lat=30.245767&max_lng=120.210239&min_lng=120.155047&filters=%7B%7D&request_ts=1595584547625&source=bkpc&authorization=005cf63ab58d68b7c58efbe075d218ea&_=1595584416227",
            data=post_param, verify=False)

        # print(len(json.loads(return_data.text.split("(")[1].split(")")[0])["data"]['list']))
        # 遍历json
        datas = json.loads(return_data.text.split("(")[1].split(")")[0])["data"]['list']
        # print(datas)
        items = datas.items()
        for key, value in items:
            print(str(key) + '=' + str(value))
            print("小区名称==" + value['name'])
            print("单价==" + str(value['unit_price']))
            print("数量==" + str(value['count']))
            print("经度==" + str(value['longitude']))
            print("纬度==" + str(value['latitude']))

            one = value['name']
            two = str(value['unit_price'])
            three = str(value['count'])
            four = str(value['longitude'])
            five = str(value['latitude'])

            sql = 'insert into map_village(village_name,house_price,house_count,longitude,latitude) values (%s,%s,%s,%s,%s);'
            # 数据库链接
                        #ip       #用户       #密码      #数据库名
            test = MyDb('localhost', 'root', 'mysql', 'fang_data')
            # 执行sql语句
            # '+one+', '+two+', '+three+', '+four+', '+five+'
            test.insertInfo(sql, (one, two, three, four, five))
            test.close()
        yield scrapy.Request(return_data, callback=self.parse)
