# -*- coding: UTF-8 -*-
__author__ = 'Chengrongkai'

# 浏览器驱动地址
driver_path = 'D://soft/ChromeCore/chromedriver.exe'



# 数据库连接信息
# 服务器ip地址
host='127.0.0.1'
# 端口号
port=3306
# 用户名
user='xxx'
# 密码
passwd='xxxx'
# 数据库名
db='xxxx'
# 字符集
charset='utf8mb4'
# 需要采集的网站:1、博客园;2、东方财富网;3、开源中国；4、csdn;5、掘金社区;6、大众娱乐;7、微信公众号;8、同花顺财经
config_spiders = [1,3,4]
# 发布的平台:1、百家号
config_publishers = [1]