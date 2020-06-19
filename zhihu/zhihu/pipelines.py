# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

from config import host,port,user,passwd,charset,db
import pymysql
import time
from zhihu.items import ZhihuItem,ZhihuActivityItem

class ZhihuPipeline(object):
    def __init__(self):
        self.conn = pymysql.connect(host=host, port=port, user=user, passwd=passwd, db=db, charset=charset)
        self.cursor = self.conn.cursor(cursor=pymysql.cursors.DictCursor)


    def process_item(self, item, spider):
        # 识别需要处理的内容类别
        if isinstance(item,ZhihuItem):
            sql = "insert into zhihu(user_name,sex,user_sign,user_avatar,user_url,user_add) values(%s,%s,%s,%s,%s,%s)"
            param = (item['user_name'],item['sex'],item['user_sign'],item['user_avatar'],item['user_url'],item['user_add'])
        else:
            sql = "insert into zhihu_activity(user_name,title,activity_type) values(%s,%s,%s)"
            param = (item['user_name'],item['title'],item['activity_type'])
        try:
            self.cursor.execute(sql, param)
            self.conn.commit()
        except Exception as e:
            print(e)
            self.conn.rollback()
        return item
