# -*- coding: utf-8 -*-
import scrapy
import json
from jsonpath  import jsonpath
from jingdongSpider.items import  Product
# from scrapy_redis.spiders import RedisSpider
import pickle
class JdProductSpider(scrapy.Spider):
    name = 'product'
    allowed_domains = ['jd.com','3.cn']
    start_urls = ['https://list.jd.com/list.html?cat=9987,653,655&page={}','https://list.jd.com/list.html?cat=670,671,2694&page={}'
    ,'https://list.jd.com/list.html?cat=670,671,672&page={}']
    # 最多爬取三十页
    max_page = 130
    type_dict =['手机','平板电脑','笔记本电脑']
   
    def start_requests(self):
        for i in range(len(self.start_urls)):
            url = self.start_urls[i].format(1)
            yield scrapy.Request(url=url,callback=self.parse,meta={'product_type':i})

    def parse(self,response):
        page = response.xpath('//span[@class="p-skip"]/em/b/text()').extract_first()
        product_type = response.meta['product_type']
        if(int(page)>self.max_page):
            page = self.max_page
        else:
            page = int(page)
        print(page)
        for i in range(page):
            url = self.start_urls[product_type].format(i+1)
            yield scrapy.Request(url,callback=self.parse_list,meta={'product_type':product_type})

    def parse_list(self, response):
        product_type = response.meta['product_type']
        #解析列表页，提取商品的skuid
        sku_ids=response.xpath('//div[contains(@class,"j-sku-item")]/@data-sku').extract()
        for sku_id in sku_ids:
            #创建Product,用于保存商品信息
            #构建商品基本信息的请求
            product_base_url='https://item.jd.com/{}.html'.format(sku_id)
            # 处理安卓手机    
            yield  scrapy.Request(product_base_url,callback=self.parse_detail,meta={'product_type':product_type})


    def parse_detail(self,response):
        item=Product()
        item['product_type'] = self.type_dict[response.meta['product_type']]
        # 商品类型
        # 品牌
        item['brand'] = response.xpath('//ul[@id="parameter-brand"]/li/@title').extract_first()
        # 商品名称
        contents = response.xpath('//ul[@class="parameter2 p-parameter-list"]/li/text()').extract()
        item['classification'] = '无'
        item['cpu'] = '无'
        item['file_save'] = '无'
        item['screen_size'] = '无'
        item['system'] = '无'
        item['color'] = '无'
        for content in contents:
            if('商品名称' in content):
                item['name'] = content[5:]
            elif('商品编号' in content):
                item['code'] = content[5:]
            elif('商品毛重' in content):
                item['weight'] = content[5:]
            elif('分类：' in content):
                item['classification'] = content[3:]

            if('内存容量：' in content):
                item['file_save'] = content[5:]
            elif('机身存储：' in content):
                item['file_save'] = content[5:]
            elif('存储容量：' in content):
                item['file_save'] = content[5:]
                

            if('处理器：' in content):
                item['cpu'] = content[4:]
            elif('CPU型号：' in content):
                item['cpu'] = content[6:]
            if('主屏幕尺寸（英寸）：' in content):
                item['screen_size'] = content[10:]
            elif('屏幕尺寸：' in content):
                item['screen_size'] = content[5:]

            if('机身颜色：' in content):
                item['color'] = content[5:]
            elif('颜色：' in content):
                item['color'] = content[3:]
            elif('色系：' in content):
                item['color'] = content[3:]

            if('操作系统：' in content):
                item['system'] = content[5:]
            elif('系统：' in content and '显存容量' not in content):
                item['system'] = content[3:]
        print(item)
        yield item  


     
