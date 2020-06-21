import scrapy
from qiantuwang.items import QiantuwangItem


class QiantuwangSpiderSpider(scrapy.Spider):
    name = "qiantuwang_spider"
    allowed_domains = ["588ku.com"]
    #对应的爬取的图片的列表地址
    starturl = 'https://588ku.com/gif/0-0-0-default-'
    offset = 1
    start_urls = [starturl+str(offset)+'/']
    
    # 默认的解析数据
    def parse(self,response):
        listUrl = response.xpath('//a[@class="img-box"]/@href').extract()
        for url in listUrl:
            item = QiantuwangItem()
            yield scrapy.Request("https://"+url,callback=self.parse_item,meta={"item":item})
        # 只爬取前十页的数据
        if(self.offset<2):
            self.offset = self.offset+1
            yield scrapy.Request(self.starturl+str(self.offset)+'/',self.parse)

    # 自定义的详情页解析数据
    def parse_item(self,response):
        item = response.meta['item']
        item['name'] = response.xpath('//img[@class="scaleImg"]/@title').extract()[0]
        item['url'] = response.xpath('//img[@class="scaleImg"]/@src').extract()[0]
        yield item


