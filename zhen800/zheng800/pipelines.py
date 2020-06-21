# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import os
import requests

class Zheng800Pipeline(object):
    basepath = 'D://spiderFile/zheng8002/'

    def process_item(self, item, spider):
        print(item)
        package = item['title']
        frist_url = item['frist_url']
        urls = item['urls']
        urls1 = item['urls1']
        # self.mkdir(self.basepath+package)
        path = self.basepath
        # 保存标题图
        fileName = path + frist_url[frist_url.rfind('/'):]
        r = requests.get(frist_url)
        with open(fileName, 'wb') as f:
            f.write(r.content) 
        # 保存详情图
        for url in urls:
            fileName = path + url[url.rfind('/'):]
            r = requests.get(url)
            with open(fileName, 'wb') as f:
                f.write(r.content)
        for url in urls1:
            fileName = path + url[url.rfind('/'):]
            r = requests.get(url)
            with open(fileName, 'wb') as f:
                f.write(r.content)        
        return item


    def mkdir(self,path):
        # 去除首位空格
        path=path.strip()
        # 去除尾部 \ 符号
        path=path.rstrip("\\")
    
        # 判断路径是否存在
        # 存在     True
        # 不存在   False
        isExists=os.path.exists(path)
    
        # 判断结果
        if not isExists:
            # 如果不存在则创建目录
            os.makedirs(path) 
            print(path+' 创建成功')
            return True
        else:
            # 如果目录存在则不创建，并提示目录已存在
            print(path+' 目录已存在')
            return False
