import pymysql
from config import *
import datetime


# 数据库工具
class database_util:
    def __init__(self):
        self.conn = pymysql.connect(host=host_ip, port=port, user=host_user, passwd=password, db=db, charset=charset)
        self.cursor = self.conn.cursor(cursor=pymysql.cursors.DictCursor)

    # 存储学校新闻
    def save_news(self,data):
        sql = 'insert school_news(title,create_time,creator,content,link) VALUES (%s,%s,%s,%s,%s)'
        values = [data['title'],data['create_time'],data['creator'],data['content'],data['link']]
        self.cursor.execute(sql,values)
        self.conn.commit()

    # 查询学校新闻
    def query_news(self,title):
        query_sql = 'select count(1) as count from school_news where title = %s'
        values = [title]
        self.cursor.execute(query_sql,values)
        data = self.cursor.fetchone()
        if(data['count'] > 0):
            return True
        else:
            return False

