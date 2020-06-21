import requests
from lxml import etree
from openpyxl import Workbook
from myutils import get_header
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import random

# 爬虫处理类
# 目标网站 蘑菇租房：http://www.mgzf.com/list/qy13_
class Spider:
    # 目标网站列表页的基本链接
    baseUrl = 'http://www.mgzf.com/list/qy@position_'
    pageurl = 'http://www.mgzf.com/list/pg@page/qy@position_/?searchWord=&paraName='
    # 自定义的header
    # 爬取的页数总和
    def getPageCount(self):
        req = requests.get(self.baseUrl,headers=get_header())
        print(req.text)
        tree = etree.HTML(req.text)
        # 通过xpath提取链接
        page = tree.xpath('//div[@class="pageBox"]/div[@class="page-box"]/span/text()')
        if(len(page)>0):
            return int(page[0][1:3])
        else:
            return 0

    def buffer(self,browser):
        for i in range(50):
            time.sleep(0.3)
            browser.execute_script('window.scrollBy(0,300)', '')
    
    def getDataByBrowswer(self):
        data = []
        print('开始爬虫')
        browser = webdriver.Chrome('C://Users/Administrator/AppData/Local/Google/Chrome/Application/chromedriver.exe')
        page_link = self.pageurl.replace('@position',str(13))
        page = 1     
        for offset in range(page):
            pageUrl = page_link.replace('@page',str(offset+1))
            browser.get(pageUrl)
            time.sleep(30)
            self.buffer(browser)
            links = browser.find_elements_by_xpath('//div[@class="roomCardSmall-box"]//a')
            types = browser.find_elements_by_xpath('//div[@class="roomCardSmall-box"]//a//div[@class="text-content-middle"]//h2[1]')
            desps = browser.find_elements_by_xpath('//div[@class="roomCardSmall-box"]//a//div[@class="text-content-middle"]//h2[2]')
            positions = browser.find_elements_by_xpath('//div[@class="roomCardSmall-box"]//a//div[@class="text-content-middle"]//p')
            for i in range(len(links)):
                item = {}
                link = links[i].get_attribute('href')
                item['name'] = links[i].text
                item['type'] = types[i].text
                item['desp'] = desps[i].text
                item['position'] = positions[i].text
                browser.get(link)
                time.sleep(30)
                self.buffer(browser)
                item['pay_type'] = browser.find_element_by_xpath('//div[@class="w460 price mt10"]/div[@class="info"]/span[@class="type"]').text
                item['pay_price'] = browser.find_element_by_xpath('//div[@class="w460 price mt10"]/div[@class="info"]/span[@class="num orange"]').text
                item['pay_price_unit'] = browser.find_element_by_xpath('//div[@class="w460 price mt10"]/div[@class="info"]/span[@class="num orange"]/i').text
                item['phone'] = browser.find_element_by_xpath('//div[@class="w460 room-call"]//div[@class="phone orange"]').text
                data.append(item)
        print(data)
        browser.close()
        return data
            
    # 列表页处理函数、批量获取详情页链接地址
    def getData(self):
        data = []
        print('开始爬虫')
        # page = self.getPageCount()
        page = 1
        page_link = self.pageurl.replace('@position',str(13))
        print(page)
        for offset in range(page):
            # 拼接URL
            pageUrl = page_link.replace('@page',str(offset))
            print(pageUrl)
            # 通过requests获取数据
            response = requests.get(url=pageUrl,headers=get_header())
            print(response.text)
            # html=response.content
            # html_doc=str(html,'utf-8')
            # 通过etree解析文档
            tree = etree.HTML(response.text)
            # 通过xpath提取链接
            links = tree.xpath('//div[@class="roomCardSmall-box"]//a/@href')
            print(links)
            names = tree.xpath('//div[@class="roomCardSmall-box"]//a/@title')
            types = tree.xpath('//div[@class="roomCardSmall-box"]//a//div[@class="text-content-middle"]//h2[1]/text()')
            desps = tree.xpath('//div[@class="roomCardSmall-box"]//a//div[@class="text-content-middle"]//h2[2]/text()')
            positions = tree.xpath('//div[@class="roomCardSmall-box"]//a//div[@class="text-content-middle"]//p/text()')
            for i in range(len(links)):
                item = {}
                item['name'] = names[i]
                item['type'] = types[i]
                item['desp'] = desps[i]
                item['position'] = positions[i]
                link = links[i]
                req = requests.get(link,headers=get_header())
                html_doc = str(req.content,'utf-8')
                print(html_doc)
                tree = etree.HTML(html_doc)
                item['pay_type'] = tree.xpath('//div[@class="w460 price mt10"]/div[@class="info"]/span[@class="type"]/text()')[0]
                item['pay_price'] = tree.xpath('//div[@class="w460 price mt10"]/div[@class="info"]/span[@class="num orange"]/text()')[0]
                item['pay_price_unit'] = tree.xpath('//div[@class="w460 price mt10"]/div[@class="info"]/span[@class="num orange"]/i/text()')[0]
                item['phone'] = tree.xpath('//div[@class="w460 room-call"]//div[@class="phone orange"]/text()')[0]
                data.append(item)
                time.sleep(random.random()*8)
            time.sleep(random.random()*8)
        return data
        

    # # 保存数据到excel文件
    def saveToCsv(self,data):
        wb = Workbook()
        ws = wb.active
        ws.append(['标题', '类型', '描述', '地理位置', '房租支付方式', '房租', '房租单位','手机号'])
        for item in data:
            line = [item['name'], item['type'],item['desp'],item['position'],item['pay_type'],item['pay_price'],item['pay_price_unit'],item['phone']]
            ws.append(line)
            wb.save('蘑菇租房_上海.xlsx')
    
    # # 开始爬虫
    def startSpider(self):
        data = self.getData()
        self.saveToCsv(data)
        # self.getDataByBrowswer()

if __name__ == "__main__":
    spider = Spider()
    spider.startSpider()