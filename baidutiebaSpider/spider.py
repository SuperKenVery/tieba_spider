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
from urllib import parse
import pdb


from requests.adapters import HTTPAdapter, Retry

s = requests.Session()

retries = Retry(total=10,
                backoff_factor=0.1,
                status_forcelist=[ 500, 502, 503, 504 ])

s.mount('http://', HTTPAdapter(max_retries=retries))
s.mount('https://', HTTPAdapter(max_retries=retries))

class User:
    cache={}
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux aarch64; rv:109.0) Gecko/20100101 Firefox/115.0",
    }
    @classmethod
    def get(cls,uid):
        if uid in cls.cache:
            return cls.cache[uid]
        else:
            return cls(uid)
    def __init__(self,uid):
        #uid: e.g. tb.1.254e4e87.UpdwCNdazsrBZxnmDeqthA
        self.uid=uid
        infourl = f'https://tieba.baidu.com/home/get/panel?ie=utf-8&id={self.uid}'
        info = json.loads(s.get(infourl, headers=self.headers).text)
        data=info['data']
        self.sex = data.get('sex','unknown')
        self.name=data.get('name_show','unknown')
        self.nickname=data.get('show_nickname','unknown')

# 数据采集
class DataSpider:
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/109.0",
    }
    def __init__(self):
        self.database = database_util()


    # 采集百度贴吧的数据
    def spider_tieba(self):
        # 目标地址
        url = 'https://tieba.baidu.com/f?kw=%E6%A1%8C%E9%A5%BA&ie=utf-8&tab=good'
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
        response = s.get(url,headers=self.headers)
        try:
            response_txt = str(response.content,'utf-8')
        except Exception as e:
            response_txt = str(response.content,'gbk')
        # response_txt = str(response.content,'utf-8')
        bs64_str = re.findall('<code class="pagelet_html" id="pagelet_html_frs-list/pagelet/thread_list" style="display:none;">[.\n\S\s]*?</code>', response_txt)

        bs64_str = ''.join(bs64_str).replace('<code class="pagelet_html" id="pagelet_html_frs-list/pagelet/thread_list" style="display:none;"><!--','')
        bs64_str = bs64_str.replace('--></code>','')
        html = etree.HTML(bs64_str)
        if not html:
            print("IP Blocked")
            print(response_txt)

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
        print("Collecting the list")
        for i in range(len(title_list)):
            item = dict()
            item['create_time'] = create_time_list[i]
            if(item['create_time'] == '广告'):
                continue
            item['create_time'] = self.get_time_convert(item['create_time'])
            item['title'] = self.filter_emoji(title_list[i])
            item['link'] = 'https://tieba.baidu.com'+link_list[i]
            item['creator'] = self.filter_emoji(creator_list[i]).replace('主题作者: ','')
            item['content'] = self.filter_emoji(item['title'])
            print(f"Post {item['title']} by {item['creator']}")
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
        response = s.get(link,headers=self.headers)
        html = etree.HTML(response.text)
        # html = etree.HTML(str(response.content,'utf-8'))
        author_list = html.xpath('//div[@id="j_p_postlist"]/div/div[@class="d_author"]/ul/li[@class="d_name"]/a/text()')
        content_list = html.xpath('//div[@class="d_post_content j_d_post_content "]/text()')
        id_list = html.xpath('//div[@class="d_post_content j_d_post_content "]/@id')
        pid_list=html.xpath('//div[@class="l_post l_post_bright j_l_post clearfix  "]/@data-pid')
        author_property_list = html.xpath('//div[@id="j_p_postlist"]/div/div[@class="d_author"]/ul/li[@class="d_name"]/a/@data-field')
        location_list = html.xpath('//div[@class="post-tail-wrap"]/span[1]/text()')

        print("Collecting replies")
        for j in range(len(id_list)):
            reply_item = dict()
            reply_item['reply_id'] = id_list[j]
            reply_result = self.database.query_tieba_reply(reply_item['reply_id'])
            if (not reply_result):
                reply_item['content'] = self.filter_emoji(content_list[j])
                reply_item['creator'] = self.filter_emoji(author_list[j])
                # reply_item['create_time'] = reply_create_time_list[j]
                reply_item['link'] = link

                creator_info=json.loads(author_property_list[j])
                uid=creator_info['id']
                user=User.get(uid=uid)
                reply_item['sex']=user.sex

                reply_item['location']=location_list[j]

                print(f"Reply by {reply_item['creator']} sex {user.sex} at {reply_item['location']}")

                self.database.save_tieba_reply(reply_item)
            else:
                print(f"Reply {reply_item['reply_id']} already saved")

            # lzl
            pid=pid_list[j]
            splitted=parse.urlsplit(link)
            path=splitted.path
            tid=path.split('/')[2]
            self.get_lzl(tid,pid)



        nex_page = html.xpath('//ul[@class="l_posts_num"]/text()/li[@class="l_pager pager_theme_5 pb_list_pager"]/@href')
        nex_page_text = html.xpath('//ul[@class="l_posts_num"]/text()/li[@class="l_pager pager_theme_5 pb_list_pager"]/text()')
        if(len(nex_page)>0):
            for t in range(len(nex_page_text)):
                if(nex_page_text[t]=='下一页'):
                    next_url = 'https://tieba.baidu.com'+nex_page[t]
                    self.spider_tieba_detail(next_url)


    def get_lzl(self,tid:str,pid:str):
        print(f"Getting lzl of tid {tid} pid {pid}")
        page_num=1
        in_range=True
        while in_range:
            url = f"https://tieba.baidu.com/p/comment?tid={tid}&pid={pid}&pn={page_num}"
            response=s.get(
                url,
                headers=self.headers
            )
            html=etree.HTML(response.text)
            pagers=html.xpath('//a')
            if len(pagers)<=1:
                in_range=False
                print(f"No lzl, request at {url}, response is {response.text}")
                break

            print(f"...Getting page {page_num}")
            reply_infos_raw=html.xpath('//li/@data-field')
            reply_infos=[json.loads(i) for i in reply_infos_raw]
            spids=[i['spid'] for i in reply_infos[:-1]]

            replies_authors=html.xpath('//li/div/a/@data-field')
            replies=html.xpath('//li/div/span/text()')

            authors=[json.loads(i) for i in replies_authors]
            uids=[x['id'] for x in authors]
            users=[User.get(i) for i in uids]

            for i in range(len(spids)):
                data={
                    'reply_id':spids[i],
                    'creator':self.filter_emoji(users[i].name),
                    'content':self.filter_emoji(replies[i]),
                    'link':'lzl, no link',
                    'sex':users[i].sex,
                    'location':'lzl, no location',
                }
                # pdb.set_trace()
                if not self.database.query_tieba_reply(data['reply_id']):
                    self.database.save_tieba_reply(data)

            print(f"Processed {len(spids)} lzls")

            page_num+=1



if __name__ == "__main__":
    ds = DataSpider()
    urls='''
https://tieba.baidu.com/p/8519789465
https://tieba.baidu.com/p/8317872453
https://tieba.baidu.com/p/8520909875
https://tieba.baidu.com/p/8323958054
https://tieba.baidu.com/p/8505129223
https://tieba.baidu.com/p/8500159354
https://tieba.baidu.com/p/8465333453
https://tieba.baidu.com/p/8470720345
https://tieba.baidu.com/p/8448957790
https://tieba.baidu.com/p/8441462991
https://tieba.baidu.com/p/8519152802
https://tieba.baidu.com/p/8461950758
https://tieba.baidu.com/p/8299057234
https://tieba.baidu.com/p/8209859721
https://tieba.baidu.com/p/8514602303
https://tieba.baidu.com/p/8519389912
https://tieba.baidu.com/p/8513274948
https://tieba.baidu.com/p/8482618402

'''.strip().split('\n')
    for u in urls:
        print(f"Getting {u}")
        ds.spider_tieba_detail(link=u)





