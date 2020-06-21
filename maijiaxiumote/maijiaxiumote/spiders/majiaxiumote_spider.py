import scrapy
from maijiaxiumote.items import MaijiaxiumoteItem

class maijiaxiumoteSpider(scrapy.Spider):
    name = 'majiaxiumote_spider'
    domain = 'www.tbqq.net'
    basedomain = 'http://www.tbqq.net'
    start_url = 'http://www.tbqq.net/forum.php?mod=forumdisplay&fid=2&sortid=2&sortid=2&page='
    offset = 1
    start_urls = [start_url+str(offset)]

    # 默认的解析数据
    def parse(self,response):
        listUrl = response.xpath('//div[@class="deanmadouname"]/a/@href').extract()
        titles = response.xpath('//div[@class="deanmadouname"]/a/text()').extract()
        for i in range(len(listUrl)):
            item = MaijiaxiumoteItem()
            item['name'] = titles[i]
            detal_url = self.basedomain+'/'+listUrl[i]
            # print(detal_url)
            headers = {'referer': detal_url}
            yield scrapy.Request(detal_url,callback=self.parse_item,meta={"item":item},headers=headers)
  
        self.offset = self.offset+1
        yield scrapy.Request(self.start_url+str(self.offset),self.parse)

    # 自定义的详情页解析数据
    def parse_item(self,response):
        item = response.meta['item']
        item['pics'] = response.xpath('//div[@class="deanmotepic"]/ul/li/img/@src').extract()
        item['picdetails'] = response.xpath('//td[@class="t_f"]/ignore_js_op/img/@zoomfile').extract()
        item['age'] = response.xpath('//div[@class="deanmdclinfo"]/div[1]/em/text()').extract()
        item['position'] = response.xpath('//div[@class="deanmdclinfo"]/div[2]/em/text()').extract()
        item['name'] = response.xpath('//div[@class="deanmdclinfo"]/div[5]/em/text()').extract()
        item['c_type'] = response.xpath('//div[@class="deanmdclinfo"]/div[6]/em/text()').extract()
        yield item