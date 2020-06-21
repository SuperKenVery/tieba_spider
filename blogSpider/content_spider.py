# -*- coding: UTF-8 -*-
__author__ = 'Chengrongkai'

import pymysql
import requests
from spiders import *
from config.config import *
import time
import datetime
from lxml import etree
from selenium import webdriver
# 爬虫类 获取文章内容
class ContentSpider:
    # 初始化
    def __init__(self):
        self.databaseUtil = DatabaseUtil()

    # 采集过程
    def start_spider(self):
        for config_type in config_spiders:
            try:
                spider = BaseSpider()
                if(config_type == 1):
                   spider = CnblogsSpider()
                elif(config_type == 2):
                   spider = DongfangcaifuSpider()      
                elif(config_type == 3):
                   spider = OsChinaSpider()   
                elif(config_type == 4):
                   spider = CsdnSpider()
                elif(config_type == 5):
                   spider = JuejinSpider()    
                elif(config_type == 6):
                   spider = DazhongyuleSpider()     
                elif(config_type == 7):
                   spider = WeixingongzhonghaoSpider() 
                elif(config_type == 8):
                   spider = TonghuashunNewsSpider()     
                data = spider.start_spider()
                self.save_data(data)
            except Exception as e:
                print(e)
                continue
        # 关闭数据库链接
        self.databaseUtil.close()
        print('全部采集任务执行完毕')
        
    # 保存至数据库
    def save_data(self,data):
        print(data)
        for item in data:
            self.databaseUtil.save_articles(item)
        
    
    # 随机取出几篇文章
    @classmethod
    def get_articles(self,num):
        databaseUtil = DatabaseUtil()
        data = databaseUtil.get_articles(num)
        databaseUtil.update_articles(data)
        databaseUtil.close()
        return data

        


# 数据库工具类
class DatabaseUtil:
    def __init__(self):
        self.conn = pymysql.connect(host=host, port=port, user=user, passwd=passwd, db=db, charset=charset)
        self.cursor = self.conn.cursor(cursor=pymysql.cursors.DictCursor)

    
    # 保存至数据库
    def save_articles(self,item):
        sql = ("INSERT articles(title,content,origin_url,cover_images,origin_name,has_publish"
        ") VALUES (%s,%s,%s,%s,%s,%s)")
        values =[item['title'],item['content'],item['origin_url'],item['cover_images'],item['origin_name'],0]      
        self.cursor.execute(sql,values)
        self.conn.commit()
    
    # 随机获取五篇文章
    def get_articles(self,num):
        sql = "SELECT id,title,content,origin_url,cover_images from articles where has_publish = 0 ORDER BY RAND() limit {}".format(num)
        self.cursor.execute(sql)
        data = self.cursor.fetchall()
        return data
    # 更新已发布的文章的状态
    def update_articles(self,data):
        for item in data: 
            now = datetime.datetime.now()
            now = now.strftime('%Y-%m-%d %H:%M:%S')   
            sql = "UPDATE articles SET has_publish = 1,publish_time = %s where id = %s"
            values = [now,item['id']]
            self.cursor.execute(sql,values)
            self.conn.commit()
    
    def save_images(self,item):
        sql = "INSERT images(href,has_publish) VALUES (%s,0)"
        values =[item.replace('_s.','.')]      
        self.cursor.execute(sql,values)
        self.conn.commit()
    
    def get_image(self):
        sql = "SELECT id,href from images where has_publish = 0 ORDER BY RAND() limit 1"
        self.cursor.execute(sql)
        data = self.cursor.fetchone()
        return data
    def update_image(self,item):   
        now = datetime.datetime.now()
        now = now.strftime('%Y-%m-%d %H:%M:%S')   
        sql = "UPDATE images SET has_publish = 1,publish_time = %s where id = %s"
        values = [now,item['id']]
        self.cursor.execute(sql,values)
        self.conn.commit()

    # 关闭数据库链接
    def close(self):
        self.conn.close()

# 封面图工具类
class ImageUtil:
    base_url = 'http://sc.chinaz.com/tupian/'
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en',
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
    }


    # 爬取封面图
    def images_spider(self):
        # data = []
        for i in range(10):
            url = self.base_url+'index_{}.html'.format(i+2)
            browser = webdriver.Chrome(driver_path)
            browser.implicitly_wait(20)
            try:
                browser.get(url=url)
            except:
                print("加载页面太慢，停止加载，继续下一步操作")
                browser.execute_script("window.stop()")
            time.sleep(3)
            browser.execute_script("window.scrollTo(0,document.body.scrollHeight)")
            time.sleep(2)
            html_doc = browser.page_source
            browser.quit()
            html = etree.HTML(html_doc)
            hrefs = html.xpath('//*[@id="container"]/div/div/a/img/@src')
            print(hrefs)
            self.save_data(hrefs)
            
            # data = data+hrefs
            
            
        # return data
            
    # 保存爬取的数据
    def save_data(self,data):
        database_util = DatabaseUtil()
        for item in data:
            database_util.save_images(item)
        database_util.close()

    # 获取一张图片地址
    @classmethod
    def get_one(self):
        database_util = DatabaseUtil()
        image = database_util.get_image()
        database_util.update_image(image)
        database_util.close()
        return image['href']

    


