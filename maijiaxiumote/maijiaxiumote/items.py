# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class MaijiaxiumoteItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    age = scrapy.Field()
    position = scrapy.Field()
    c_type = scrapy.Field()
    pics = scrapy.Field()
    picdetails = scrapy.Field()
