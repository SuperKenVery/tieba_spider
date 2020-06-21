
import requests
import pymysql

import threading
from time import strftime, localtime

# 数据库连接信息
# 服务器ip地址
host='127.0.0.1'
# 端口号
port=3306
# 用户名
user='chengrongkai'
# 密码
passwd='kai941021'
# 数据库名
db='web_crawler'
# 字符集
charset='utf8mb4'

def saveFile(loops,data):
    base_path = 'D://spiderFile/sexImage/'
    for item in data:
        url = item['image_url']
        title = item['title']
        info_type = item['info_type']
        r = requests.get(url)
        base_name = info_type+'_'+title+url[url.rfind('/')+1:]
        fileName = base_path+base_name
        with open(fileName, 'wb') as f:
            f.write(r.content)


def main():
    print ('开始处理:'+strftime("%Y-%m-%d %H:%M:%S", localtime()))
    conn = pymysql.connect(host=host, port=port, user=user, passwd=passwd, db=db, charset=charset)
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    sql = "SELECT image_url,title,info_type from yitu_images"
    cursor.execute(sql)
    data = cursor.fetchall()
    print ('共有数据:'+str(len(data))+'条')
    threads_num = 100
    threads = []
    per_thread=int(len(data)/threads_num)
    print ('每个线程处理数据:'+str(per_thread)+'条')
    for i in range(threads_num):
        if threads_num-i==1:    #最后一个线程，分担余下的所有工作量
             t=threading.Thread(target=saveFile,args=(i,data[i*per_thread:]))
        else:
             t=threading.Thread(target=saveFile,args=(i,data[i*per_thread:i*per_thread+per_thread]))
        threads.append(t)
    """创建启动线程"""
    for i in range(threads_num):
        threads[i].start()
    for i in range(threads_num):
        threads[i].join()
    print ('处理完毕:'+strftime("%Y-%m-%d %H:%M:%S", localtime()))


if __name__ == '__main__':
    main()
