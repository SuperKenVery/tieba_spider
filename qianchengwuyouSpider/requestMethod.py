import requests,time,warnings,threading
import pandas as pd
from lxml import etree
warnings.filterwarnings("ignore")

def getdata(bot,top):
    for i in range(bot,top):
        print("正在爬取第" + str(i) + "页的数据")
        url0 = "https://search.51job.com/list/000000,000000,0000,00,9,99,%25E6%2595%25B0%25E6%258D%25AE,2,"
        url_end = ".html?"
        url = url0 + str(i) + url_end
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'
        }
        html = requests.get(url, headers=headers)
        html.encoding = "gbk"
        Html = etree.HTML(html.text)
        # ①岗位名称
        JobName = Html.xpath('//div[@class="dw_table"]/div[@class="el"]//p/span/a[@target="_blank"]/@title')
        # ②公司名称
        CompanyName = Html.xpath('//div[@class="dw_table"]/div[@class="el"]/span[@class="t2"]/a[@target="_blank"]/@title')
        # ③工作地点
        Address = Html.xpath('//div[@class="dw_table"]/div[@class="el"]/span[@class="t3"]/text()')
        # ④工资
        sal = Html.xpath('//div[@class="dw_table"]/div[@class="el"]/span[@class="t4"]')
        salary = [i.text for i in sal]
        # ⑤发布时间
        ShowTime = Html.xpath('//div[@class="dw_table"]/div[@class="el"]/span[@class="t5"]/text()')
        # ⑥获取职位详情url
        DetailUrl = Html.xpath('//div[@class="dw_table"]/div[@class="el"]//p/span/a[@target="_blank"]/@href')
        OthersInfo = []
        JobDescribe = []
        CompanyType = []
        CompanySize = []
        Industry = []
        for i in range(len(DetailUrl)):
            HtmlInfo = requests.get(DetailUrl[i], headers=headers)
            HtmlInfo.encoding = "gbk"
            HtmlInfo = etree.HTML(HtmlInfo.text)
            # ⑦经验、学历信息等其他信息
            otherinfo = HtmlInfo.xpath('//div[@class="tHeader tHjob"]//div[@class="cn"]/p[@class="msg ltype"]/text()')
            # ⑧岗位详情
            JobDescibe = HtmlInfo.xpath('//div[@class="tBorderTop_box"]//div[@class="bmsg job_msg inbox"]/p/text()')
            # ⑨公司类型
            ComType = HtmlInfo.xpath('//div[@class="tCompany_sidebar"]//div[@class="com_tag"]/p[1]/@title')
            # ⑩公司规模(人数)
            ComSize = HtmlInfo.xpath('//div[@class="tCompany_sidebar"]//div[@class="com_tag"]/p[2]/@title')
            # ⑪所属行业(公司)
            industry = HtmlInfo.xpath('//div[@class="tCompany_sidebar"]//div[@class="com_tag"]/p[3]/@title')
            #将上述信息存入列表中
            OthersInfo.append(otherinfo)
            JobDescribe.append(JobDescibe)
            CompanyType.append(ComType)
            CompanySize.append(ComSize)
            Industry.append(industry)
            # 休眠
            time.sleep(0.5)
        # 一边爬取一边写入
        data = pd.DataFrame()
        data["岗位名称"] = JobName
        data["工作地点"] = Address
        data["公司名称"] = CompanyName
        data["工资"] = salary
        data["发布日期"] = ShowTime
        data["经验、学历"] = OthersInfo
        data["所属行业"] = Industry
        data["公司类型"] = CompanyType
        data["公司规模"] = CompanySize
        data["岗位描述"] = JobDescribe
        # 有些网页会跳转到公司官网，会返回空值，所以将其忽略
        try:
            data.to_csv("job_info.csv", mode="a+", header=None, index=None, encoding="gbk")
        except:
            print("跳转官网，无数据")
        time.sleep(1)
    print("数据爬取完成!!!!")

# 此处是创建多个线程的方法，后面可以自行优化

threads = []
t1 = threading.Thread(target=getdata,args=(1,125))
threads.append(t1)
t2 = threading.Thread(target=getdata,args=(125,250))
threads.append(t2)
t3 = threading.Thread(target=getdata,args=(250,375))
threads.append(t3)
t4 = threading.Thread(target=getdata,args=(375,500))
threads.append(t4)
t5 = threading.Thread(target=getdata,args=(500,625))
threads.append(t5)
t6 = threading.Thread(target=getdata,args=(625,750))
threads.append(t6)
t7 = threading.Thread(target=getdata,args=(750,875))
threads.append(t7)
t8 = threading.Thread(target=getdata,args=(875,1000))
threads.append(t8)
# t9 = threading.Thread(target=getdata,args=(1000,1125))
# threads.append(t9)
# t10 = threading.Thread(target=getdata,args=(1125,1250))
# threads.append(t10)
# t11 = threading.Thread(target=getdata,args=(1250,1375))
# threads.append(t11)
# t12 = threading.Thread(target=getdata,args=(1375,1500))
# threads.append(t12)

if __name__ == "__main__":
    for t in threads:
        t.setDaemon(True)
        t.start()