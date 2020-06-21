import xlrd
import xlwt
import xlutils.copy
import requests
from bs4 import BeautifulSoup
from lxml import etree
import time

class ExcelUtil:
    # 存储路径
    path = ''
    
    # 目标网站地址
    start_url = 'http://www.eastmoney.com/'

    # 请求头
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'
        }
    
    
    # 初始化
    def __init__(self,path):
        self.path = path

    # 读取文件
    def start_spider(self):
        # 利用requests获取目标网站数据
        event_html = requests.get(url=self.start_url,headers=self.headers,timeout=5)
        html=event_html.content
        html_doc=str(html,'utf-8')
        # 利用etree解析网页
        event_req = etree.HTML(html_doc)
        # 利用xpath定位目标数据
        ul_list = event_req.xpath('//div[@id="cjdd_list"]//ul')
        for ul in ul_list:
            

        # 详情页标题
        news_title = event_req.xpath('//div[@id="cjdd_list"]//ul/li/a/text()')
        # 详情页链接
        news_link = event_req.xpath('//div[@id="cjdd_list"]//ul/li/a/@href')
        # 获取详情页数据
        contents = self.getContent(news_link)
        self.writeExcel(self.path,news_title,contents)

    # 写入文件
    def writeExcel(self,path,news_title,contents):
        path = path + time.strftime('%Y年%m月%d日',time.localtime(time.time()))+'.xls'
        data = xlrd.open_workbook(path)
        ws = xlutils.copy.copy(data)
        table=ws.get_sheet(0)
        table.write(0,1,'标题')
        table.write(0,2,'新闻')
        print('开始写入')
        for i in range(len(contents)):
            table.write(i+1,1,news_title[i])
            table.write(i+1,2,contents[i])
        ws.save(path)

    # 读取内容
    def getContent(self,urls):
        urls = urls[1:]
        contents = []
        for url in urls:
            if(url == ''):
                continue
            try:
                response = requests.get(url,timeout=2)
                html=response.content
                html_doc=str(html,'utf-8')
                soup = BeautifulSoup(html_doc, 'lxml')
                content = soup.select('div[id="ContentBody"]')[0].text
                contents.append(content.strip())
            except Exception as e:
                print(e)
                print('数据读取异常：'+url)
        return contents





