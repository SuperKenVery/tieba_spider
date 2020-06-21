# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import os
import requests

class MaijiaxiumotePipeline(object):
    basepath = 'D://spiderFile/maijiaxiumote/'
    basedomain = 'http://www.tbqq.net'
    def process_item(self, item, spider):
        # print(item)
        name = item['name'][0]
        age = item['age'][0]
        position = item['position'][0]
        c_type = item['c_type'][0]
        pics = item['pics']
        picdetails = item['picdetails']
        path = self.basepath+name+'_'+age+'_'+position+'_'+c_type+'_'
        print(path)
        print(pics)
        print(picdetails)
        # 保存详情图
        for url in pics:
            fileName = path + url[url.rfind('/')+1:]
            if(not os.path.exists(fileName)):
                print(url)
                r = requests.get(self.basedomain+'/'+url)
                with open(fileName, 'wb') as f:
                    f.write(r.content)
        for url in picdetails:
            fileName = path + url[url.rfind('/')+1:]
            if(not os.path.exists(fileName)):
                print(url)
                r = requests.get(self.basedomain+'/'+url)
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