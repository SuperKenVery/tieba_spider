import pymysql
from config import *
import datetime

# 数据库工具
class database_util:
    def __init__(self):
        self.conn = pymysql.connect(host=host_ip, port=port, user=host_user, passwd=password, db=db, charset=charset)
        self.cursor = self.conn.cursor(cursor=pymysql.cursors.DictCursor)



    # 存储贴吧数据
    def save_tieba(self,data):
        sql = 'insert tieba(title,create_time,creator,content,link) VALUES (%s,%s,%s,%s,%s)'
        values = [data['title'],data['create_time'],data['creator'],data['content'],data['link']]
        self.cursor.execute(sql,values)
        self.conn.commit()

    def query_tieba(self,link):
        query_sql = 'select count(1) as count from tieba where link = %s'
        values = [link]
        self.cursor.execute(query_sql,values)
        data = self.cursor.fetchone()
        if(data['count'] > 0):
            return True
        else:
            return False

     # 存储贴吧数据
    def save_tieba_reply(self,data):
        sql = 'insert tieba_reply(reply_id,creator,content,link,sex,location) VALUES (%s,%s,%s,%s,%s,%s)'
        values = [data['reply_id'],data['creator'],data['content'],data['link'],data['sex'],data['location']]
        self.cursor.execute(sql,values)
        self.conn.commit()

    def query_tieba_reply(self,reply_id):
        query_sql = 'select count(1) as count from tieba_reply where reply_id = %s'
        values = [reply_id]
        self.cursor.execute(query_sql,values)
        data = self.cursor.fetchone()
        if(data['count'] > 0):
            return True
        else:
            return False
