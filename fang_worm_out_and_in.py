# 二, 一房一价

def func_worm():
    import requests, time
    from lxml import html

    etree = html.etree

    url = 'http://www.tmsf.com/newhouse/OpenReport_shownew.htm'

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36',
        'Cookie': 'BSFIT_EXPIRATION=1596239422481; BSFIT_DEVICEID=VHIvNRR_KqoOZsJTzIzT4Y8dEMH-EJw0xc0Ib9ilTa5XClLS-JBtObPtQ7F8yGw26e3N4cuEVt3nYrGN3_4SRTP6v6xDTaFgUQjweQ9v9y5I7-xoefsIrANEMJexoMVNFeT2IreCLM2_vPstEBBcWUW4RbN4Pjx8; br_access_code=bXHeIANj0RQAAAAAn/ojXwAAAADTFw3p; Hm_lvt_bbb8b9db5fbc7576fd868d7931c80ee1=1596193083; gr_user_id=308c87d5-cec7-4f62-bea3-d4bd9c5e7aac; b61f24991053b634_gr_session_id=18409add-f716-4fbc-bd10-ad93f663abfd; b61f24991053b634_gr_session_id_18409add-f716-4fbc-bd10-ad93f663abfd=true; grwng_uid=db4c641d-54da-4cef-9364-3b7f3a166ee4; UM_distinctid=173a4865523a1e-00fe76ea26287c-3323765-1fa400-173a4865524c26; CNZZDATA1253675216=925856595-1596188471-http%253A%252F%252Fwww.tmsf.com%252F%7C1596188471; JSESSIONID=339FBD3EBBE366DEA0F2270795ECAB7E; BSFIT_lg8q0=j7Rf+S0fja03+aj1Ml,jqlejqlejqlejl,jqlejqlejqlejl'
    }

    number = 0
    # 所有小区页翻页
    for a in range(1,500):
        data = {
            'searchoption': 1,
            'searchtype': 1,
            # "page":5
        }

        data["page"] = a
        # data = json.dumps(kv_out)
        time.sleep(1)
        response = requests.post(url, headers=headers, data=data).text

        html = etree.HTML(response)

        # 首页一个页面的数据 -- 获取的是当前页的所有房屋链接
        ret_list = html.xpath('//*[@id="searchpresell"]/div/div[2]/div/a[1]/@href')


        for c in ret_list:
            # http://www.tmsf.com/newhouse/presell_330191_1172978715_6958663.htm  第一页的所有房屋链接
            new_url = 'http://www.tmsf.com' + c
            time.sleep(1)
            print(new_url)
            # 小区内房屋页翻页
            for b in range(1, 10):
                kv_in = {}
                kv_in['page'] = b
                time.sleep(1)
                new_response = requests.get(new_url, headers=headers, params=kv_in).text
                new_html = etree.HTML(new_response)
                new_list = new_html.xpath('/html/body/div[6]/div[8]/div/div[2]/div/table//tr')

                my_dict = {
                    "numberone": "1",
                    "numbertwo": "2",
                    "numberthree": "3",
                    "numberfour": "4",
                    "numberfive": "5",
                    "numbersix": "6",
                    "numberseven": "7",
                    "numbereight": "8",
                    "numbernine": "9",
                    "numberzero": "0",
                    "numberdor": "."
                }

                # 小区名称:
                name = new_html.xpath('/html/body/div[4]/div[1]/div[1]/span/text()')
                village_name = ''.join(name).replace(' ', '').replace('\n', '').replace('\r', '').replace('\t', '')

                file = open('fang_sql_data.sql','a+', encoding='utf-8')

                # 一个页面的数据
                for i in new_list:
                    # 1楼栋
                    one = i.xpath('.//td[1]/a/text()')
                    # str1 = '楼栋:' + ''.join(one)
                    loudong = ''.join(one)

                    # 2房号
                    two = i.xpath('.//td[2]/a/div/text()')
                    # str2 = '房号:' + ''.join(two)
                    room_num = ''.join(two)

                    # 3建筑面积
                    a = i.xpath('.//td[3]/a/div/span/@class')
                    jianzhu = ""
                    for num in a:
                        jianzhu += my_dict[num]
                    # str3 = '建筑面积' + jianzhu
                    covered_area = jianzhu

                    # 4套内建筑面积
                    inner_jianzhu = ""
                    b = i.xpath('.//td[4]/a/div/span/@class')
                    for num in b:
                        inner_jianzhu += my_dict[num]
                    # str4 = '套内建筑面积' + inner_jianzhu
                    inner_area = inner_jianzhu

                    # 5得房率
                    home = ""
                    c = i.xpath('.//td[5]/a/div/span/@class')
                    for num in c:
                        home += my_dict[num]
                    # str5 = '得房率' + home
                    get_house = home

                    # 6申请备案单价
                    Price = ""
                    d = i.xpath('.//td[6]/a/div/span/@class')
                    for num in d:
                        Price += my_dict[num]
                    # str6 = '申请备案单价' + Price
                    apply_price = Price

                    # 7企业承诺装修价格
                    renovation = ""
                    e = i.xpath('.//td[7]/a/div/span/@class')
                    for num in e:
                        renovation += my_dict[num]
                    # str7 = '企业承诺装修价格' + renovation
                    renovation_costs = renovation

                    # 8总价
                    Total = ""
                    f = i.xpath('.//td[8]/a/div/span/@class')
                    for num in f:
                        Total += my_dict[num]
                    # str8 = '总价' + Total
                    total_price = Total

                    # sql保存数据
                    sql = 'INSERT INTO village_value(village_name,building_num,room_num,covered_area,inner_area,get_house,apply_price,renovation_costs,total_price) values ("'+village_name+'", "'+loudong+'", "'+room_num+'",'+covered_area+', '+inner_area+', '+get_house+', '+apply_price+', '+renovation_costs+', '+total_price+')'
                    file.write(sql)
                    file.write('\n')

        number +=a
        print(number)
