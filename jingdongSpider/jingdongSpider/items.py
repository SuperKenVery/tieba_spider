# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class JingdongspiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class Category(scrapy.Item):
    #大分类名称
    b_category_name=scrapy.Field()
    #大分类的URL
    b_category_url=scrapy.Field()
    #中分类名称
    m_category_name=scrapy.Field()
    #中分类URL
    m_category_url=scrapy.Field()
    #小分类名称
    s_category_name=scrapy.Field()
    #小分类URL
    s_category_url=scrapy.Field()
    
class Product(scrapy.Item):
    product_type = scrapy.Field()#商品类型
    brand=scrapy.Field()#商品品牌
    name=scrapy.Field()#商品名称
    code=scrapy.Field()#商品编号
    weight=scrapy.Field()#商品毛重
    cpu=scrapy.Field()#cpu
    # run_size=scrapy.Field()#运行内存
    file_save=scrapy.Field()#机身存储
    # save_card=scrapy.Field()#存储卡
    # back_photo=scrapy.Field() #后置摄像头
    # front_photo=scrapy.Field()#前置摄像头
    screen_size=scrapy.Field() #屏幕大小
    # screen_percent=scrapy.Field()#屏幕百分比
    # screen_type=scrapy.Field() #屏幕类型
    # power_size=scrapy.Field()#电池容量
    color=scrapy.Field() #颜色
    system=scrapy.Field()#操作系统
    classification = scrapy.Field()#分类
