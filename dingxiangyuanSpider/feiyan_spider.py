import re
import time
import json
import datetime
import requests
import pymysql
import pandas as pd
import os

"""
采集丁香园国外的疫情数据
"""
class VirusSupervise(object):
    def __init__(self):
        self.url = 'https://3g.dxy.cn/newh5/view/pneumonia?scene=2&clicktime=1579582238&enterid=1579582238&from=timeline&isappinstalled=0'
        self.all_data = list()
        host_ip = "127.0.0.1"  # 你的mysql服务器地址
        host_user = "xxx" 数据库用户名
        password = "xxx"  # 你的mysql密码
        db = 'xxx' 数据库名
        port = 3306
        charset= 'utf8'
        self.conn = pymysql.connect(host=host_ip, port=port, user=host_user, passwd=password, db=db, charset=charset)
        self.cursor = self.conn.cursor(cursor=pymysql.cursors.DictCursor)

    def request_page(self):
        """
        请求页面数据
        """
        res = requests.get(self.url)
        res.encoding = 'utf - 8'
        pat0 = re.compile('window.getListByCountryTypeService2true = ([\s\S]*?)</script>')
        data_list = pat0.findall(res.text)
        data = data_list[0].replace('}catch(e){}', '')
        true = True
        false = False
        data = eval(data)
        return data



    def getStatisticsData(self,url,province_name):
        reponse = requests.get(url)
        json_data = reponse.json()
        data = json_data['data']
        for item in data:
            dateId = item['dateId']
            item['modify_time'] = time.strptime(str(dateId), "%Y%m%d")
            item['province_name'] = province_name
            self.save_incr_mysql(item)
        # 保存所有数据至json文件
        update_time = time.strftime('%Y-%m-%d',time.localtime(time.time()))
        self.save_incr_json(data,province_name,update_time)

    def filtration_data(self):
        """
        过滤数据
        """
        data = self.request_page()
        print(data)
        result = []
        for item in data:
            # 省份/国家
            provinceName = item['provinceName']
            provinceId = item['provinceId']
            # 国家/州
            continents = item['continents']
            # 当前确诊人数
            currentConfirmedCount = item['currentConfirmedCount']
            # 确诊总人数
            confirmedCount = item['confirmedCount']
            # 治愈人数
            curedCount = item['curedCount']
            # 死亡人数
            deadCount = item['deadCount']
            # 疑似病例
            suspectedCount = item['suspectedCount']
            # 城市类型
            countryType = item['countryType']
            # 更新时间
            if('中国' == provinceName):
                modifyTime = datetime.datetime.now()
            else:
                modifyTime = item['modifyTime']
                modifyTime = float(modifyTime/1000)
                timeArray = time.localtime(modifyTime)
                modifyTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
            info = {'province_name':provinceName,'province_id':provinceId,'continents':continents
            ,'current_confirmed_count':currentConfirmedCount,'confirmed_count':confirmedCount,'is_new':1
            ,'cured_count':curedCount,'dead_count':deadCount,'suspected_count':suspectedCount,'country_type':countryType,'modify_time':modifyTime}
            self.save_last_mysql(info)
            result.append(info)
            # 静态数据 每日各项数据的变化
            if(hasattr(item, 'statisticsData')):
                self.getStatisticsData(item['statisticsData'],provinceName)

    def save_incr_json(self,info,province_name,update_time):
        file_dir = os.path.abspath(os.path.join(os.getcwd(), "jsonData"))
        filename= file_dir+'/'+update_time
        if(not os.path.exists(filename)):
            os.makedirs(filename)
        filename = filename+'/'+province_name+'.json'
        with open(filename,'w',encoding = 'utf-8') as file_obj:
            json.dump(info,file_obj,ensure_ascii=False)


    # 保存数据增长趋势到数据库
    def save_incr_mysql(self,item):
        # 
        query_sql = 'select count(1) as count from feiyan_incr where modify_time = %s and province_name = %s'
        values = [item['modify_time'],item['province_name']]
        self.cursor.execute(query_sql,values)
        data = self.cursor.fetchone()
        if(data['count'] == 0):
            sql = ("INSERT feiyan_incr(province_name,modify_time,confirmed_count,confirmed_incr\
            ,cured_count,cured_incr,dead_count,dead_incr,current_confirmed_count,current_confirmed_incr"
            ") VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)")
            values =[item['province_name'],item['modify_time'],item['confirmedCount'],item['confirmedIncr'],item['curedCount']
            ,item['curedIncr'],item['deadCount'],item['deadIncr'],item['currentConfirmedCount'],item['currentConfirmedIncr']]      
            self.cursor.execute(sql,values)
            self.conn.commit()

    # 保存最新的数据到数据库
    def save_last_mysql(self,item):
        # 更新所有历史数据的is_new字段
        update_sql = 'update feiyan_data set is_new = 0 where is_new = 1 and province_name = %s'
        values= [item['province_name']]
        self.cursor.execute(update_sql,values)
        self.conn.commit()
        sql = ("INSERT feiyan_data(province_name,province_id,continents,current_confirmed_count\
        ,confirmed_count,cured_count,dead_count,suspected_count,country_type,modify_time,is_new"
        ") VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)")
        values =[item['province_name'],item['province_id'],item['continents'],item['current_confirmed_count'],item['confirmed_count']
        ,item['cured_count'],item['dead_count'],item['suspected_count'],item['country_type'],item['modify_time'],item['is_new']]      
        self.cursor.execute(sql,values)
        self.conn.commit()


if __name__ == '__main__':
    sup = VirusSupervise()
    sup.filtration_data()
