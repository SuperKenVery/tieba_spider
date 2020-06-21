import scrapy
from yituquanjingSpider.items import YituquanjingspiderItem


class yituquanjing_spider(scrapy.Spider):
    name = 'yituquanjing_spider'
    domains = ['www.yeitu.com']
    start_url = 'https://www.yeitu.com/'

    start_url = 'https://www.yeitu.com/meinv/xinggan/'


    def start_requests(self):
        yield scrapy.Request(url=self.start_url,callback=self.parse)

    def parse(self,response):
        # print(response.text)
        listUrl = response.xpath('//div[@class="list-box"]/ul/li/a/@href').extract()
        print(listUrl)
        titles = response.xpath('//div[@class="list-box"]/ul/li/a/@title').extract()
        for i in range(len(listUrl)):
            item = YituquanjingspiderItem()
            item['title'] = titles[i]
            url = listUrl[i]
            item['url'] = url
            yield scrapy.Request(url=url,callback=self.parseList,meta={"item":item})


    def parseList(self,response):
        # print(response.text)
        item = response.meta['item']
        page = response.xpath('//div[@id="pages"]/a/text()').extract()
        print(page)
        count = page[len(page)-1]
        if(not count.isdigit()):
           count =  page[len(page)-2]
        for i in range(int(count)):
            url = item['url'].replace('.html','_'+str(i+2)+'.html')
            print(url)
            yield scrapy.Request(url = url,callback=self.parseItem,meta={"item":item})

    def parseItem(self,response):

        item = response.meta['item']
        image = response.xpath('//div[@class="img_content"]/div[@class="img_box"]/a/img/@src').extract()
        item['imageUrl'] = image[0]
        item['infoType'] = '亿图全景'
        yield item