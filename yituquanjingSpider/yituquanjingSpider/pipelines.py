# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from config import host,port,user,passwd,charset,db
import pymysql
import time
import requests

class YituquanjingspiderPipeline(object):

    basepath = 'D://spiderFile/yitu/'

    def __init__(self):
        self.conn = pymysql.connect(host=host, port=port, user=user, passwd=passwd, db=db, charset=charset)
        self.cursor = self.conn.cursor(cursor=pymysql.cursors.DictCursor)


    def process_item(self, item, spider):
        sql = ("INSERT yitu_images(title,url,info_type,image_url"
        ") VALUES (%s,%s,%s,%s)")
        values =[item['title'],item['url'],item['infoType'],item['imageUrl']]      
        self.cursor.execute(sql,values)
        self.conn.commit()
        # t = time.time()
        # fileName = self.basepath+item['title']+str(int(round(t * 1000)))+'.jpg'
        # self.save_file(item['url'],fileName)
        return item

    # def save_file(self,url,fileName):
    #     r = requests.get(url)
    #     with open(fileName, 'wb') as f:
    #         f.write(r.content)
