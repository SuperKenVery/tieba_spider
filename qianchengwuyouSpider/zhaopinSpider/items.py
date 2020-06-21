# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ZhaopinspiderItem(scrapy.Item):
    # define the fields for your item here like:
    # 工作ID
    id = scrapy.Field()
    # 工作名称
    jobName = scrapy.Field()
    # 招聘详细链接
    positionURL = scrapy.Field()
    # 公司名称
    companyName = scrapy.Field()
    # 公司描述
    companyDesc = scrapy.Field()
    # 公司ID
    companyNumber = scrapy.Field()
    # 公司性质
    companyType = scrapy.Field()
    # 公司所在行业
    companyIndustry = scrapy.Field()
    # 公司规模
    companySize = scrapy.Field()
    # 公司招聘主页
    companyUrl = scrapy.Field()
    # 公司地点
    companyDisplay = scrapy.Field()
    # 薪资
    salary = scrapy.Field()
    # 学历要求
    eduLevel = scrapy.Field()
    # 工作经历
    workingExp = scrapy.Field()
    # 招聘人数
    peopleNum = scrapy.Field()
    # 职位类型
    emplType = scrapy.Field()
    # 公司福利
    welfare = scrapy.Field()
    # 工作发布标签
    timeState = scrapy.Field()
    # 更新时间
    updateDate = scrapy.Field()
    # 职位描述
    jobDetail = scrapy.Field()
    # 地理位置
    position = scrapy.Field()
