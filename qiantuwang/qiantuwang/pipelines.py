# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import requests

class QiantuwangPipeline(object):
    def process_item(self, item, spider):
        print(item)
        fileName = item['name']
        url = item['url']
        index = url.find(".")
        fileName = "D://files/"+fileName+'.gif'
        print(fileName)
        r = requests.get(url)
        with open(fileName, 'wb') as f:
            f.write(r.content) 
        return item
