"""
采集空气质量的数据
目标网站：http://www.pm25.in/
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

class kongqizhiliang:
    DEFAULT_REQUEST_HEADERS = {
      'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
      'Accept-Language': 'en',
      'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
    }
    url = 'http://www.pm25.in/{}'
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
        city_fail = []
        for city_name in city_config:
            try:
                city_url = self.url.format(self.get_code(city_name))
                response = requests.get(url=city_url,headers=self.DEFAULT_REQUEST_HEADERS)
                print(response.text)
                html = etree.HTML(response.text)
                item = dict()
                # 城市名称
                # city_name= html.xpath('//div[@class="span12 avg"]/div/div[@class="city_name"]/h2/text()')
                item['city_name'] = city_name
                # 空气质量等级
                level = html.xpath('//div[@class="span12 avg"]/div/div[@class="level"]/h4/text()')
                item['level'] = re.sub('\s','',level[0])
                # 数据更新时间
                live_data_time = html.xpath('//div[@class="span12 avg"]/div/div[@class="live_data_time"]/p/text()')
                item['live_data_time'] = live_data_time[0].replace('数据更新时间：','')
                update_time = item['live_data_time']
                # 数值单位
                live_data_unit = html.xpath('//div[@class="span12 avg"]/div/div[@class="live_data_unit"]/text()')
                item['live_data_unit'] = re.sub('\s','',live_data_unit[0].replace('数值单位：',''))
                # 数值列表
                values = html.xpath('//div[@class="span12 avg"]/div[@class="span12 data"]/div/div[@class="value"]/text()')
                # 数值类型
                captions = html.xpath('//div[@class="span12 avg"]/div[@class="span12 data"]/div/div[@class="caption"]/text()')
                for i in range(len(captions)):
                    if('AQI' in captions[i]):
                        item['AQI'] = re.sub('\s','',values[i])
                    elif('PM2.5/1h' in captions[i]):
                        item['PM2.5/1h'] = re.sub('\s','',values[i])
                    elif('PM10/1h' in captions[i]):
                        item['PM10/1h'] = re.sub('\s','',values[i])
                    elif('CO/1h' in captions[i]):
                        item['CO/1h'] = re.sub('\s','',values[i])
                    elif('NO2/1h' in captions[i]):
                        item['NO2/1h'] = re.sub('\s','',values[i])
                    elif('O3/1h' in captions[i]):
                        item['O3/1h'] = re.sub('\s','',values[i])
                    elif('O3/8h' in captions[i]):
                        item['O3/8h'] = re.sub('\s','',values[i])
                    elif('SO2/1h' in captions[i]):
                        item['SO2/1h'] = re.sub('\s','',values[i])
                #对健康影响状况
                affect = html.xpath('//div[@class="affect"]/p/text()')
                item['affect'] = re.sub('\s','',affect[0].replace('对健康影响情况：',''))
                primary_pollutant = html.xpath('//div[@class="primary_pollutant"]/p/text()')
                # 首要污染物
                item['primary_pollutant'] = re.sub('\s','',primary_pollutant[0].replace('首要污染物：',''))
                action = html.xpath('//div[@class="action"]/p/text()')
                # 建议采取的措施
                item['action'] = re.sub('\s','',action[0].replace('建议采取的措施：',''))
            
                self.save_mysql(item)
                success_count = success_count+1
                log_text = '采集的城市:{},采集的结果:{}'.format(item['city_name'],'成功')
                self.save_log({'log_type':'0','log_text':log_text})
            except Exception as e:
                print(e)
                log_text = '采集的城市:{},采集的结果:{}'.format(city_name,'失败')
                city_fail.append(city_name)
                self.save_log({'log_type':'1','log_text':log_text})
                pass
            continue
        log_text = '采集完成,成功采集的城市数:{},采集失败的城市为{}'.format(
                success_count,"、".join(city_fail))
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
        print(data)
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
