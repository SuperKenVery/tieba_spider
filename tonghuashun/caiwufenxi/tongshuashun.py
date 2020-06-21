# -*- coding: UTF-8 -*-
__author__ = 'Chengrongkai'

from selenium import webdriver
from openpyxl import Workbook,load_workbook
from selenium.webdriver.common.action_chains import ActionChains
import time
import requests 
from lxml import etree
import json
import random

"""
目的:爬取同花顺网站的股票财务分析信息
爬取工具:selenium、requests
爬取过程:
通过txt文件读取要爬取的股票的code列表
然后通过selenium获取财务分析页面的表头部分数据
直接抓取到表头里面的iframe页面的跳转地址，获取到对应的code请求参数
然后直接找到对应的详细数据的请求js，通过requests请求这个js的数据，
解析json数据。
接着用selenium获取具体的财务报表相关页面的数据，通过selenium点击
切换li标签，然后获取具体的元素。
最后一次性将所有的数据存储到excel文件中
"""


class Spider:
    # 初始化，传入设置的驱动路径
    def __init__(self,driverPath):
        self.driverPath = driverPath
    # 开始爬取
    def start_action(self,read_file,save_path,jidu_list):
        # 读取需要爬取的股票
        list = self.get_code_list(read_file)
        # 处理股票信息
        data_list = self.get_info_list(list)
        # 存储到excel
        self.save_excel(data_list,save_path,jidu_list)
    # 通过txt文件读取爬取的股票code
    def get_code_list(self,read_file):
        f = open(read_file,"r")   #设置文件对象
        data = f.readlines()  #直接将文件中按行读到list里，
        f.close()
        return data

    # 获取股票信息
    def get_info_list(self,list):
        data = []
        for code in list:
            code = code.strip()
            if(code.isdigit()):
                data.append(self.get_finance_info(code))
        return data
    # 获取股票的头部信息
    def get_head_info(self,code):
        browser = webdriver.Chrome(self.driverPath)
        base_url = 'http://stockpage.10jqka.com.cn/'+str(code)+'/'
        event_url = base_url+'finance'
        browser.implicitly_wait(20)
        browser.get(event_url)
        html = browser.page_source
        browser.quit()
        reponse = etree.HTML(html)
        iframe_url = reponse.xpath('//iframe[@name="ifm"]/@src')[0]
        code_new = iframe_url.split('#')[1]
        print(code)
        js_url = 'http://d.10jqka.com.cn/v2/realhead/{}/last.js'.format(code_new)
        print(js_url)
        headers = {
            'Referer':'http://stockpage.10jqka.com.cn/{}/'.format(code),
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
        }
        info = {}
        response = requests.get(js_url,headers=headers) #使用代理
        print(response.status_code)
        if response.status_code == 200:
            result = response.text
            # print(result)
            data = result[result.index('_last')+6:len(result)-1]
            print(data)
            jsons = json.loads(data)
            item = jsons['items']
            print(item)   
            info_price = item['10']
            print(info_price)
            info = {
                '股票价格':item['10'],
                '涨跌幅':item['199112'],
                '成交额':item['19'],
                '总市值':item['3541450'],
                '换手':item['1968584'],
                '市盈率(动)':item['2034120'],
            }
        # time.sleep(random.uniform(1,30))
        return info
        

    
    # 获取股票详细信息
    def get_finance_info(self,code):
        item = self.get_head_info(code)

        browser = webdriver.Chrome(self.driverPath)
        browser.implicitly_wait(20)
        base_url = 'http://basic.10jqka.com.cn/'+str(code)+'/'
        event_url = base_url+'finance.html'
        browser.get(event_url)
        item['股票名称'] = browser.find_element_by_xpath('/html/body/div[3]/div[1]/div[2]/div[1]/div[1]/h1').text.strip()
        item['股票代码'] = browser.find_element_by_xpath('/html/body/div[3]/div[1]/div[2]/div[1]/div[2]/h1').text.strip()
        print(item)
        time.sleep(2)
        caiwu = browser.find_element_by_xpath('//ul[@class="tabDataTab m_tab"]/li[3]/a')
        caiwu.click()
        ths = browser.find_elements_by_xpath('//div[@class="data_tbody"]/table[@class="top_thead"]//th/div')

        tds1 = browser.find_elements_by_xpath('//div[@class="data_tbody"]/table[@class="tbody"]//tr[5]/td')

        tds2 = browser.find_elements_by_xpath('//div[@class="data_tbody"]/table[@class="tbody"]//tr[7]/td')

        tds3 = browser.find_elements_by_xpath('//div[@class="data_tbody"]/table[@class="tbody"]//tr[13]/td')

        tds4 = browser.find_elements_by_xpath('//div[@class="data_tbody"]/table[@class="tbody"]//tr[16]/td')
        
        times = []
        for i in range(6):
            time_de = ths[i].text
            times.append(time_de)
            year = time_de[0:4]
            month_day = time_de[5:]
            jidu = self.get_convert(month_day)
            item[year+'年'+jidu+'扣非'] = tds1[i].text
            item[year+'年'+jidu+'营收'] = tds2[i].text
            item[year+'年'+jidu+'现金流'] = tds3[i].text
            item[year+'年'+jidu+'毛利率'] = tds4[i].text
        browser.quit()   
        item['times'] = times
        return item

    def get_convert(self,month_day):
        # 时间转换
        conver_dict = {'03-31':'Q1','06-30':'Q2','09-30':'Q3','12-31':'Q4'}
        return conver_dict[month_day]

    def get_unit(self,unit):
        if(unit.find('亿')!=-1):
            return 100000000
        elif(unit.find('万')!=-1):
            return 10000
        else:
            return 1

    # 保存到excel
    def save_excel(self,data_list,save_path,jidu_list):
        print(data_list)
        wb = Workbook()
        ws = wb.active
        title = [ '股票代码','股票名称','股票价格','涨跌幅','成交额', '总市值','换手' , '市盈率(动)']
        # frist = data_list[0]
        # times = frist['times']
        for tiem_str in jidu_list:
            # year = time[0:4]
            # month_day = time[5:]
            # jidu = self.get_convert(month_day)
            title.append(tiem_str+'扣非')
            title.append(tiem_str+'营收')
            title.append(tiem_str+'现金流')
            title.append(tiem_str+'毛利率')     
        ws.append(title)
        for item in data_list:
            line = [item['股票代码'], item['股票名称'], item['股票价格'], item['涨跌幅'], item['成交额']
            , item['总市值'], item['换手'] , item['市盈率(动)'] ]
            for tiem_str in jidu_list:
                # year = time[0:4]
                # month_day = time[5:]
                # jidu = self.get_convert(month_day)
                if((tiem_str + '扣非') in item):
                    line.append(item[tiem_str+'扣非'])
                else:
                    line.append('')
                if((tiem_str + '营收') in item):
                    line.append(item[tiem_str+'营收'])
                else:
                    line.append('')
                if((tiem_str + '现金流') in item):
                    line.append(item[tiem_str+'现金流'])
                else:
                    line.append('')
                if((tiem_str + '毛利率') in item):
                    line.append(item[tiem_str+'毛利率'])
                else:
                    line.append('')
            ws.append(line)
        wb.save(save_path)
        print('采集完成')

        
    

    
if __name__ == "__main__":
    # 驱动文件位置
    driverPath = "D:/workspace/python/pythonTask/tonghuashunSpider/browser/chromedriver.exe"
    spider = Spider(driverPath)
    # 读取的股票信息
    read_file = "data.txt"
    # 保存的excel路径
    save_path = "tonghuashun.xlsx"
    # 需要爬取的季度数据
    jidu_list = ['2019年Q3','2019年Q2','2019年Q1','2018年Q4','2018年Q3','2018年Q2']
    spider.start_action(read_file,save_path,jidu_list)

