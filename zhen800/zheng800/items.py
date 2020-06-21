# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class Zheng800Item(scrapy.Item):
    # define the fields for your item here like:
    title = scrapy.Field()
    frist_url = scrapy.Field()
    urls = scrapy.Field()
    urls1 = scrapy.Field()
