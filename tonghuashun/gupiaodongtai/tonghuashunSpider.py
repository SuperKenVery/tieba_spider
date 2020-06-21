# -*- coding: UTF-8 -*-
__author__ = 'Chengrongkai'

import requests
from lxml import etree
import time
import os
import xlrd
import xlwt
import xlutils.copy
from sendEmail import EmailService
from myutils import user_agent
from setting import mailserver,username_send,password
import time
from tkinter import END
import random
import json

class Spider:
    cookie = ''

    cookie_nologin = 'Hm_lvt_78c58f01938e4d85eaf619eae71b4ed1=1576984235; __guid=89649499.3432241371182561000.1576984249761.5198; monitor_count=1; v=AiBfyMkramfKiNZj61uhKmcA8SXlKQTzpg1Y95ox7DvOlc4ZQjnUg_YdKIvp'

    login_status = False
    events_list = []

    def __init__(self,app,username_recv,login):
        self.emailService = EmailService(username_send,password,mailserver,username_recv)
        self.app = app
        if(login):
            self.getCookie()
            if(self.cookie != ''):
                self.login_status = True
            else:
                self.login_status = False  
                self.cookie =  self.cookie_nologin
        else:
            self.login_status = False  
            self.cookie =  self.cookie_nologin
        i = 1
        info = '开始执行扫描任务:'+time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time()))
        self.app.text.insert('end',info+'\n')
        self.app.text.see(END)
        while(True):
            if(self.login_status):
                self.getSelfInfo()
            else: 
                self.getDetailPageInfo()
            info = '第'+str(i)+'次扫描执行完毕:'+time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time()))
            print(info)
            self.app.text.insert('end',info+'\n')
            self.app.text.see(END)
            i = i+1
            time.sleep(60)
    
    # 获取并解析详情页面的数据
    def getDetailPageInfo(self):
        # 不同市场的链接
        type_url='http://q.10jqka.com.cn/index/index/board/all/field/zdf/order/desc/page/'
        # 各个分类的开始页
        # start_urls = [hs,ss,zxb,cyb]
        # for type_url in start_urls:
        page = 1
        headers = {
            'User-Agent': user_agent,
            'Cookie': self.cookie    
        }
        start_url = type_url+str(page)+'/ajax/1/'
        print(start_url)
        req = requests.get(url=start_url,headers=headers,timeout=5)
        # print(req.text)
        root3 = etree.HTML(req.text)
        # 获取总页数
        p=root3.xpath('//*[@id="m-page"]/span/text()')
        print(p)
        # if(len(p) == 0):
        #     # print(start_url)
        #     continue
        p = p[0]
        page_all=p[2:]
        # print(page_all)
        # page_all= int(page_all) if (int(page_all)<10) else 10
        # 遍历每一页
        for page in range(int(page_all)):
            start_url = type_url+str(page)+'/ajax/1/'
            print(start_url)
            self.get_list(start_url)
            # 休眠一秒
            time.sleep(random.uniform(30,45))
        # 休眠两秒
        # time.sleep(60)

    # 获取列表页         
    def get_list(self,start_url):
        headers = {
            'User-Agent': user_agent,
            'Cookie': self.cookie   
        }
        req = requests.get(url=start_url,headers=headers,timeout=5)
        print(req.text)
        root3 = etree.HTML(req.text)
        no_list=root3.xpath('/html/body/table/tbody/tr/td[1]/text()')
        # print(no_list)
        code_no=root3.xpath('/html/body/table/tbody/tr/td[2]/a/text()')
        # print(code_no)
        code_name=root3.xpath('/html/body/table/tbody/tr/td[3]/a/text()')
        # print(code_name)
        code_url=root3.xpath('/html/body/table/tbody/tr/td[2]/a/@href')       
        # print(code_url)
        for i in range(len(code_url)):
            info = {
                'code':code_no[i],
                'code_name':code_name[i],
                'code_url':code_url[i]
            }
            self.get_events(info)       

    # 寻找事件
    def get_events(self,info):
        print(info)
        base_url = info['code_url'].replace('stockpage.10jqka.com.cn','basic.10jqka.com.cn')
        event_url = base_url+'event.html'
        headers = {
        'User-Agent': user_agent,
        'Cookie': self.cookie,    
        # 'Host':'basic.10jqka.com.cn',
        # 'Referer':event_url
        }
        event_html = requests.get(url=event_url,headers=headers,timeout=15)
        html=event_html.content
        html_doc=str(html,'gbk')
        event_req = etree.HTML(html_doc)
        today_event_type = event_req.xpath('//table[@id="tableToday"]//tr[1]/td/strong/text()')
        today_event = event_req.xpath('//table[@id="tableToday"]//tr[1]/td/span/text()')
        events = []
        msg = '正在扫描股票:'+info['code_name']
        self.app.text.insert('end',msg+'\n')
        self.app.text.see(END)
        for i in range(len(today_event)):
            if(not today_event[i].isspace() ):
                if('新增概念：' == today_event_type[i].strip()):
                    events.append(today_event[i].strip())
                    self.compareNewsInfo(info,today_event[i].strip())


    # 比较新概念事件
    def compareNewsInfo(self,info,event):
        # 从excel里读取已存储的事件信息
        file_name = 'event_'+info['code_name']+'_'+time.strftime('%Y-%m-%d',time.localtime(time.time()))+'.xls'
        exist = False
        # 文件已存在
        if(os.path.exists(os.path.abspath(file_name))):
            workbook = xlrd.open_workbook(file_name)
            sheet1 = workbook.sheet_by_index(0)      #用索引取第1个sheet
            nrows = sheet1.nrows                #读取行数
            for i in range(nrows):         #循环逐行打印
                if i==0:     #跳过第一行
                    continue
                event_old = sheet1.row_values(i)[:1]
                if(event_old[0] == event):
                    exist = True
                    break
            if(not exist):
                ws = xlutils.copy.copy(workbook) #复制之前表里存在的数据
                table=ws.get_sheet(0)
                table.write(nrows, 0, event)  #最后一行追加数据
                ws.save(file_name)  #保存的有旧数据和新数据
        else:
            workbook = xlwt.Workbook(encoding='utf-8')       #新建工作簿
            sheet1 = workbook.add_sheet("新概念事件")          #新建sheet   
            sheet1.write(0,0,"事件")      #第1行第1列数据
            sheet1.write(1,0,event)  
            workbook.save(os.path.abspath(file_name))   #保存
        if(not exist):
            # 发送邮箱提醒
            msg = '股票名称:'+info['code_name']+';新增概念:'+event+';详情地址:'+info['code_url']
            self.app.text.insert('end',msg+'\n')
            self.app.text.see(END)
            self.emailService.sendMessage(msg)
            msg = '提醒发送成功:'+time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            self.app.text.insert('end',msg+'\n')
            self.app.text.see(END)

    # 获取登录的cookie
    def getCookie(self):
        path = 'cookies'+'_'+time.strftime('%Y-%m-%d',time.localtime(time.time()))+'.txt'
        with open(path, "r") as fp:
                cookies = json.load(fp)
                for item in cookies:
                    # cookie.pop('domain')  # 如果报domain无效的错误
                    self.cookie = self.cookie+item["name"] + "=" + item["value"]+'; '
    # 获取自选股票信息
    def getSelfInfo(self):
        url = 'http://pop.10jqka.com.cn/getselfstockinfo.php'
        headers = {
        'User-Agent': user_agent,
        'Cookie': self.cookie,    
        # 'Host':'basic.10jqka.com.cn',
        # 'Referer':event_url
        }
        rep = requests.get(url=url,headers=headers)
        js = json.loads(rep.text)
        for data in js:
            code = data['code']
            if(code.isdigit()):
                self.get_self_events(code)

    def get_self_events(self,code):
        base_url = 'http://basic.10jqka.com.cn/'+str(code)+'/'
        event_url = base_url+'event.html'
        headers = {
        'User-Agent': user_agent,
        'Cookie': self.cookie,    
        # 'Host':'basic.10jqka.com.cn',
        # 'Referer':event_url
        }
        event_html = requests.get(url=event_url,headers=headers,timeout=15)
        html=event_html.content
        html_doc=str(html,'gbk')
        event_req = etree.HTML(html_doc)
        today_event_type = event_req.xpath('//table[@id="tableToday"]//tr[1]/td/strong/text()')
        today_event = event_req.xpath('//table[@id="tableToday"]//tr[1]/td/span/text()')
        events = []
        name = event_req.xpath('//div[@class="code fl"]/div/h1/text()')
        if(len(name) == 0):
            return
        msg = '正在扫描股票:'+name[0].strip()
        info = {
            'code':code,
            'code_name':name
        }
        self.app.text.insert('end',msg+'\n')
        self.app.text.see(END)
        for i in range(len(today_event)):
            if(not today_event[i].isspace() ):
                if('新增概念：' == today_event_type[i].strip()):
                    events.append(today_event[i].strip())
                    self.compareNewsInfo(info,today_event[i].strip())
    
# if __name__ == "__main__":
#     spider = Spider()
#     spider.getDetailPageInfo()

