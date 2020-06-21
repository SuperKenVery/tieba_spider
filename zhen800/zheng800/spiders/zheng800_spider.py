import scrapy
from zheng800.items import Zheng800Item

class zheng800Spider(scrapy.Spider):
    name = 'zheng800_spider'
    domain = ['www.zheng800.com']
    start_url = 'http://www.zheng800.com/plus/list.php?tid=5&PageNo='
    offset = 1
    start_urls = [start_url+str(offset)]

    # 默认的解析数据
    def parse(self,response):
        listUrl = response.xpath('//span[@class="cheaptitleword"]/a/@href').extract()
        titles = response.xpath('//span[@class="cheaptitleword"]/a/text()').extract()
        frist_url = response.xpath('//div[@class="cheapimga"]/a/img/@src').extract()
        for i in range(len(listUrl)):
            item = Zheng800Item()
            item['frist_url'] = frist_url[i]
            item['title'] = titles[i]
            detal_url = listUrl[i]
            # print(detal_url)
            yield scrapy.Request(detal_url,callback=self.parse_item,meta={"item":item})
        # 只爬取前十页的数据
        self.offset = self.offset+1
        yield scrapy.Request(self.start_url+str(self.offset),self.parse)

    # 自定义的详情页解析数据
    def parse_item(self,response):
        item = response.meta['item']
        item['urls1'] = response.xpath('//div[@data-plugin="autoitem"]/img/@src').extract()
        item['urls'] = response.xpath('//div[@data-plugin="autoitem"]/p/a/@href').extract()
        yield item

