# -*- coding: UTF-8 -*-
__author__ = 'Chengrongkai'

ZHILIAN_COOKIE = '4JtkV8kAhpbfbcC_reqGcQ_VnUWyh_lpNEDP.cTIWrSPhXYDfb_ZfayRGSDrgoSb.j.enyyMXpPDUk6D0UtqIXVczz3EnaNjzed5IvQwGTZ_fNFEuat3uuCoTmjUxalepJSABnfF6gc2KAU7DZd1fS2W3mohxrploYSGTE4GPKz2yJSBP1Q7vKenKH9mYmhyv7jNcXLUlr2Cns1c9k5aIde4tBg8VVJfDxLz02xYbroX7_WOArTqxXXp6KQrErK.YRPMrcsIPE2l0x21PedBnum3csokgQZ.AvKTOYSowtWh1MUZmdvBFo0DWETU8KWNBrg.W1uKkrcKpvyDWZ4FTlh3.gTErTDF1NseioZCUkb3XsFXMVxTWkugSL5btWIZxZzAnYUU1d6lnVmnF72Juhr7w'

# 数据库配置
# 服务器ip地址
host='127.0.0.1'
# 端口号
port=3306
# 用户名
user='chengrongkai'
# 密码
passwd='kai941021'
# 数据库名
db='web_crawler'
# 字符集
charset='utf8'

# 需要爬取的城市 建议不要一次性爬取太多，这里维护的是一个数组，若这个数据为空，则默认查询全国
# 前程无忧对查询有限制，全国的数据也只能获取最多30万条，分开按每个省份查询可以加快爬取，并且可以获得更多数据
cityList = ['全国']
# cityList = ['北京','上海','重庆','天津','黑龙江省','辽宁省''吉林省','河北省','河南省','湖北省','湖南省','山东省','山西省','陕西省','安徽省','浙江省','江苏省','福建省','广东省','海南省','四川省','云南省','贵州省','青海省','甘肃省','江西省','台湾省']
# 查询的关键词 如JAVA、python等，可以不配置
keyword = ''

# 开始的页数
startPage = 101

# 每次爬取的页数
pageLimit = 200