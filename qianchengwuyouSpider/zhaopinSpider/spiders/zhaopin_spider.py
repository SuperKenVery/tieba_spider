# -*- coding: UTF-8 -*-
__author__ = 'Chengrongkai'

import scrapy
import requests
from zhaopinSpider.myutils import get_header
import json
from urllib.parse import urlencode
from zhaopinSpider.items import ZhaopinspiderItem
from lxml import etree
import zhaopinSpider.config as config

class ZhaopinSpider(scrapy.Spider):
    name = 'zhaopin_spider'
    # 允许的域名
    allowed_domains = ["zhaopin.com"]
    # 开始页
    start_url = 'https://fe-api.zhaopin.com/c/i/sou?'
    # 开始页集合
    # start_urls = [start_url]
    # 爬取的页数限制
    page = 15
    

    def start_requests(self):
        for page in range(self.page):
            params = {
                "start": 90*page,
                "pageSize": 90,
                "workExperience": -1,
                "education": -1,
                "companyType": -1,
                "employmentType": -1,
                "jobWelfareTag": -1,
                "kt": 3,
                "salary": '0, 0',
                'userCode':654124150
            }
            # 拼接链接
            url = self.start_url+urlencode(params, encoding='GBK')
            print(url)
            # 异步请求
            yield scrapy.Request(url=url,headers=get_header(),callback=self.parse)

    def parse(self,response):
        # 获取json数据
        print(response)
        js = json.loads(response.body)  
        data = js['data']['results']
        print(data)
        if len(data) != 0:
            for job in data:
                jobd = ZhaopinspiderItem()
                jobd['id'] = job.get('number')
                jobd['jobName'] = job.get('jobName')
                jobd['positionURL'] = job.get('positionURL')
                company = job.get('company')
                jobd['companyName'] = company.get('name')
                jobd['companyNumber'] = company.get('number')
                jobd['companyType'] = company.get('type').get('name')
                jobd['companySize'] = company.get('size').get('name')
                jobd['companyUrl'] = company.get('url')
                jobd['companyDisplay'] = job.get('city').get('display')
                jobd['salary'] = job.get('salary')
                jobd['eduLevel'] = job.get('eduLevel').get('name')
                try:
                    jobd['workingExp'] = job.get('workingExp').get('name')
                except:
                    jobd['workingExp'] = '经验不限'
                jobd['emplType'] = job.get('emplType')
                jobd['welfare'] = '、'.join(job.get('welfare')) or '无'
                jobd['timeState'] = job.get('timeState')
                jobd['updateDate'] = job.get('updateDate')
                header = get_header()
                header['referer'] = job.get('positionURL')
                header['upgrade-insecure-requests'] = '1'
                header['cookie'] = config.ZHILIAN_COOKIE
                # req1 = requests.get(job.get('positionURL'), headers=header)
                # req1.encoding = 'utf-8'
                # html = etree.HTML(req1.text)
                # detail = ''.join(html.xpath('//*[@class="describtion__detail-content"]//*/text()'))
                # if not detail:
                #     detail = ''.join(html.xpath('//*[@class="describtion__detail-content"]/text()'))
                # # print(detail)
                # jobd['jobDetail'] = detail.strip()
                yield jobd


        



