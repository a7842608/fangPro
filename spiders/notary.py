import scrapy
import pymysql
import requests
from lxml import etree
import uuid
import time
from io import StringIO
from io import open
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfinterp import PDFResourceManager,process_pdf

from fangPro.spiders.CPdf2TxtManager import *



class NotarySpider(scrapy.Spider):
    name = 'notary'
    allowed_domains = ['hz-notary.com']
    start_urls = ['https://www.hz-notary.com/lottery/index?page.pageNum=1']

    def read_base_pdf(self,pdf):
        #pdf = str("E:/B/work/project/lushangLi/fangPro/fangPro/spiders/")+pdf
        print("pdf-------------------")
        print(pdf)
        # resource manager
        rsrcmgr = PDFResourceManager()
        retstr = StringIO()
        laparams = LAParams()
        # device
        device = TextConverter(rsrcmgr, retstr, laparams=laparams)
        process_pdf(rsrcmgr, device, pdf)
        device.close()
        content = retstr.getvalue()
        retstr.close()
        # 获取所有行
        lines = str(content).split("\n")
        return lines
    def parse(self, response):
        time.sleep(1)
        pdfDirNameWrite = ""
        #遍历最外层列表
        lis = response.xpath("//div[@id='content']/div[2]/div[2]/ul/li")
        for li in lis:
            #print(li.xpath("./div/a/@href").get())
            #组装请求摇号结果和意向登记汇总表的地址
            infoUrl = "https://www.hz-notary.com" + li.xpath('./div/a/@href').get()
            post_param = {'action': '', 'start': '0', 'limit': '1'}
            return_data = requests.get(infoUrl, data=post_param,verify=False)
            #print(return_data.text)
            parse_html = etree.HTML(return_data.text)
            liss = parse_html.xpath("//div[@id='content']/div[2]/div[2]/ul/li")
            #for liOne in liss:
            #print(len(liss.xpath('./li')))
            yhjgUrl = parse_html.xpath('//a[contains(text(), "销售摇号结果")]/@href')
            yxdjUrl = parse_html.xpath('//a[contains(text(), "意向登记汇总表")]/@href')
            print("----------------------------------")
            print(yhjgUrl)
            print(yxdjUrl)


            #if len(liss) >= 4:
            time_stamp = time.strftime('%Y-%m-%d-%H-%M-%S', time.localtime(time.time()))
            #=================================摇号结果==================================
            # 摇号结果 请求地址
            #yhjgUrl = liss[2].xpath('./a/@href')[0]
            #获取PDF链接
            if len(yhjgUrl) > 0:
                print(yhjgUrl[0])
                infoUrl = "https://www.hz-notary.com" + yhjgUrl[0]
                print(infoUrl)
                post_param = {'action': '', 'start': '0', 'limit': '1'}
                return_data = requests.get(infoUrl, data=post_param, verify=False)
                # print(return_data.text)
                parse_html2 = etree.HTML(return_data.text)
                print(parse_html2.text)
                #摇号结果 PDF地址
                #yhjg_pdf_url = parse_html.xpath("//div[@class='detail_content']/p[5]/a/@href")[0]
                yhjg_pdf_urlArray = parse_html2.xpath('//a[contains(@title, ".pdf")]/@href')
                print("333333333333")
                print(yhjg_pdf_urlArray)
                if len(yhjg_pdf_urlArray)>0:
                    print("摇号结果pdf地址----------------------------")
                    yhjg_pdf_url = yhjg_pdf_urlArray[0]
                    print(yhjg_pdf_url)
                    #下载PDF到本地
                    r2 = requests.get(yhjg_pdf_url)
                    pdfBaseUrl = time_stamp+".pdf"
                    with open(str(pdfDirNameWrite)+pdfBaseUrl, "wb") as code:
                        code.write(r2.content)
                    print("88888888")
                    print(pdfBaseUrl)
                    #解析本地PDF 并 入库
                    #print(self.read_base_pdf(pdfBaseUrl))
                    cp = CPdf2TxtManager()
                    cp.changePdfToText(str(pdfDirNameWrite) + pdfBaseUrl2)
            if len(yxdjUrl) > 0:
                #=========================================意向登记汇总=======================================
                #意向登记汇总表
                #yxdjUrl = liss[3].xpath('./a/@href')[0]
                # 获取PDF链接
                yxdjInfoUrl = "https://www.hz-notary.com" + yxdjUrl[0]
                print(yxdjInfoUrl)
                return_data = requests.get(yxdjInfoUrl, data=post_param, verify=False)
                parse_html3 = etree.HTML(return_data.text)
                # 意向登记汇总 PDF地址
                #yxdj_pdf_url = parse_html.xpath("//div[@class='detail_content']/p[5]/a/@href")[0]
                yxdj_pdf_urlArray = parse_html3.xpath('//a[contains(@title, ".pdf")]/@href')
                print(parse_html3.text)
                print("444444")
                print(yxdj_pdf_urlArray)
                if len(yxdj_pdf_urlArray)>0:
                    yxdj_pdf_url = yxdj_pdf_urlArray[0]
                    print("意向登记汇总pdf地址----------------------------")
                    print(yxdj_pdf_url)
                    # 下载PDF到本地
                    r = requests.get(yxdj_pdf_url)
                    pdfBaseUrl2 = time_stamp + ".pdf"
                    with open(str(pdfDirNameWrite)+pdfBaseUrl2, "wb") as code:
                        code.write(r.content)
                    # 解析本地PDF 并 入库
                    print("88888888")
                    print(pdfBaseUrl2)
                    #print(self.read_base_pdf(pdfBaseUrl2))
                    cp = CPdf2TxtManager()
                    cp.changePdfToText(str(pdfDirNameWrite)+pdfBaseUrl2)
            next_url = response.xpath("//div[@id='d_page']/form/ul/li[5]/a/@href").get()
            #print(next_url)
            next_url2 = "https://www.hz-notary.com" + next_url

            # 数据库连接
            db_conn = pymysql.connect(db="test",host="127.0.0.1",user="root",password="root",charset="utf8")
            db_cursor = db_conn.cursor()
            sql  = 'insert into test(id,name) values (1,1);'
            db_cursor.execute(sql)
            db_conn.commit()
            db_cursor.close()
            db_conn.close()
            yield scrapy.Request(next_url2, callback=self.parse)



