from prettytable import PrettyTable
import requests
import json
import datetime
import time
from openpyxl import Workbook
import random
 

class xiechengSppider:

    city = { '阿尔山': 'YIE', '阿克苏': 'AKU', '阿拉善右旗': 'RHT', '阿拉善左旗': 'AXF', '阿勒泰': 'AAT', '阿里': 'NGQ', '澳门': 'mfm',
            '安庆': 'AQG', '安顺': 'AVA', '鞍山': 'AOG', '巴彦淖尔': 'RLK', '百色': 'AEB', '包头': 'BAV', '保山': 'BSD', '北海': 'BHY',
            '北京': 'bjs', '白城': 'DBC', '白山': 'NBS', '毕节': 'BFJ', '博乐': 'BPL', '重庆': 'CKG', '昌都': 'BPX', '常德': 'CGD',
            '常州': 'CZX', '朝阳': 'CHG', '成都': 'CTU', '池州': 'JUH', '赤峰': 'CIF', '揭阳': 'SWA', '长春': 'CGQ', '长沙': 'CSX',
            '长治': 'CIH', '承德': 'CDE', '沧源': 'CWJ', '达县': 'DAX', '大理': 'DLU', '大连': 'DLC', '大庆': 'DQA', '大同': 'DAT',
            '丹东': 'DDG', '稻城': 'DCY', '东营': 'DOY', '敦煌': 'DNH', '芒市': 'LUM', '额济纳旗': 'EJN', '鄂尔多斯': 'DSN', '恩施': 'ENH',
            '二连浩特': 'ERL', '佛山': 'FUO', '福州': 'FOC', '抚远': 'FYJ', '阜阳': 'FUG', '赣州': 'KOW', '格尔木': 'GOQ', '固原': 'GYU',
            '广元': 'GYS', '广州': 'CAN', '贵阳': 'KWE', '桂林': 'KWL', '哈尔滨': 'HRB', '哈密': 'HMI', '海口': 'HAK', '海拉尔': 'HLD',
            '邯郸': 'HDG', '汉中': 'HZG', '杭州': 'HGH', '合肥': 'HFE', '和田': 'HTN', '黑河': 'HEK', '呼和浩特': 'HET', '淮安': 'HIA',
            '怀化': 'HJJ', '黄山': 'TXN', '惠州': 'HUZ', '鸡西': 'JXA', '济南': 'TNA', '济宁': 'JNG', '加格达奇': 'JGD', '佳木斯': 'JMU',
            '嘉峪关': 'JGN', '金昌': 'JIC', '金门': 'KNH', '锦州': 'JNZ', '嘉义': 'CYI', '西双版纳': 'JHG', '建三江': 'JSJ', '晋江': 'JJN',
            '井冈山': 'JGS', '景德镇': 'JDZ', '九江': 'JIU', '九寨沟': 'JZH', '喀什': 'KHG', '凯里': 'KJH', '康定': 'KGT', '克拉玛依': 'KRY',
            '库车': 'KCA', '库尔勒': 'KRL', '昆明': 'KMG', '拉萨': 'LXA', '兰州': 'LHW', '黎平': 'HZH', '丽江': 'LJG', '荔波': 'LLB',
            '连云港': 'LYG', '六盘水': 'LPF', '临汾': 'LFQ', '林芝': 'LZY', '临沧': 'LNJ', '临沂': 'LYI', '柳州': 'LZH', '泸州': 'LZO',
            '洛阳': 'LYA', '吕梁': 'LLV', '澜沧': 'JMJ', '龙岩': 'LCX', '满洲里': 'NZH', '梅州': 'MXZ', '绵阳': 'MIG', '漠河': 'OHE',
            '牡丹江': 'MDG', '马祖': 'MFK', '南昌': 'KHN', '南充': 'NAO', '南京': 'NKG', '南宁': 'NNG', '南通': 'NTG', '南阳': 'NNY',
            '宁波': 'NGB', '宁蒗': 'NLH', '攀枝花': 'PZI', '普洱': 'SYM', '齐齐哈尔': 'NDG', '黔江': 'JIQ', '且末': 'IQM', '秦皇岛': 'BPE',
            '青岛': 'TAO', '庆阳': 'IQN', '衢州': 'JUZ', '日喀则': 'RKZ', '日照': 'RIZ', '三亚': 'SYX', '厦门': 'XMN', '上海': 'SHA',
            '深圳': 'SZX', '神农架': 'HPG', '沈阳': 'SHE', '石家庄': 'SJW', '塔城': 'TCG', '台州': 'HYN', '太原': 'TYN', '扬州': 'YTY',
            '唐山': 'TVS', '腾冲': 'TCZ', '天津': 'TSN', '天水': 'THQ', '通辽': 'TGO', '铜仁': 'TEN', '吐鲁番': 'TLQ', '万州': 'WXN',
            '威海': 'WEH', '潍坊': 'WEF', '温州': 'WNZ', '文山': 'WNH', '乌海': 'WUA', '乌兰浩特': 'HLH', '乌鲁木齐': 'URC', '无锡': 'WUX',
            '梧州': 'WUZ', '武汉': 'WUH', '武夷山': 'WUS', '西安': 'SIA', '西昌': 'XIC', '西宁': 'XNN', '锡林浩特': 'XIL',
            '香格里拉(迪庆)': 'DIG',
            '襄阳': 'XFN', '兴义': 'ACX', '徐州': 'XUZ', '香港': 'HKG', '烟台': 'YNT', '延安': 'ENY', '延吉': 'YNJ', '盐城': 'YNZ',
            '伊春': 'LDS',
            '伊宁': 'YIN', '宜宾': 'YBP', '宜昌': 'YIH', '宜春': 'YIC', '义乌': 'YIW', '银川': 'INC', '永州': 'LLF', '榆林': 'UYN',
            '玉树': 'YUS',
            '运城': 'YCU', '湛江': 'ZHA', '张家界': 'DYG', '张家口': 'ZQZ', '张掖': 'YZY', '昭通': 'ZAT', '郑州': 'CGO', '中卫': 'ZHY',
            '舟山': 'HSN',
            '珠海': 'ZUH', '遵义(茅台)': 'WMT', '遵义(新舟)': 'ZYI'}

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36",
        "Content-Type": "application/json",  # 声明文本类型为 json 格式,
        'Cookie': '_abtest_userid=8ee7fbb6-7736-451f-b2ea-984201e35a64; _RF1=171.41.89.230; _RSG=ZBK1gcs5xmAbbbm7MUkvE9; _RDG=28c37ba2bc5ec028c603c559529e259742; _RGUID=ac3b1769-aa05-42e3-93b9-b9e587c25965; MKT_CKID=1581075861927.0cj2v.d9oy; MKT_CKID_LMT=1581075861928; _ga=GA1.2.2105747730.1581075862; _gid=GA1.2.769732103.1581075862; MKT_Pagesource=PC; __guid=208962885.4174806476472203300.1581075939262.9272; DomesticUserHostCity=SHA%7c%c9%cf%ba%a3; gad_city=6712d5626914d5b6588dd7cf3ca6ea27; Session=SmartLinkCode=U153507&SmartLinkKeyWord=&SmartLinkQuary=&SmartLinkHost=&SmartLinkLanguage=zh; Union=OUID=title&AllianceID=5376&SID=153507&SourceID=&createtime=1581142158&Expires=1581746958354; appFloatCnt=6; FlightIntl=Search=[%22MFM|%E6%BE%B3%E9%97%A8(MFM)|59|MFM|480%22%2C%22SHA|%E4%B8%8A%E6%B5%B7(SHA)|2|SHA|480%22%2C%222020-02-08%22]; FD_SearchHistorty={"type":"S","data":"S%24%u6FB3%u95E8%28MFM%29%24MFM%242020-02-08%24%u4E0A%u6D77%28SHA%29%24SHA%24%24%24"}; _bfa=1.1581075859309.38802l.1.1581138619177.1581149403858.5.41; _bfs=1.1; _jzqco=%7C%7C%7C%7C1581075942690%7C1.1864799789.1581075861923.1581144138528.1581149406051.1581144138528.1581149406051.undefined.0.0.34.34; __zpspc=9.5.1581149406.1581149406.1%232%7Csp0.baidu.com%7C%7C%7C%25E6%2590%25BA%25E7%25A8%258B%7C%23; _gat=1; _bfi=p1%3D10320673302%26p2%3D10320673302%26v1%3D41%26v2%3D40; monitor_count=28'
    }

    def __init__(self,date_list,start_city,end_city):
        self.date_list = date_list
        self.start_city = start_city
        self.end_city = end_city
        self.wb = Workbook()
        self.ws = self.wb.active
        self.ws.append(['出发日期', '航空公司', '航班号', '出发城市','到达城市','起飞时间', '到达时间', '到达准点率', '价格'])
    
    def statr_spider(self):
        for date in self.date_list:
            data = self.getinfo(date,self.start_city,self.end_city)
            self.saveToCsv(data)
            time.sleep(random.uniform(5,15))
                


    def getinfo(self,date,start_city,end_city):
        url = 'https://flights.ctrip.com/itinerary/api/12808/products'
        request_payload = {"flightWay": "Oneway",
                        "army": "false",
                        "classType": "ALL",
                        "hasChild": 'false',
                        "hasBaby": 'false',
                        "searchIndex": 1,
                        "token": "a205997a42fbb033706dce5bd54cb15c",
                        "airportParams": [
                            {"dcity": self.city.get(start_city), "acity": self.city.get(end_city), 
                            "dcityname": self.start_city, "acityname": self.end_city,
                                "date": date}]}
    
        # 这里传进去的参数必须为 json 格式
        response = requests.post(url, data=json.dumps(request_payload), headers=self.headers).text
        routeList = json.loads(response)["data"].get('routeList')
        return self.printTable(routeList,date)

    
    def saveToCsv(self,data):
        for item in data:
            line = [item['出发日期'], item['航空公司'],item['航班号'],item['出发城市'],item['到达城市']
            ,item['起飞时间'],item['到达时间'],item['到达准点率'],item['价格']]
            self.ws.append(line)
            self.wb.save('携程机票信息_'+self.start_city+'到'+self.end_city+'.xlsx')
    
    def printTable(self,routeList,date):
        table = PrettyTable(["出发日期","航空公司","航班号" ,"出发城市","到达城市", "起飞时间","到达时间", "到达准点率", "价格"])
        # print("123",routeList)
        data = []
        for route in routeList:
            if len(route.get('legs')) == 1:
                info = {}
                legs = route.get('legs')[0]
                flight = legs.get('flight')
                info['出发日期'] = date
                info['航空公司'] = flight.get('airlineName')
                info['航班号'] = flight.get('flightNumber')
                info['出发城市'] = self.start_city
                info['到达城市'] = self.end_city
                info['起飞时间'] = flight.get('departureDate')[-8:-3]
                info['到达时间'] = flight.get('arrivalDate')[-8:-3]
                info['到达准点率'] = flight.get('punctualityRate')
                info['价格'] = legs.get('characteristic').get('lowestPrice')
    
                table.add_row(info.values())
                print(table)
                data.append(info)
        return data

def getLastMonthDay(days):
    begin_date = (datetime.datetime.now()).strftime("%Y-%m-%d")
    date_list = []
    begin_date = datetime.datetime.strptime(begin_date, "%Y-%m-%d")
    end_date = datetime.datetime.strptime((datetime.datetime.now() + datetime.timedelta(days =days)).strftime("%Y-%m-%d"), "%Y-%m-%d")
    while begin_date <= end_date:
        date_str = begin_date.strftime("%Y-%m-%d")
        date_list.append(date_str)
        begin_date += datetime.timedelta(days=1)
    return date_list

 
 
if __name__ == "__main__":
    # 出发城市
    start_city = "广州"
    # 到达城市
    end_city = "上海"
    # 从当前日期开始后多少天的数据
    days = 90
    dateList = getLastMonthDay(days)
    spider = xiechengSppider(dateList,start_city,end_city)
    spider.statr_spider()
