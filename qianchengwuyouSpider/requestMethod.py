import requests,time,warnings,threading
import pandas as pd
from lxml import etree
import random
warnings.filterwarnings("ignore")

# 获取代理IP
def get_proxy():
    return requests.get("http://127.0.0.1:5010/get/").json()

# 删除失效的代理IP
def delete_proxy(proxy):
    requests.get("http://127.0.0.1:5010/delete/?proxy={}".format(proxy))


# your spider code

# 利用代理IP请求
def getHtml(url):
    # ....
    retry_count = 5
    proxy = get_proxy().get("proxy")
    while retry_count > 0:
        try:
            headers = {
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'
                    }
            print("代理信息:{}".format(proxy))
            html = requests.get(url,headers=headers, proxies={"http": "http://{}".format(proxy)})
            # 使用代理访问
            return html
        except Exception:
            retry_count -= 1
    # 出错5次, 删除代理池中代理
    delete_proxy(proxy)
    return None

def getdata(bot,top):
    for i in range(bot,top):
        print("正在爬取第" + str(i) + "页的数据")
        url0 = "https://search.51job.com/list/000000,000000,0000,00,9,99,%25E6%2595%25B0%25E6%258D%25AE,2,"
        url_end = ".html?"
        url = url0 + str(i) + url_end
        html = getHtml(url)
        if(html == None):
            continue
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
            HtmlInfo = getHtml(DetailUrl[i])
            HtmlInfo.encoding = "gbk"
            HtmlInfo = etree.HTML(HtmlInfo.text)
            if(HtmlInfo == None):
                continue
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
            time.sleep(random.uniform(0.1,1))
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
        time.sleep(random.uniform(0.2,0.5))
        print("数据爬取完成!!!!")

# 分配线程任务
def start_spider(num):
    start = 1
    end = 0
    count = 2000
    size = count//(num-1)
    print(size)
    while num > 1:
        end = start+size
        t = threading.Thread(target=getdata,args=(start,end))
        start = end+1
        t.start()
        num = num-1
    # 分配剩下的任务给新的线程
    if(end < count):
        start = end+1
        end = count
        t = threading.Thread(target=getdata,args=(start,end))
        t.start()

if __name__ == "__main__":
    num = 8
    start_spider(num)