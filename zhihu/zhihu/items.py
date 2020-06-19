# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ZhihuItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # 用户名
    user_name = scrapy.Field()
    # 用户性别
    sex  = scrapy.Field()
    # 用户签名
    user_sign = scrapy.Field()
    # 用户主页
    user_url = scrapy.Field()
    # 用户头像
    user_avatar = scrapy.Field()
    # 附加信息
    user_add = scrapy.Field()

class ZhihuActivityItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # 用户名
    user_name = scrapy.Field()
    # 活动标题，如问题标题
    title  = scrapy.Field()
    # 活动类型 比如关注的话题、赞同的话题。。。
    activity_type = scrapy.Field()