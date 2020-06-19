#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import codecs
import copy
import csv
import json
import math
import os
import random
import sys
import traceback
from collections import OrderedDict
from datetime import date, datetime, timedelta
from time import sleep

import requests
from lxml import etree
from requests.adapters import HTTPAdapter
from tqdm import tqdm
import re
from bs4 import BeautifulSoup
import requests
from database_util import database_util
from config import *
from lxml import etree
from lxml import html
from html import unescape
import time
import re
import json
# 数据采集
class data_spider:
    def __init__(self):
        self.database = database_util()
        self.headers = {
            "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36"
        }


 
    def spider_news(self):
        url = 'http://www.ahpu.edu.cn/xwzx/3391/list{}.htm'
        response = requests.get(url.format(1))
        html = etree.HTML(str(response.content,'utf-8'))
        per_count = int(html.xpath('//em[@class="per_count"]/text()')[0])
        all_count = int(html.xpath('//em[@class="all_count"]/text()')[0])
        page = (round(all_count//per_count) + 1) if (all_count%per_count!=0) else round(all_count//per_count)
        return_flag = False
        # page=15
        for i in range(1,page):
            try:
                list_url = url.format(i)
                response = requests.get(list_url)
                html = etree.HTML(str(response.content,'utf-8'))
                # 创建人列表
                creator_list = html.xpath('//table[@id="newslist"]//table//tr/td[1]/text()')
                # 新闻标题列表
                title_list = html.xpath('//table[@id="newslist"]//table//tr/td[2]/a/text()')
                # 新闻链接列表
                link_list = html.xpath('//table[@id="newslist"]//table//tr/td[2]/a/@href')
                # print(link_list)
                # 创建时间列表
                create_time_list = html.xpath('//table[@id="newslist"]//table//tr/td[3]/span/text()')
                for i in range(len(title_list)):
                    item = dict()
                    item['title'] = title_list[i]
                    # 如果数据库中已经存在,就不用继续执行了
                    result = self.database.query_news(item['title'])
                    if(result):
                        return_flag = True
                        continue
                    item['creator'] = creator_list[i]
                    item['create_time'] = create_time_list[i]
                    link = 'http://www.ahpu.edu.cn'+link_list[i]
                    if('_redirect' in link or '/_upload' in link_list[i]):
                        item['content'] = ''
                        item['link'] = link
                    elif('https' in link_list[i] or 'http' in link_list[i]):
                        item['content'] = ''
                        item['link'] = link_list[i]
                    else:
                        try:
                            item['link'] = link
                            print(link)
                            response = requests.get(link)
                            # print(response)
                            html = etree.HTML(str(response.content,'utf-8'))
                            # print(str(response.content,'utf-8'))
                            content = html.xpath('//div[@class="Article_Content"]')[0]
                            content = etree.tostring(content, method='html')
                            item['content'] = unescape(content.decode())
                        except Exception as e:
                            print(e)
                            item['link'] = link
                            item['content'] = ''
                            continue

                    # print(item)
                    self.database.save_news(item)
                if(return_flag):
                    continue
                if(i%20==0):
                    time.sleep(2)
            except Exception as e:
                print(e)
                continue
    
    
if __name__ == "__main__":
    data_spider = data_spider()
    data_spider.spider_news()
    # test()
    



    
