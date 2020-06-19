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
  
    # 采集百度贴吧的数据
    def spider_tieba(self):
        # 目标地址
        url = 'https://tieba.baidu.com/f?kw=%E5%AE%89%E5%BE%BD%E5%B7%A5%E7%A8%8B%E5%A4%A7%E5%AD%A6&ie=utf-8'
        self.spider_tieba_list(url)
    
     
    def GetMiddleStr(self,content,startStr,endStr):
        patternStr = r'%s(.+?)%s'%(startStr,endStr)
        p = re.compile(patternStr,re.IGNORECASE)
        m= re.match(p,content)
        if m:
            return m.group(1)

    # 时间转换
    def get_time_convert(self,timeStr):
        if(re.match('^\d{1,2}:\d{1,2}$',timeStr) != None):
            day = time.strftime('%Y-%m-%d',time.localtime(time.time()))
            timeStr = day+' '+timeStr+':00'
        elif(re.match('^\d{4}-\d{1,2}$',timeStr) != None):
            day = time.strftime('%d',time.localtime(time.time()))
            timeStr = timeStr+'-'+day+' 00:00:00'
        elif(re.match('^\d{1,2}-\d{1,2}$',timeStr) != None):
            day = time.strftime('%Y',time.localtime(time.time()))
            timeStr = day+'-'+timeStr+' 00:00:00'
        return timeStr


    # 过滤表情
    def filter_emoji(self,desstr,restr=''):  
        try:  
            co = re.compile(u'[\U00010000-\U0010ffff]')  
        except re.error:  
            co = re.compile(u'[\uD800-\uDBFF][\uDC00-\uDFFF]')  
        return co.sub(restr, desstr)

    # 采集百度贴吧列表数据
    def spider_tieba_list(self,url):
        print(url)
        response = requests.get(url,headers=self.headers)
        try:
            response_txt = str(response.content,'utf-8')
        except Exception as e:
            response_txt = str(response.content,'gbk')
        # response_txt = str(response.content,'utf-8')
        bs64_str = re.findall('<code class="pagelet_html" id="pagelet_html_frs-list/pagelet/thread_list" style="display:none;">[.\n\S\s]*?</code>', response_txt)
        
        bs64_str = ''.join(bs64_str).replace('<code class="pagelet_html" id="pagelet_html_frs-list/pagelet/thread_list" style="display:none;"><!--','')
        bs64_str = bs64_str.replace('--></code>','')
        print(bs64_str)
        html = etree.HTML(bs64_str)
        # print(thread_list)
        # 标题列表
        title_list = html.xpath('//div[@class="threadlist_title pull_left j_th_tit "]/a[1]/@title')
        # print(title_list)
        # 链接列表
        link_list = html.xpath('//div[@class="threadlist_title pull_left j_th_tit "]/a[1]/@href')
        # 发帖人
        creator_list = html.xpath('//div[@class="threadlist_author pull_right"]/span[@class="tb_icon_author "]/@title')
        # 发帖时间
        create_time_list = html.xpath('//div[@class="threadlist_author pull_right"]/span[@class="pull-right is_show_create_time"]/text()')
        creator_list = creator_list[1:]
        create_time_list = create_time_list[1:]
        print(create_time_list)
        print(create_time_list[1])
        for i in range(len(title_list)):
            item = dict()
            item['create_time'] = create_time_list[i]
            if(item['create_time'] == '广告'):
                continue
            item['create_time'] = self.get_time_convert(item['create_time'])
            print(item['create_time'])
            item['title'] = self.filter_emoji(title_list[i])
            item['link'] = 'https://tieba.baidu.com'+link_list[i]
            item['creator'] = self.filter_emoji(creator_list[i]).replace('主题作者: ','')
            item['content'] = self.filter_emoji(item['title'])
            print(item['creator'])
            # 保存帖子数据
            result = self.database.query_tieba(item['link'])
            if(not result):
                self.database.save_tieba(item)
            self.spider_tieba_detail(item['link'])    
        # 定时采集任务则只采集最新的一页数据
        # 如果有下一页继续采集下一页
        # nex_page = html.xpath('//a[@class="next pagination-item "]/@href')
        # if(len(nex_page)>0):
        #     next_url = 'https:'+nex_page[0]
        #     self.spider_tieba_list(next_url)

    # 采集帖子详情页
    def spider_tieba_detail(self,link):
        response = requests.get(link,headers=self.headers)
        html = etree.HTML(response.text)
        # html = etree.HTML(str(response.content,'utf-8'))
        author_list = html.xpath('//div[@id="j_p_postlist"]/div/div[@class="d_author"]/ul/li[@class="d_name"]/a/text()')
        content_list = html.xpath('//div[@class="d_post_content j_d_post_content  clearfix"]/text()')
        id_list = html.xpath('//div[@class="d_post_content j_d_post_content  clearfix"]/@id')       
    
        for j in range(len(id_list)):
            reply_item = dict()
            reply_item['content'] = self.filter_emoji(content_list[j])
            reply_item['creator'] = self.filter_emoji(author_list[j])
            # reply_item['create_time'] = reply_create_time_list[j]
            reply_item['link'] = link            
            reply_item['reply_id'] = id_list[j]
            reply_result = self.database.query_tieba_reply(reply_item['reply_id'])
            if(not reply_result):
                self.database.save_tieba_reply(reply_item)
        nex_page = html.xpath('//ul[@class="l_posts_num"]/text()/li[@class="l_pager pager_theme_5 pb_list_pager"]/@href')
        nex_page_text = html.xpath('//ul[@class="l_posts_num"]/text()/li[@class="l_pager pager_theme_5 pb_list_pager"]/text()')
        if(len(nex_page)>0):
            for t in range(len(nex_page_text)):
                if(nex_page_text[t]=='下一页'):
                    next_url = 'https://tieba.baidu.com'+nex_page[t]
                    self.spider_tieba_detail(next_url)

        
    
    
if __name__ == "__main__":
    data_spider = data_spider()
    data_spider.spider_tieba()
    



    
