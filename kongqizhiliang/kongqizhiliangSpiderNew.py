"""
采集空气质量的数据
目标网站：http://sthjt.hubei.gov.cn/hjsj/
"""
import requests
from lxml import etree
import re
from xpinyin import Pinyin
import pymysql
import sys
from settings.config import *
from utils import RedisUtil
import datetime
import json
from selenium import webdriver

class kongqizhiliang:
    DEFAULT_REQUEST_HEADERS = {
      'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
      'Accept-Language': 'en',
      'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
    }
    url = 'http://sthjt.hubei.gov.cn/wcmapi/service/aqi.xhtml'
    redis_key = 'kongqi:config_city'
    update_time = 'kongqi:update_time'
    # 汉字转拼音
    pinyin = Pinyin()

    def __init__(self):
        self.conn = pymysql.connect(host=host, port=port, user=user, passwd=passwd, db=db, charset=charset)
        self.cursor = self.conn.cursor(cursor=pymysql.cursors.DictCursor)

    # 将城市名转化为code
    def get_code(self,city_name):
        return self.pinyin.get_pinyin(city_name, '' )

    def get_city_config(self):
        redis_util = RedisUtil.get_redis()
        city_list = redis_util.list_get_range(self.redis_key)
        return city_list

    def update_spider_time(self,update_time):
        redis_util = RedisUtil.get_redis()
        redis_util.str_set(self.update_time,update_time)

    def get_data(self):   
        city_config = self.get_city_config()
        log_text = '采集开始,准备采集的城市:{},计划采集的数据量:{}'.format(city_config,len(city_config))
        self.save_log({'log_type':'2','log_text':log_text})
        success_count = 0
        update_time = ''
        driverPath = 'browser\\chromedriver.exe'
        options = webdriver.ChromeOptions()
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
                # options.add_argument(('--proxy-server=http://' + ip))
        browser = webdriver.Chrome(options=options, executable_path=driverPath)
        browser.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
                    "source": """
        Object.defineProperty(navigator, 'webdriver', {
        get: () => undefined
        })
        """
                })
        browser.get(self.url)
        html = browser.page_source
        browser.quit()
        # print(html)
        reponse = etree.HTML(html)
        data = reponse.xpath('//body/text()')[0]
        json_data = json.loads(data)
        # print(json_data)
        result_list = json_data['data']['hour']
        print(result_list)
        for result in result_list:
            item = dict()
            item['affect'] = result['AFFECTINFO']
            item['action'] = result['SUGGEST']
            if('AQIPRIMPOLLUTE' in result):
                item['primary_pollutant'] = result['AQIPRIMPOLLUTE']
            else:
                item['primary_pollutant'] = '无'
            item['AQI'] = result['AQI']
            item['PM2.5/1h'] = result['PM25']
            item['PM10/1h'] = result['PM10']
            item['CO/1h'] = result['CO']
            item['NO2/1h'] = result['NO2']
            item['O3/1h'] = result['O3']
            item['O3/8h'] = result['O3_2']
            item['SO2/1h'] = result['SO2']
            item['city_name'] = result['POINTNAME']
            item['level'] = result['CODEAQILEVEL']+'（'+result['AQILEVELNAME']+'）'
            item['live_data_time'] = result['MONITORTIME']
            item['live_data_time'] = datetime.datetime.strptime(item['live_data_time'], "%Y年%m月%d日%H") 
            update_time = item['live_data_time'].strftime('%Y-%m-%d %H:%M:%S')
            item['live_data_unit'] = 'μg/m3(CO为mg/m3)'
            if(item['city_name'] in city_config):
                self.save_mysql(item)
                success_count = success_count+1
                log_text = '采集的城市:{},采集的结果:{}'.format(item['city_name'],'成功')
                self.save_log({'log_type':'0','log_text':log_text})
        self.save_log({'log_type':'3','log_text':log_text})
        self.update_spider_time(update_time)

    # 存储运行日志
    def save_log(self,item):
        sql = 'INSERT INTO log(log_text,log_type,created_time) VALUES (%s,%s,%s)'
        values = [item['log_text'],item['log_type'],datetime.datetime.now()]
        self.cursor.execute(sql,values)
        self.conn.commit()

    def save_mysql(self,item):
        # 查询数据库已存在的数据
        query_sql = 'select count(1) as count from kongqizhiliang where city_name= %s and live_data_time = %s'
        values = [item['city_name'],item['live_data_time']]
        self.cursor.execute(query_sql,values)
        data = self.cursor.fetchone()
        # 如果不存在同一城市同一时刻更新的数据，则新增
        if(data['count'] == 0):
            sql = ("INSERT kongqizhiliang(city_name,level,live_data_time,live_data_unit,AQI,PM25_1h,PM10_1h,CO_1h"
            ",NO2_1h,O3_1h,O3_8h,SO2_1h,affect,primary_pollutant,action"
            ") VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)")
            values =[item['city_name'],item['level'],item['live_data_time'],item['live_data_unit'],item['AQI']
            ,item['PM2.5/1h'],item['PM10/1h'],item['CO/1h'],item['NO2/1h'],item['O3/1h'],item['O3/8h']
            ,item['SO2/1h'],item['affect'],item['primary_pollutant'],item['action']]      
            self.cursor.execute(sql,values)
            self.conn.commit()


if __name__ == "__main__":
    app = kongqizhiliang()
    app.get_data()
