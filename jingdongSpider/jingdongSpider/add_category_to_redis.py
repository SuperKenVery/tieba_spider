from pymongo import MongoClient
from redis import StrictRedis
import pickle
from jingdongSpider.settings import MONGODB_URL,REDIS_URL
from jingdongSpider.spiders.product_spider import JdProductSpider
"""步骤：
1.在项目文件夹下创建add_category_to_redis.py
1.实现方法  add_category_to_redis:
a.链接mongodb
b.链接redis
c.读取mongodb中分类信息，序列化后，添加到商品爬虫redis_key 指定的list中
d.关闭mongodb"""

def add_category_to_redis():
    #a.链接mongodb
    mongo=MongoClient(MONGODB_URL)
   #b.链接redis
    redis=StrictRedis.from_url(REDIS_URL)
    #c.读取mongodb中分类信息，序列化后，添加到商品爬虫redis_key指定的list中
    #获取分类信息
    collection=mongo['jd']['category']
    #读取分类信息
    cursor=collection.find()
    for category in cursor:
        #序列化字典数据
        data=pickle.dumps(category)
        #添加到商品爬虫redis_key指定的list中
        redis.lpush(JdProductSpider.redis_key,data)
    #d.关闭mongodb
    mongo.close()
if __name__ == '__main__':
    add_category_to_redis()
