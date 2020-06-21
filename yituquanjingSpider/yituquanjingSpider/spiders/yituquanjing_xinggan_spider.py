import scrapy
from yituquanjingSpider.items import YituquanjingspiderItem


class yituquanjing_spider(scrapy.Spider):
    name = 'yituquanjing_xinggan_spider'
    domains = ['www.yeitu.com']
    # start_url = 'https://www.yeitu.com/'

    # start_url = 'https://www.yeitu.com/meinv/xinggan/'
    # start_url = 'https://www.yeitu.com/meinv/siwameitui/'
    # start_url = 'https://www.yeitu.com/meinv/weimei/'
    # start_url = 'https://www.yeitu.com/meinv/chemo/'
    # start_url = 'https://www.yeitu.com/meinv/wangluomeinv/'
    # start_url = 'https://www.yeitu.com/meinv/tiyumeinv/'
    start_url = 'https://www.yeitu.com/mingxing/nv/'
    


    def start_requests(self):
        yield scrapy.Request(url=self.start_url,callback=self.parse)

    def parse(self,response):
        print(response.text)
        page = response.xpath('//div[@id="pages"]/a/text()').extract()
        count = page[len(page)-1]
        if(not count.isdigit()):
           count =  page[len(page)-2]
        for i in range(int(count)-1):
            if(i==0):
                url = self.start_url
            else:
                url = self.start_url+str(i+1)+'.html'
            yield scrapy.Request(url,callback=self.parsePage)
        

    def parsePage(self,response):
        listUrl = response.xpath('//div[@class="wf"]/ul/li/a/@href').extract()
        print(listUrl)
        titles = response.xpath('//div[@class="wf"]/ul/li/div/a/text()').extract()
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
        item['infoType'] = '美女明星'
        yield item