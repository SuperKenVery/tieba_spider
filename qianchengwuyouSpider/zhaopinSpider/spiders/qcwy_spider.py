# -*- coding: UTF-8 -*-
__author__ = 'Chengrongkai'

import scrapy
import requests
from zhaopinSpider.myutils import get_header
import json
from urllib.parse import urlencode
from zhaopinSpider.items import ZhaopinspiderItem
from lxml import etree
from zhaopinSpider.config import cityList,keyword,pageLimit,startPage
import time

class ZhaopinSpider(scrapy.Spider):
    name = 'qcwy_spider'
    # 允许的域名
    allowed_domains = ["51job.com"]
    baseurl = 'https://search.51job.com/list/'
    city_req = ''
    city_code = ''
    queryKey = ''


    def get_city_list(self):
        url = 'https://js.51jobcdn.com/in/js/2016/layer/area_array_c.js'
        req = requests.get(url, headers=get_header()).text
        self.city_req = req
    
    # 获取城市的code集合
    def _get_city_code(self,city):
        if(self.city_req == ''):
            self.get_city_list()
        a = self.city_req.find(city)
        return self.city_req[a - 9:a - 3]
    
    # 自定义开始的请求
    def start_requests(self):
        print('开始爬取:{}'.format(time.strftime('%Y.%m.%d',time.localtime(time.time()))))
        # 获取城市code
        for city in cityList:
            if(city == '全国'):
                self.city_code = 000000
            else:
                self.city_code = self._get_city_code(city)
            # 拼接搜索页的请求
            self.queryKey = keyword
            if(self.queryKey == ''):
                # 表示查询所有
                self.queryKey = '%2520'
            url = self.baseurl + '{},000000,0000,00,9,99,{},2,1.html'.format(self.city_code, self.queryKey)
            # yield scrapy.Request(url=url,headers=get_header(),encoding='gbk',callback=self.parse)
            req = requests.get(url=url, headers=get_header())
            req.encoding = 'gbk'
            response = etree.HTML(req.text)
            max_page = response.xpath('//*[@id="resultList"]/div[2]/div[5]/text()')[2][3:]
            print(max_page)
            start = 1
            end = int(max_page)+1
            # 根据设置的分页参数爬取
            if(int(startPage)+int(pageLimit) <= int(max_page)):
                start = int(startPage)
                end = int(startPage)+int(pageLimit)+1
            print(self.city_code,self.queryKey)
            for page in range(start, end):
                # 拼接列表页的请求
                page_url = self.baseurl + '{},000000,0000,00,9,99,{},2,{}.html'.format(self.city_code, self.queryKey, page)
                # 异步执行列表页的请求
                print(page_url)
                yield scrapy.Request(url=page_url,encoding='gbk',headers=get_header(),callback=self.parseList)
        print('爬取完成:{}'.format(time.strftime('%Y.%m.%d',time.localtime(time.time()))))
            

    # def parse(self,response):
    #     # 获取最大的页数
    #     print(response.text)
    #     max_page = response.xpath('//*[@id="resultList"]/div[2]/div[5]/text()').extract()[2]
    #     max_page = "".join(max_page.split())[1:]
    #     max_page = (int(max_page) if(int(max_page)<1) else 1)
    #     print(self.city_code,self.queryKey)
    #     for page in range(1, int(max_page) + 1):
    #         # 拼接列表页的请求
    #         page_url = self.baseurl + '{},000000,0000,00,9,99,{},2,{}.html'.format(self.city_code, self.queryKey, page)
    #         # 异步执行列表页的请求
    #         print(page_url)
    #         yield scrapy.Request(url=page_url,encoding='gbk',headers=get_header(),callback=self.parseList)

    # 解析列表页   
    def parseList(self,response):
        print(response)
        for i in range(4, 54):
            try:
                item = ZhaopinspiderItem()
                # 通过xpath获取数据
                jobName = response.xpath('//*[@id="resultList"]/div[{}]/p/span/a/@title'.format(i)).extract()
                if jobName[0] == None:
                    break
                item['jobName'] = jobName[0]
                companyName = response.xpath('//*[@id="resultList"]/div[{}]/span[1]/a/text()'.format(i)).extract()
                item['companyName'] = companyName[0] if(companyName[0] != None) else ''
                positionURL = response.xpath('//*[@id="resultList"]/div[{}]/p/span/a/@href'.format(i)).extract()
                item['positionURL'] = positionURL[0] if(positionURL[0] != None) else ''
                companyDisplay = response.xpath('//*[@id="resultList"]/div[{}]/span[2]/text()'.format(i)).extract()
                item['companyDisplay'] = companyDisplay[0] if(companyDisplay[0] != None) else ''
                salary = response.xpath('//*[@id="resultList"]/div[{}]/span[3]/text()'.format(i)).extract()
                item['salary'] = salary[0] if(salary[0] != None) else ''
                updateDate = response.xpath('//*[@id="resultList"]/div[{}]/span[4]/text()'.format(i)).extract()
                item['updateDate'] = updateDate[0] if(updateDate[0] != None) else ''
                if(item['positionURL'] == '' or item['positionURL'].find('jobs.51job.com') == -1):
                    continue
                # 请求详情页数据处理
                yield scrapy.Request(url=item['positionURL'],headers=get_header(),callback=self.parseDetail,meta={'item':item})
            except:
                continue
    
    # 解析详情页
    def parseDetail(self,response):
        # 接收传递的item
        item = response.meta['item']
        print(item)
        # 获取详细的工作描述
        item['jobDetail'] = ''.join(response.xpath('//*[@class="bmsg job_msg inbox"]//p/text()').extract())
        if item['jobDetail'].isspace():
            item['jobDetail'] = ''.join(response.xpath('//*[@class="bmsg job_msg inbox"]/text()').extract())
        item['jobDetail'] = "".join(item['jobDetail'].split())
        # 获取详细的公司描述
        item['companyDesc'] = ''.join(response.xpath('//*[@class="tmsg inbox"]/text()').extract())
        if item['companyDesc'].isspace():
            item['companyDesc'] = ''.join(response.xpath('//*[@class="tmsg inbox"]//*/text()').extract())
        item['companyDesc'] = "".join(item['companyDesc'].split())
        # 获取其他的一些详细信息
        # 地理位置
        item['position'] = response.xpath('//div[@class="tHeader tHjob"]/div/div/p[@class="msg ltype"]/text()').extract()[0]
        item['position'] = "".join(item['position'].split())
        # 工作经验
        item['workingExp'] = response.xpath('//div[@class="tHeader tHjob"]/div/div/p[@class="msg ltype"]/text()').extract()[1]
        item['workingExp'] = "".join(item['workingExp'].split())
        # 学历要求
        item['eduLevel'] = response.xpath('//div[@class="tHeader tHjob"]/div/div/p[@class="msg ltype"]/text()').extract()[2]
        item['eduLevel'] = "".join(item['eduLevel'].split())
        # 招聘人数
        item['peopleNum'] = response.xpath('//div[@class="tHeader tHjob"]/div/div/p[@class="msg ltype"]/text()').extract()[3]
        item['peopleNum'] = "".join(item['peopleNum'].split())
        # 福利标签
        tag = response.xpath('//div[@class="jtag"]/div/span/text()').extract()
        item['welfare'] = ','.join(tag)
        # 公司主页
        companyUrl = response.xpath('//div[@class="tCompany_sidebar"]//div[@class="com_msg"]/a/@href').extract()
        item['companyUrl'] = companyUrl[0] if(companyUrl[0] != None) else ''
        # 公司性质
        item['companyType'] = response.xpath('//div[@class="tCompany_sidebar"]//div[@class="com_tag"]/p/@title').extract()[0]
        # 公司规模
        item['companySize'] = response.xpath('//div[@class="tCompany_sidebar"]//div[@class="com_tag"]/p/@title').extract()[1]
        # 公司所在行业
        item['companyIndustry'] = response.xpath('//div[@class="tCompany_sidebar"]//div[@class="com_tag"]/p/@title').extract()[2]

        print(item)
        yield item

    
    


        



